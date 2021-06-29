from __future__ import annotations
from typing import List


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


from model.message import Message
from model.node import Node
from model.position import Position
