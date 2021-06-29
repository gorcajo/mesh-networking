from __future__ import annotations
import math


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
