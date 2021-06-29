from __future__ import annotations
import logging
from typing import List


class Node:

    def __init__(self, node_id: int, pos: Point, power: int) -> None:
        self.id: int = node_id
        self.pos: Point = pos
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


from model.medium import Medium
from model.message import Message
from model.point import Point
