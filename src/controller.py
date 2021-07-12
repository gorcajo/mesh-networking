import logging
import math
from typing import Tuple

import pygame

from simulation import Simulation
from node import Node
from point import Point


GRID_SIZE = 20
GRID_GEOMETRY = (80, 40)

SCREEN_GEOMETRY = (GRID_GEOMETRY[0] * GRID_SIZE, GRID_GEOMETRY[1] * GRID_SIZE)
SCREEN_WIDTH = SCREEN_GEOMETRY[0]
SCREEN_HEIGHT = SCREEN_GEOMETRY[1]

BACKGROUND_COLOR = (20, 20, 20)

AXIS_COLOR = (40, 40, 40)

NODE_SIZE = 10
NODE_BORDER_SIZE = 2
NODE_ONLINE_COLOR = (180, 180, 250)
NODE_OFFLINE_COLOR = (30, 30, 30)
NODE_ONLINE_BORDER_COLOR = (255, 255, 255)
NODE_OFFLINE_BORDER_COLOR = (255, 80, 80)
NODE_TEXT_COLOR = (80, 80, 80)
NODE_POWER_COLOR = (255, 255, 0)
NODE_POWER_BORDER_SIZE = 1

LINK_LINE_WIDTH = 2
LINK_ARROW_HEAD_SIZE = 4
LINK_COLOR = (50, 50, 150)

MESSAGE_SIZE = 3
MESSAGE_COLORS = [
    (200, 200, 0),
    (150, 150, 255),
    (0, 150, 0),
    (255, 70, 0),
    (255, 255, 255),
]

FONT_FAMILY = 'monospace'
FONT_SIZE = 12


logging.basicConfig(
    format  = '%(asctime)-5s.%(msecs)03d | %(levelname)-7s | %(message)s',
    level   = logging.INFO,
    datefmt = '%Y-%m-%d %H:%M:%S')


class Engine:

    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)

        self.screen = pygame.display.set_mode(SCREEN_GEOMETRY, 0, 32)
        pygame.display.set_caption('Mesh Viewer')

        self.running = False


    def loop(self) -> None:
        clock = pygame.time.Clock()
        self.running = True

        self.init()
        
        frame = 0

        while self.running:
            self.update(frame)
            self.draw()
            clock.tick(60)
            frame += 1


    def init(self) -> None:
        print('''
        Simulation controls:
          - M:                 Inject a new message
          - SPACE:             Run a simulation step
          - R:                 Reset and refresh
          - Mouse over a node: Display power range and reached nodes

        Edition controls:
          - Left-click on a node: Toggle online/offline
          - Mouse-wheel on a node: Increase/decrease power
          - Right-click on a node:      Remove node
          - Right-click on empty space: Create node
          - CTRL+S: Save nodes

        Common controls:
          - ESC: Exit
        ''')
        self.simulation = Simulation()


    def update(self, frame: int) -> None:
        if frame % 20 == 0:
            self.simulation.refresh_if_nodes_file_changed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.simulation.run_step()
                elif event.key == pygame.K_m:
                    self.simulation.inject_new_message()
                elif event.key == pygame.K_r:
                    self.simulation.refresh()
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.simulation.save()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    print(":D")
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                left_button = pygame.mouse.get_pressed()[0]
                right_button = pygame.mouse.get_pressed()[2]
                wheel_up = event.button == 4
                wheel_down = event.button == 5

                mouse_pos = Point.from_mouse_pos(pygame.mouse.get_pos())

                for node in self.simulation.medium.nodes:
                    if mouse_pos.distance_to(node_to_screen_pos(node)) <= NODE_SIZE:
                        if left_button:
                            node.online = not node.online
                        elif right_button:
                            self.simulation.remove_node(node)
                        elif wheel_up:
                            node.power += 1
                        elif wheel_down:
                            node.power -= 1

                        break
                else:
                    if right_button:
                        self.simulation.create_node(screen_pos_to_point(mouse_pos))


    def draw(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)

        self.draw_axis()

        mouse_pos = Point.from_mouse_pos(pygame.mouse.get_pos())

        for node in self.simulation.medium.nodes:
            if mouse_pos.distance_to(node_to_screen_pos(node)) <= NODE_SIZE:
                self.draw_node_range(node)

                for other in self.simulation.medium.nodes:
                    if node.id != other.id and node.pos.distance_to(other.pos) <= node.power:
                        self.highlight_node(other)

        for node in self.simulation.medium.nodes:
            if not node.online:
                continue

            for other in self.simulation.medium.nodes:
                if node.id != other.id and other.online and node.pos.distance_to(other.pos) <= node.power:
                    self.draw_link(node, other)

        for node in self.simulation.medium.nodes:
            self.draw_node(node)

        for node in self.simulation.medium.nodes:
            self.draw_messages(node)

        pygame.display.update()
    

    def draw_axis(self) -> None:
        pygame.draw.line(self.screen, AXIS_COLOR, (0, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2))
        pygame.draw.line(self.screen, AXIS_COLOR, (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))

        for i in range(1, int(SCREEN_WIDTH/GRID_SIZE)):
            pygame.draw.line(
                self.screen,
                AXIS_COLOR,
                (GRID_SIZE * i, SCREEN_HEIGHT/2 - 4),
                (GRID_SIZE * i, SCREEN_HEIGHT/2 + 4))

        for i in range(1, int(SCREEN_WIDTH/GRID_SIZE)):
            pygame.draw.line(
                self.screen,
                AXIS_COLOR,
                (SCREEN_WIDTH/2 - 4, GRID_SIZE * i),
                (SCREEN_WIDTH/2 + 4, GRID_SIZE * i))


    def draw_node(self, node: Node) -> None:
        center = node_to_screen_pos(node)

        node_color = NODE_ONLINE_COLOR if node.online else NODE_OFFLINE_COLOR
        node_border_color = NODE_ONLINE_BORDER_COLOR if node.online else NODE_OFFLINE_BORDER_COLOR
        
        pygame.draw.circle(self.screen, node_color, (center.x, center.y), NODE_SIZE - NODE_BORDER_SIZE)
        pygame.draw.circle(self.screen, node_border_color, (center.x, center.y), NODE_SIZE, NODE_BORDER_SIZE)

        text = self.font.render(str(node.id), False, NODE_TEXT_COLOR)
        text_x = center.x - (text.get_rect().width / 2)
        text_y = center.y - (text.get_rect().height / 2)
        self.screen.blit(text, (text_x, text_y))


    def draw_messages(self, node: Node) -> None:
        center = node_to_screen_pos(node)

        for i, message in enumerate(node.input_queue):
            x = center.x + NODE_SIZE + 4
            y = center.y - NODE_SIZE + ((MESSAGE_SIZE + 1) * 2 * i)
            color = MESSAGE_COLORS[message.id % len(MESSAGE_COLORS)]
            pygame.draw.circle(self.screen, color, (x, y), MESSAGE_SIZE)


    def draw_node_range(self, node: Node) -> None:
        center = node_to_screen_pos(node)
        pygame.draw.circle(self.screen, NODE_POWER_COLOR, (center.x, center.y), node.power * GRID_SIZE, NODE_POWER_BORDER_SIZE)


    def highlight_node(self, node: Node) -> None:
        center = node_to_screen_pos(node)
        pygame.draw.circle(self.screen, NODE_POWER_COLOR, (center.x, center.y), NODE_SIZE * 1.5, NODE_POWER_BORDER_SIZE)


    def draw_link(self, from_node: Node, to_node: Node) -> None:
        from_pos = (Point(from_node.pos.x, -from_node.pos.y) * GRID_SIZE) + (Point(SCREEN_WIDTH, SCREEN_HEIGHT) / 2)
        to_pos = (Point(to_node.pos.x, -to_node.pos.y) * GRID_SIZE) + (Point(SCREEN_WIDTH, SCREEN_HEIGHT) / 2)

        from_pos, to_pos = shrink_line(from_pos, to_pos, NODE_SIZE + NODE_BORDER_SIZE * 2)

        pygame.draw.line(self.screen, LINK_COLOR, (from_pos.x, from_pos.y), (to_pos.x, to_pos.y), LINK_LINE_WIDTH)

        rotation = math.degrees(math.atan2(from_pos.y - to_pos.y, to_pos.x - from_pos.x)) + 90

        triangle_vertice_0 = (
            to_pos.x + LINK_ARROW_HEAD_SIZE * math.sin(math.radians(rotation)),
            to_pos.y + LINK_ARROW_HEAD_SIZE * math.cos(math.radians(rotation)))

        triangle_vertice_1 = (
            to_pos.x + LINK_ARROW_HEAD_SIZE * math.sin(math.radians(rotation - 120)),
            to_pos.y + LINK_ARROW_HEAD_SIZE * math.cos(math.radians(rotation - 120)))

        triangle_vertice_2 = (
            to_pos.x + LINK_ARROW_HEAD_SIZE * math.sin(math.radians(rotation + 120)),
            to_pos.y + LINK_ARROW_HEAD_SIZE * math.cos(math.radians(rotation + 120)))

        pygame.draw.polygon(self.screen, LINK_COLOR, (triangle_vertice_0, triangle_vertice_1, triangle_vertice_2))


def shrink_line(from_pos: Point, to_pos: Point, reduction: int) -> Tuple[Point, Point]:
    line = to_pos - from_pos
    new_modulus = line.modulus - reduction
    line = Point.from_polar(new_modulus, line.angle)
    to_pos = line + from_pos
    return (from_pos, to_pos)


def node_to_screen_pos(node: Node) -> Point:
    return (Point(node.pos.x, -node.pos.y) * GRID_SIZE) + (Point(SCREEN_WIDTH, SCREEN_HEIGHT) / 2)


def screen_pos_to_point(screen_pos: Point) -> Point:
    screen_pos.x += GRID_SIZE // 2
    screen_pos.y += GRID_SIZE // 2

    offset = Point(GRID_GEOMETRY[0] // 2, GRID_GEOMETRY[1] // 2)

    point_y_inverted = (screen_pos // GRID_SIZE) - offset
    return Point(point_y_inverted.x, -point_y_inverted.y)


if __name__ == '__main__':
    engine = Engine()
    engine.loop()
