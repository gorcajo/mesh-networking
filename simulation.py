import logging

import yaml


NODES_DEFINITION = yaml.safe_load(open('nodes.yml', 'r'))


class Simulation:

    def __init__(self) -> None:
        self.step = 0

        self.medium = Medium()

        for node in NODES_DEFINITION:
            node_id = node['id']
            node_pos = Point(node['pos']['x'], node['pos']['y'])
            node_power = node['power']
            node_type = node['type']

            if node_type == 'flooding':
                self.medium.add_node(FloodingNode(node_id, node_pos, node_power, self.medium, len(NODES_DEFINITION)))
            elif node_type == 'routing':
                self.medium.add_node(RoutingNode(node_id, node_pos, node_power, self.medium, len(NODES_DEFINITION)))
            else:
                raise ValueError()


    def inject_new_message(self) -> None:
        self.medium.find_node_by_id(0).create_message()


    def run_step(self) -> None:
        logging.info(f'Running step #{self.step} ----------------------------------------------------------------')

        for node in self.medium.nodes:
            node.process_next_message()

        for node in self.medium.nodes:
            node.emit_next_message()

        self.step += 1


from medium import Medium
from node import FloodingNode, RoutingNode
from point import Point
