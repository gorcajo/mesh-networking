import logging

import yaml


NODES_DEFINITION = yaml.safe_load(open('nodes.yml', 'r'))


class Simulation:

    def __init__(self) -> None:
        self.next_message_id = 0
        self.step = 0

        self.medium = Medium()

        for node in NODES_DEFINITION:
            self.medium.add_node(
                Node(
                    node['id'],
                    Point(node['pos']['x'], node['pos']['y']),
                    node['power']))


    def inject_new_message(self) -> None:
        message = Message(message_id=self.next_message_id, destination_id=4, payload='test')
        self.medium.find_node_by_id(0).receive_message(message)
        self.next_message_id += 1


    def run_step(self) -> None:
        logging.info(f'Running step #{self.step} ----------------------------------------------------------------')

        for node in self.medium.nodes:
            node.process_next_message(self.medium)

        for node in self.medium.nodes:
            node.emit_next_message(self.medium)

        self.step += 1


from model.medium import Medium
from model.message import Message
from model.node import Node
from model.point import Point
