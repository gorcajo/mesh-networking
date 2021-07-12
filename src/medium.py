from __future__ import annotations
from typing import List


class Medium:

    def __init__(self) -> None:
        self.nodes: List[Node] = []


    def add_node(self, new_node: Node) -> None:
        self.nodes.append(new_node)


    def propagate_message(self, message: Message, emitter: Node) -> None:
        receiving_nodes = self.get_nodes_in_range_of(emitter)

        for node in receiving_nodes:
            if node.id != emitter.id:
                node.receive_message(message.clone)


    def get_nodes_in_range_of(self, central_node: Node) -> List[Node]:
        for node in self.nodes:
            if node.pos.distance_to(central_node.pos) <= central_node.power:
                yield node


    def find_node_by_id(self, node_id: int) -> Node:
        for node in self.nodes:
            if node.id == node_id:
                return node

        return None


    def find_first_free_id(self) -> int:
        if len(self.nodes) <= 0:
            return 0

        node_ids = sorted([node.id for node in self.nodes])
        highest_id = max(node_ids)

        for i in range(highest_id + 1):
            if i != node_ids[i]:
                return i

        return highest_id + 1


    def get_highest_node_id(self) -> int:
        if len(self.nodes) <= 0:
            return 0

        return max([node.id for node in self.nodes])


from message import Message
from node import Node
