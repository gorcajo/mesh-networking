from __future__ import annotations
import math


class Point:

    @classmethod
    def from_polar(cls, modulus: float, angle: float) -> Point:
        x = modulus * math.cos(angle)
        y = modulus * math.sin(angle)
        return Point(x, y)


    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


    def distance_to(self, other: Point) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


    @property
    def modulus(self)-> float:
        return math.hypot(self.x, self.y)


    @property
    def angle(self)-> float:
        return math.atan2(self.y, self.x)


    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)


    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)


    def __mul__(self, other: int) -> Point:
        return Point(self.x * other, self.y * other)


    def __truediv__(self, other: int) -> Point:
        return Point(int(self.x / other), int(self.y / other))


    def __str__(self) -> str:
        return f'Point({self.x}, {self.y})'
