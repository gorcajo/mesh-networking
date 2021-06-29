import logging

import yaml


NODES_DEFINITION = yaml.safe_load(open('nodes.yml', 'r'))


class Simulation:

    def __init__(self) -> None:
        self.step = 0

        self.medium = Medium()

        for node in NODES_DEFINITION:
            self.medium.add_node(
                Node(
                    node['id'],
                    Position(node['pos']['x'], node['pos']['y']),
                    node['power']))


    def run_step(self) -> None:
        logging.info(f'Running step #{self.step} ----------------------------------------------------------------')

        if self.step == 0:
            message = Message(message_id=0, destination_id=4, payload='test')
            self.medium.find_node_by_id(0).receive_message(message)
        else:
            for node in self.medium.nodes:
                node.process_next_message(self.medium)

            for node in self.medium.nodes:
                node.emit_next_message(self.medium)

        self.step += 1


from model.medium import Medium
from model.message import Message
from model.node import Node
from model.position import Position
