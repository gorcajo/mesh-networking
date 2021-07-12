from __future__ import annotations
import logging
from typing import List


class Node:

    def __init__(self, node_id: int, pos: Point, power: int, online: bool, medium: Medium, node_count: int) -> None:
        self.id = node_id
        self.pos = pos
        self.power = power
        self.online = online
        self.medium = medium
        self.node_count = node_count

        self.input_queue: List[Message] = []
        self.output_queue: List[Message] = []


    def receive_message(self, message: Message) -> None:
        if self.online:
            self.input_queue.append(message)
            logging.info(f'{self} received {message}')


    def process_next_message(self) -> None:
        if self.online and len(self.input_queue) > 0:
            message = self.input_queue.pop(0)
            self.process_message(message)


    def dispatch_message(self, message: Message) -> None:
        self.output_queue.append(message)


    def emit_next_message(self) -> None:
        if self.online and len(self.output_queue) > 0:
            message = self.output_queue.pop(0)
            self.medium.propagate_message(message, self)
            logging.debug(f'{self} emitted {message}')


    def create_message(self) -> None:
        raise NotImplementedError()


    def process_message(self, message: Message) -> None:
        raise NotImplementedError()


    def __str__(self) -> str:
        return f'Node(id={self.id})'


class FloodingNode(Node):

    def __init__(self, node_id: int, pos: Point, power: int, online: bool, medium: Medium, node_count: int) -> None:
        super().__init__(node_id, pos, power, online, medium, node_count)

        self.next_message_id = 0

        self.consumed_message_ids: List[int] = []
        self.relayed_message_ids: List[int] = []


    def create_message(self) -> None:
        destination_id = self.node_count - 1
        message = FloodingMessage(message_id=self.next_message_id, destination_id=destination_id, payload='test')
        self.receive_message(message)
        self.next_message_id += 1


    def process_message(self, message: Message) -> None:
        if message.id in self.relayed_message_ids:
            logging.debug(f'{self} ignoring already relayed {message}')
        elif message.id in self.consumed_message_ids:
            logging.debug(f'{self} ignoring already consumed {message}')
        elif message.destination_id == self.id:
            logging.info(f'{message} reached final destination')
            self.consumed_message_ids.append(message.id)
        else:
            logging.debug(f'{self} relaying {message}')
            self.dispatch_message(message)
            self.relayed_message_ids.append(message.id)

        logging.debug(f'{self} processed {message}')


class RoutingNode(Node):

    def __init__(self, node_id: int, pos: Point, power: int, online: bool, medium: Medium, node_count: int) -> None:
        super().__init__(node_id, pos, power, online, medium, node_count)


    def create_message(self) -> None:
        pass # TODO


    def process_message(self, message: Message) -> None:
        pass # TODO


from medium import Medium
from message import Message, FloodingMessage, RoutingMessage
from point import Point