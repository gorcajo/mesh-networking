from __future__ import annotations
from enum import Enum
import logging
import math
from typing import List

import yaml


logging.basicConfig(
    format  = '%(asctime)-5s.%(msecs)03d | %(levelname)-7s | %(message)s',
    level   = logging.INFO,
    datefmt = '%Y-%m-%d %H:%M:%S')


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


class Medium:

    def __init__(self) -> None:
        self.nodes: List[Node] = []


    def add_node(self, new_node: Node) -> None:
        self.nodes.append(new_node)


    def propagate_message(self, message: Message, emitter: Node) -> None:
        receiving_nodes = self.get_nodes_in_range_of(emitter.pos, emitter.power)

        for node in receiving_nodes:
            if node.id != emitter.id:
                node.receive_message(message)


    def get_nodes_in_range_of(self, pos: Position, range: int) -> List[Node]:
        for node in self.nodes:
            if node.pos.distance_to(pos) <= range:
                yield node


    def find_node_by_id(self, node_id: int) -> Node:
        for node in self.nodes:
            if node.id == node_id:
                return node

        return None


class Node:

    def __init__(self, node_id: int, pos: Position, power: int) -> None:
        self.id: int = node_id
        self.pos: Position = pos
        self.power: int = power

        self.input_queue: List[Message] = []
        self.output_queue: List[Message] = []

        self.consumed_message_ids: List[int] = []
        self.relayed_message_ids: List[int] = []


    def receive_message(self, message: Message) -> None:
        self.input_queue.append(message)
        logging.info(f'{self} received {message}')


    def process_next_message(self, message: Message) -> None:
        if len(self.input_queue) > 0:
            message = self.input_queue.pop(0)

            if message.id in self.relayed_message_ids:
                logging.debug(f'{self} ignoring already relayed {message}')
            elif message.id in self.consumed_message_ids:
                logging.debug(f'{self} ignoring already consumed {message}')
            elif message.destination_id == self.id:
                logging.info(f'{message} reached final destination')
                self.consume_message(message)
                self.consumed_message_ids.append(message.id)
            else:
                logging.debug(f'{self} relaying {message}')
                self.output_queue.append(message)
                self.relayed_message_ids.append(message.id)

            logging.debug(f'{self} processed {message}')


    def emit_next_message(self, medium: Medium) -> None:
        if len(self.output_queue) > 0:
            message = self.output_queue.pop(0)
            medium.propagate_message(message, self)
            logging.debug(f'{self} emitted {message}')


    def consume_message(self, message: Message) -> None:
        logging.debug(f'{self} consuming {message}')


    def __str__(self) -> str:
        return f'Node(id={self.id})'


class Message:

    def __init__(self, message_id: int, destination_id: int, payload: str) -> None:
        self.id: int = message_id
        self.destination_id: int = destination_id
        self.payload: str = payload


    @property
    def clone(self) -> Message:
        return Message(self.id, self.destination_id, self.payload)


    def __str__(self) -> str:
        return f'Message(id={self.id}, destination_id={self.destination_id}, payload={self.payload})'


class Position:

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y


    def distance_to(self, other: Position) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


    def __add__(self, other: Position) -> Position:
        return Position(self.x + other.x, self.y + other.y)


    def __sub__(self, other: Position) -> Position:
        return Position(self.x - other.x, self.y - other.y)


    def __mul__(self, other: int) -> Position:
        return Position(self.x * other, self.y * other)


    def __truediv__(self, other: int) -> Position:
        return Position(int(self.x / other), int(self.y / other))


    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

