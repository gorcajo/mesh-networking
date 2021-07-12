from __future__ import annotations
import copy
from typing import List


class Message:

    def __init__(self, message_id: int, payload: str) -> None:
        self.id: int = message_id
        self.payload: str = payload


    @property
    def clone(self) -> Message:
        return copy.deepcopy(self)


    def __str__(self) -> str:
        return f'Message(id={self.id}, destination_id={self.destination_id}, payload={self.payload})'


class FloodingMessage(Message):

    def __init__(self, message_id: int, destination_id: int, payload: str) -> None:
        super().__init__(message_id, payload)
        self.destination_id: int = destination_id


class RoutingMessage(Message):

    def __init__(self, message_id: int, payload: str) -> None:
        super().__init__(message_id, payload)
        # TODO
