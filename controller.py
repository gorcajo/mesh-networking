import math

import pygame

from model import Simulation, Medium, Node, Message, Position


SCREEN_GEOMETRY = (800, 600)

DISTANCE_UNIT_SIZE = 25

BACKGROUND_COLOR = (20, 20, 20)

AXIS_COLOR = (25, 25, 25)

NODE_SIZE = 4
NODE_COLOR = (255, 255, 255)
NODE_TEXT_COLOR = (40, 40, 40)
NODE_RANGE_COLOR = (40, 40, 0)

LINK_ARROW_HEAD_SIZE = 4
LINK_COLOR = (150, 150, 255)

FONT_FAMILY = 'monospace'
FONT_SIZE = 19


class Engine:

    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)

        self.screen = pygame.display.set_mode(SCREEN_GEOMETRY, 0, 32)
        pygame.display.set_caption('Network Viewer')

        self.running = False


    def loop(self) -> None:
        clock = pygame.time.Clock()
        self.running = True

        self.init()
        
        while self.running:
            self.update()
            self.draw()
            clock.tick(60)


    def init(self) -> None:
        self.simulation = Simulation()


    def update(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.simulation.run_step()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False


    def draw(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)

        self.draw_axis()

        for node in self.simulation.medium.nodes:
            self.draw_node_range(node)

        for node in self.simulation.medium.nodes:
            for other in self.simulation.medium.nodes:
                if node.pos.distance_to(other.pos) <= node.power:
                    self.draw_link(node.pos, other.pos)

        for node in self.simulation.medium.nodes:
            self.draw_node(node)

        pygame.display.update()
    

    def draw_axis(self) -> None:
        width = SCREEN_GEOMETRY[0]
        height = SCREEN_GEOMETRY[1]

        pygame.draw.line(self.screen, AXIS_COLOR, (0, height/2), (width, height/2))
        pygame.draw.line(self.screen, AXIS_COLOR, (width/2, 0), (width/2, height))

        for i in range(1, int(width/DISTANCE_UNIT_SIZE)):
            pygame.draw.line(
                self.screen,
                AXIS_COLOR,
                (DISTANCE_UNIT_SIZE * i, height/2 - 4),
                (DISTANCE_UNIT_SIZE * i, height/2 + 4))

        for i in range(1, int(width/DISTANCE_UNIT_SIZE)):
            pygame.draw.line(
                self.screen,
                AXIS_COLOR,
                (width/2 - 4, DISTANCE_UNIT_SIZE * i),
                (width/2 + 4, DISTANCE_UNIT_SIZE * i))


    def draw_node(self, node: Node) -> None:
        width = SCREEN_GEOMETRY[0]
        height = SCREEN_GEOMETRY[1]

        center = (Position(node.pos.x, -node.pos.y) * DISTANCE_UNIT_SIZE) + (Position(width, height) / 2)
        self.screen.blit(self.font.render(str(node.id), False, NODE_TEXT_COLOR), (center.x + 2, center.y + 2))


    def draw_node_range(self, node: Node) -> None:
        width = SCREEN_GEOMETRY[0]
        height = SCREEN_GEOMETRY[1]

        center = (Position(node.pos.x, -node.pos.y) * DISTANCE_UNIT_SIZE) + (Position(width, height) / 2)

        pygame.draw.circle(self.screen, NODE_RANGE_COLOR, (center.x, center.y), node.power * DISTANCE_UNIT_SIZE, 1)
        pygame.draw.circle(self.screen, NODE_COLOR, (center.x, center.y), NODE_SIZE)
        self.screen.blit(self.font.render(str(node.id), False, NODE_TEXT_COLOR), (center.x + 2, center.y + 2))


    def draw_link(self, from_pos: Position, to_pos: Position, arrow_head: bool = False) -> None:
        width = SCREEN_GEOMETRY[0]
        height = SCREEN_GEOMETRY[1]

        from_pos = (Position(from_pos.x, -from_pos.y) * DISTANCE_UNIT_SIZE) + (Position(width, height) / 2)
        to_pos = (Position(to_pos.x, -to_pos.y) * DISTANCE_UNIT_SIZE) + (Position(width, height) / 2)

        pygame.draw.line(self.screen, LINK_COLOR, (from_pos.x, from_pos.y), (to_pos.x, to_pos.y))

        if arrow_head:
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


if __name__ == '__main__':
    engine = Engine()
    engine.loop()
