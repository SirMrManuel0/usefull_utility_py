import math
from dis import code_info
from typing import override

import numpy as np

from useful_utility.useful_exception import ArgumentError

def rnd(x: float) -> float:
    return float(np.round(x, 8))

class Vector:
    def __init__(self, coords: tuple | list) -> None:
        if coords is None or len(coords) == 0:
            raise ArgumentError(wrong_argument=coords, correct_argument=[0, 0])
        if True in {not isinstance(i, (int, float)) for i in coords}:
            raise ArgumentError(wrong_argument=coords, correct_argument=[0, 0])
        self.__coordinates = list(coords)

    def get_coordinates(self) -> tuple:
        return tuple(self.__coordinates)

    def get_coordinate(self, index: int) -> float:
        if index is None:
            raise ArgumentError(wrong_argument=index, correct_argument=0)
        if index < 0 or index >= len(self.__coordinates):
            raise ArgumentError(wrong_argument=index, correct_argument=0)
        return self.__coordinates[index]

    def get_dimension(self) -> int:
        return len(self.__coordinates)

    def set_coordinates(self, coords: tuple | list) -> None:
        if coords is None or len(coords) == 0:
            raise ArgumentError(wrong_argument=coords, correct_argument=[0, 0])
        if True in {not isinstance(i, (int, float)) for i in coords}:
            raise ArgumentError(wrong_argument=coords, correct_argument=[0, 0])
        self.__coordinates = list(coords)

    def set_coordinate_at(self, index: int, coordinate: int | float) -> None:
        if index is None:
            raise ArgumentError(wrong_argument=index, correct_argument=0)
        if coordinate is None:
            raise ArgumentError(wrong_argument=coordinate, correct_argument=5)
        if index < 0 or index >= len(self.__coordinates):
            raise ArgumentError(wrong_argument=index, correct_argument=0)
        self.__coordinates[index] = coordinate

    #def get_complex(self) -> complex:
    #    return complex(self.__x, self.__y)

    def length(self) -> float:
        count: float = 0
        for coordinate in self.__coordinates:
            count += coordinate * coordinate
        count: float = rnd(count ** (1/self.get_dimension()))
        return count

    #def angle(self, vec2: "Vector") -> float:
    #    dot: float = self * vec2
    #    length_self: float = self.length()
    #    length_vec2: float = vec2.length()
    #    angle: float = rnd(dot / (length_self * length_vec2))
    #    return math.acos(angle)

    # Dunder Methods
    def __copy__(self) -> "Vector":
        return Vector(self.__coordinates)

    def __add__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            raise TypeError("Operands must be of type Vector")
        while self.get_dimension() < other.get_dimension():
            self.__coordinates.append(0)
        new: list = [i for i in self.__coordinates]
        other_coordinates: tuple = other.get_coordinates()
        for index, coordinate in enumerate(other_coordinates):
            new[index] += coordinate
        return Vector(new)

    def __iadd__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            raise TypeError("Operands must be of type Vector")
        temp: Vector = self + other
        self.__coordinates = list(temp.get_coordinates())
        return self

    def __sub__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            raise TypeError("Operands must be of type Vector")
        while self.get_dimension() < other.get_dimension():
            self.__coordinates.append(0)
        new: list = [i for i in self.__coordinates]
        other_coordinates: tuple = other.get_coordinates()
        for index, coordinate in enumerate(other_coordinates):
            new[index] -= coordinate
        return Vector(new)

    def __isub__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            raise TypeError("Operands must be of type Vector")
        temp: Vector = self - other
        self.__coordinates = list(temp.get_coordinates())
        return self

    def __mul__(self, other: int | float | "Vector") -> "Vector" | float:
        if isinstance(other, (int, float)):
            new: list = [rnd(i * other) for i in self.__coordinates]
            return Vector(new)
        elif isinstance(other, Vector):
            dot: float = 0
            other_coordinates: list = list(other.get_coordinates())
            while self.get_dimension() < len(other_coordinates):
                self.__coordinates.append(0)
            while len(other_coordinates) < self.get_dimension():
                other_coordinates.append(0)
            for index, coordinate in other_coordinates:
                dot += rnd(coordinate * self.__coordinates[index])
            return dot
        else:
            raise TypeError("The operand must be a scalar (int/float) or Vector")

    def __rmul__(self, scalar: float | int) -> "Vector":
        return self.__mul__(scalar)

    def __imul__(self, scalar: float | int) -> "Vector":
        if not isinstance(scalar, (int, float)):
            raise TypeError("Operand must be a scalar (int or float)")
        temp: Vector = self * scalar
        self.__coordinates = list(temp.get_coordinates())
        return self

    def __truediv__(self, scalar: float | int) -> "Vector":
        if not isinstance(scalar, (int, float)):
            raise TypeError("The divisor must be a scalar (int or float)")
        if scalar == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        return self * (1/scalar)

    def __itruediv__(self, scalar: float | int) -> "Vector":
        if not isinstance(scalar, (int, float)):
            raise TypeError("Operand must be a scalar (int or float)")
        if scalar == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        temp: Vector = self / scalar
        self.__coordinates = list(temp.get_coordinates())
        return self

    def __str__(self) -> str:
        return f"Vector coordinates = {self.__coordinates}"

class Vector2D(Vector):
    def __init__(self, x: float = 0, y: float = 0) -> None:
        super().__init__((x, y))

    @classmethod
    def from_vector(cls, vector: "Vector") -> "Vector2D":
        coordinates = vector.get_coordinates()
        x = coordinates[0] if len(coordinates) > 0 else 0
        y = coordinates[1] if len(coordinates) > 1 else 0
        return cls(x, y)

    def angle(self, vec2: "Vector2D") -> float:
        dot: float = self * vec2
        length_self: float = self.length()
        length_vec2: float = vec2.length()
        angle: float = rnd(dot / (length_self * length_vec2))
        return math.acos(angle)

    def get_complex(self) -> complex:
        return complex(self.get_coordinate(0), self.get_coordinate(1))

    def get_x(self) -> float:
        return self.get_coordinate(0)

    def get_y(self) -> float:
        return self.get_coordinate(1)

    def set_x(self, x: float) -> None:
        self.set_coordinate_at(0, x)

    def set_y(self, y: float) -> None:
        self.set_coordinate_at(1, y)

    # Dunder Methods
    @override
    def __copy__(self) -> "Vector":
        return Vector2D(self.get_x(), self.get_y())

    @override
    def __add__(self, other: "Vector" | complex) -> "Vector":
        if isinstance(other, complex):
            result: complex = self.get_complex() + other
            return Vector2D(result.real, result.imag)
        return super().__add__(other)

    def __radd__(self, other: "Vector" | complex) -> "Vector":
        return self.__add__(other)

    @override
    def __iadd__(self, other: "Vector" | complex) -> "Vector":
        if isinstance(other, complex):
            temp: Vector2D = Vector2D.from_vector(self + other)
            self.set_x(temp.get_x())
            self.set_y(temp.get_y())
            return self
        return super().__iadd__(other)

    @override
    def __sub__(self, other: "Vector" | complex) -> "Vector":
        if isinstance(other, complex):
            result: complex = self.get_complex() - other
            return Vector2D(result.real, result.imag)
        return super().__sub__(other)

    def __rsub__(self, other: "Vector" | complex) -> "Vector":
        return self.__sub__(other)

    @override
    def __isub__(self, other: "Vector" | complex) -> "Vector":
        if isinstance(other, complex):
            result: Vector = self - other
            self.set_x(result.get_coordinate(0))
            self.set_y(result.get_coordinate(1))
            return self
        return super().__isub__(other)

    @override
    def __mul__(self, other: complex | int | float | "Vector") -> "Vector" | float:
        if isinstance(other, complex):
            result: complex = self.get_complex() * other
            return Vector2D(result.real, result.imag)
        return super().__mul__(other)

    @override
    def __rmul__(self, other: complex | int | float | "Vector") -> "Vector":
        return self.__mul__(other)

    @override
    def __imul__(self, other: complex | int | float) -> "Vector":
        if isinstance(other, complex):
            result: Vector = self * other
            self.set_x(result.get_coordinate(0))
            self.set_y(result.get_coordinate(1))
            return self
        return super().__imul__(other)

    @override
    def __truediv__(self, other: float | int | complex) -> "Vector":
        if isinstance(other, complex):
            result: complex = self.get_complex() / other
            return Vector2D(result.real, result.imag)
        return super().__truediv__(other)

    @override
    def __itruediv__(self, other: float | int | complex) -> "Vector":
        if isinstance(other, complex):
            result: Vector = self * other
            self.set_x(result.get_coordinate(0))
            self.set_y(result.get_coordinate(1))
            return self
        return super().__itruediv__(other)

    @override
    def __str__(self) -> str:
        return f"Vector2D x = {self.get_x()}; y = {self.get_y()}; complex = {self.get_complex()}"
