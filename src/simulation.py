from __future__ import annotations
import logging

import yaml


NODES_FILE = 'src/nodes.yml'


class Simulation:

    def __init__(self) -> None:
        self.previous_nodes_file_hash: str = None
        self.refresh()


    def get_nodes_file_hash(self) -> str:
        import hashlib

        BUF_SIZE = 65536

        sha1 = hashlib.sha1()

        with open(NODES_FILE, 'rb') as nodes_file:
            while data := nodes_file.read(BUF_SIZE):
                sha1.update(data)

        return sha1.hexdigest()


    def refresh_if_nodes_file_changed(self) -> None:
        if self.previous_nodes_file_hash != self.get_nodes_file_hash():
            self.refresh()


    def refresh(self) -> None:
        self.step = 0

        self.medium = Medium()

        nodes_definition = yaml.safe_load(open(NODES_FILE, 'r'))
        self.previous_nodes_file_hash = self.get_nodes_file_hash()

        network_type = nodes_definition[0]['type']

        self.NodeClass = None

        if network_type == 'flooding':
            self.NodeClass = FloodingNode
        elif network_type == 'routing':
            self.NodeClass = RoutingNode
        else:
            raise ValueError()

        for node in nodes_definition:
            if node['type'] != network_type:
                raise ValueError()

        for node in nodes_definition:
            node_id = int(node['id'])
            node_pos = Point(int(node['pos']['x']), int(node['pos']['y']))
            node_power = int(node['power'])
            node_status = str(node['status'])

            node_is_online: bool = None

            if node_status == 'online':
                node_is_online = True
            elif node_status == 'offline':
                node_is_online = False
            else:
                raise ValueError()

            self.medium.add_node(self.NodeClass(node_id, node_pos, node_power, node_is_online, self.medium))

        self.default_power = self.medium.find_node_by_id(0).power

        logging.info(f'Simulation initialized')


    def save(self) -> None:
        with open(NODES_FILE, 'w') as nodes_file:
            nodes_file.write(yaml.dump([node.to_dict() for node in self.medium.nodes]))
        logging.info(f'Nodes saved in "{NODES_FILE}"')


    def inject_new_message(self) -> None:
        self.medium.find_node_by_id(0).create_message()


    def run_step(self) -> None:
        logging.info(f'Running step #{self.step}')

        for node in self.medium.nodes:
            node.process_next_message()

        for node in self.medium.nodes:
            node.emit_next_message()

        self.step += 1


    def remove_node(self, node: Node) -> None:
        self.medium.nodes.remove(node)


    def create_node(self, pos: Point) -> None:
        node = self.NodeClass(
            self.medium.find_first_free_id(),
            pos,
            self.default_power,
            True,
            self.medium)

        self.medium.add_node(node)




from medium import Medium
from node import Node, FloodingNode, RoutingNode
from point import Point
