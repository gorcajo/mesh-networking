import logging

import yaml


class Simulation:

    def __init__(self) -> None:
        self.refresh()


    def refresh(self) -> None:
        self.step = 0

        self.medium = Medium()

        nodes_definition = yaml.safe_load(open('src/nodes.yml', 'r'))

        for node in nodes_definition:
            node_id = int(node['id'])
            node_pos = Point(int(node['pos']['x']), int(node['pos']['y']))
            node_power = int(node['power'])
            node_status = str(node['status'])
            node_type = str(node['type'])

            node_is_online: bool = None

            if node_status == 'online':
                node_is_online = True
            elif node_status == 'offline':
                node_is_online = False
            else:
                raise ValueError()

            if node_type == 'flooding':
                self.medium.add_node(FloodingNode(node_id, node_pos, node_power, node_is_online, self.medium, len(nodes_definition)))
            elif node_type == 'routing':
                self.medium.add_node(RoutingNode(node_id, node_pos, node_power, node_is_online, self.medium, len(nodes_definition)))
            else:
                raise ValueError()

        logging.info(f'Simulation initialized')


    def inject_new_message(self) -> None:
        self.medium.find_node_by_id(0).create_message()


    def run_step(self) -> None:
        logging.info(f'Running step #{self.step}')

        for node in self.medium.nodes:
            node.process_next_message()

        for node in self.medium.nodes:
            node.emit_next_message()

        self.step += 1


from medium import Medium
from node import FloodingNode, RoutingNode
from point import Point
