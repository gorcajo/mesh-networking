from __future__ import annotations
import logging
from typing import List


class Node:

    def __init__(self, node_id: int, pos: Point, power: int, medium: Medium) -> None:
        self.id = node_id
        self.pos = pos
        self.power = power
        self.medium = medium

        self.input_queue: List[Message] = []
        self.output_queue: List[Message] = []


    def receive_message(self, message: Message) -> None:
        self.input_queue.append(message)
        logging.info(f'{self} received {message}')


    def create_message(self) -> None:
        raise NotImplementedError()


    def process_next_message(self) -> None:
        raise NotImplementedError()


    def emit_next_message(self) -> None:
        if len(self.output_queue) > 0:
            message = self.output_queue.pop(0)
            self.medium.propagate_message(message, self)
            logging.debug(f'{self} emitted {message}')


    def consume_message(self, message: Message) -> None:
        logging.debug(f'{self} consuming {message}')


    def __str__(self) -> str:
        return f'Node(id={self.id})'


class FloodingNode(Node):

    def __init__(self, node_id: int, pos: Point, power: int, medium: Medium) -> None:
        super().__init__(node_id, pos, power, medium)

        self.next_message_id = 0

        self.consumed_message_ids: List[int] = []
        self.relayed_message_ids: List[int] = []


    def create_message(self) -> None:
        self.receive_message(FloodingMessage(message_id=self.next_message_id, destination_id=4, payload='test'))
        self.next_message_id += 1


    def process_next_message(self) -> None:
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


class RoutingNode(Node):

    def __init__(self, node_id: int, pos: Point, power: int, medium: Medium) -> None:
        super().__init__(node_id, pos, power, medium)


    def create_message(self) -> None:
        pass # TODO


    def process_next_message(self) -> None:
        pass # TODO


from model.medium import Medium
from model.message import Message, FloodingMessage, RoutingMessage
from model.point import Point
