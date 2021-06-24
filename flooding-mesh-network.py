from __future__ import annotations
from enum import Enum
import math
from typing import List


class Medium:

    def __init__(self) -> None:
        self.nodes: List[Node] = []


    def add_node(self, new_node: Node) -> None:
        self.nodes.append(new_node)


    def propagate_message(self, message: Message, emitter_pos: Position, emitter_power: int) -> None:
        pass


    def get_nodes_in_range_of(self, pos: Position, range: int) -> List[Node]:
        pass


class Node:

    def __init__(self, node_id: int, pos: Position, power: int) -> None:
        self.id: int = node_id
        self.pos: Position = pos
        self.power: int = power
        self.input_queue: List[Message] = []
        self.output_queue: List[Message] = []


    def receive_message(self, message: Message) -> None:
        pass


    def process_next_message(self, message: Message) -> None:
        pass


    def emit_next_message(self, medium: Medium) -> None:
        pass


class Message:

    def __init__(self, message_id: int, ttl: int, destination_id: int, payload: str) -> None:
        self.message_id: int = message_id
        self.ttl: int = ttl
        self.destination_id: int = destination_id
        self.payload: str = payload


    def decrease_ttl(self) -> None:
        self.ttl -= 1


    @property
    def is_alive(self) -> bool:
        return self.ttl > 0


    @property
    def clone(self) -> Message:
        return Message(self.message_id, self.ttl, self.destination_id, self.payload)


class Position:

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y


    def distance_to(self, other: Position) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


def main() -> None:
    pass


if __name__ == '__main__':
    main()
