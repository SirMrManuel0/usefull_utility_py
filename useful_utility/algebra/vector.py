from typing import override, Self, Union

import numpy as np

from useful_utility.errors import ArgumentError, MathError, assertion
from useful_utility.errors import ArgumentCodes,  MathCodes, TODO, TypesTuple
from useful_utility.algebra.matrix import Matrix
from useful_utility.algebra.statics import rnd
from useful_utility.types import Number, Int, Lists


class Vector(Matrix):
    """
        The Vector-class inherits from the Matrix class. It is a simple n-dimensional vector.

        La classe Vecteur hérite de la classe Matrice. Il s'agit d'un simple vecteur à n dimensions.

        Methods:
            __init__(coordinates: list, dimension: int = 2):
                Initializes the vector with the given coordinates and dimension.

            cross(vec: Vector) -> Vector:
                Computes the cross product of the vector with another 3D vector.

            from_matrix(matrix: Matrix) -> Vector:
                Creates a vector from a single-row matrix.

            get_dimension() -> int:
                Returns the dimension of the vector.

            get_component(index: int) -> float:
                Returns the component at the specified index.

            set_component(index: int, value: int | float | np.float64) -> None:
                Sets the component at the specified index.

            set_data(new: list) -> None:
                Sets the vector data with the provided list.

            get_data() -> np.ndarray:
                Returns the vector's data as a NumPy array.

            length() -> float:
                Returns the magnitude (length) of the vector.

            __add__(other: Matrix) -> Vector:
                Adds another vector or matrix to the current vector.

            __radd__(other: Matrix) -> Vector:
                Right-hand addition for vectors or matrices.

            __sub__(other: Matrix) -> Vector:
                Subtracts another vector or matrix from the current vector.

            __rsub__(other: Matrix) -> Vector:
                Right-hand subtraction for vectors or matrices.

            __mul__(other: Vector | int | float) -> Vector | float:
                Multiplies the vector with another vector (dot product) or scalar.

            __rmul__(other: Matrix | Vector | int | float) -> Vector:
                Right-hand multiplication for vectors or scalars.

            __imul__(other: Matrix | int | float) -> Vector:
                In-place multiplication for vectors or scalars.

            __truediv__(other: int | float) -> Vector:
                Divides the vector by a scalar value.

            __pow__(power, modulo=None):
                Raises an error, as exponentiation is not defined for vectors.

            __str__() -> str:
                Returns a string representation of the vector.

            __repr__() -> str:
                Returns a detailed string representation of the vector.

            copy() -> Vector:
                Returns a copy of the vector.

            __iter__():
                Allows iteration over the vector components.

    """
    def __init__(self, coordinates=None, dimension: Int = 2):
        """
        Creates a vector.

        Crée un vecteur.

        Args:
            coordinates (list): A list of the coordinates for the vector.
            dimension (int): The dimension of the vector. (default 2; or len(coordinates))
        """
        assertion.assert_types(dimension, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_is_positiv(dimension, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        assertion.assert_not_zero(dimension, ArgumentError, code=ArgumentCodes.ZERO)
        d: list = list()
        if coordinates is None:
            coordinates: list = [0 for _ in range(dimension)]
        if isinstance(coordinates, tuple):
            coordinates = list(coordinates)
        assertion.assert_types(coordinates, TypesTuple.LISTS.value, ArgumentError,
                               code=ArgumentCodes.NOT_LISTS)
        for coord in coordinates:
            if isinstance(coord, TypesTuple.NUMBER.value):
                d.append([coord])
            elif isinstance(coord, TypesTuple.LISTS.value):
                d.append([coord[0]])
            else:
                raise ArgumentError(ArgumentCodes.UNEXPECTED_TYPE, wrong_argument=type(coord))
        super().__init__(d, dimension, 1)

    def cross(self, vec: Self) -> Self:
        """
            Computes the cross product of the vector with another 3D vector.

            Calcule le produit vectoriel de 2 vecteurs.

            Args:
                vec (Vector): The vector to compute the cross product with.

            Raises:
                ArgumentError: If `vec` is not of type Vector.
                MathError: If either vector does not have a dimension of 3.

            Returns:
                Vector: The resulting vector from the cross product.
        """
        assertion.assert_type(vec, Vector, ArgumentError, code=ArgumentCodes.NOT_VECTOR)
        assertion.assert_equals(vec.get_dimension(), 3, MathError, code=MathCodes.UNFIT_DIMENSIONS)
        assertion.assert_equals(self.get_dimension(), 3, MathError, code=MathCodes.UNFIT_DIMENSIONS)
        a, b, c = vec.get_data()
        d, e, f = self.get_data()
        return Vector([
            e * c - f * b,
            f * a - d * c,
            d * b - e * a
        ])

    @classmethod
    def from_matrix(cls, matrix: Matrix) -> Self:
        """
        Transforms a matrix into a vector.

        Transforme une matrice en un vecteur.

        Args:
            matrix (Matrix): The Matrix to transform into a vector.

        Raises:
            ArgumentError: If `matrix` is not of type Matrix.
            ArgumentError: If either matrix does not have 1 row.

        Returns:
            Vector: The resulting vector from the transformation.
        """
        assertion.assert_type(matrix, Matrix, ArgumentError, code=ArgumentCodes.NOT_MATRIX)
        assertion.assert_equals(matrix.get_rows(), 1, ArgumentError,
                                code=ArgumentCodes.MISMATCH_DIMENSION)
        coordinates: list = list()
        for component in matrix.get_components():
            coordinates.append(component[0])
        return Vector(coordinates, len(coordinates))

    @override
    def get_dimension(self) -> int:
        return len(self._data)

    @override
    def get_component(self, index: Int) -> float:
        assertion.assert_types(index, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_range(index, 0, self.get_dimension() - 1, ArgumentError,
                               code=ArgumentCodes.OUT_OF_RANGE)
        return float(self._data[index][0])

    @override
    def set_component(self, index: Int, value: Number) -> None:
        super().set_component(index, 1, value)

    def set_data(self, new: Lists) -> None:
        assertion.assert_types(new, TypesTuple.LISTS.value, ArgumentError,
                               code=ArgumentCodes.NOT_LISTS)
        assertion.assert_types_list(new, TypesTuple.NUMBER.value, ArgumentError, code=ArgumentCodes.NOT_NUMBER)
        new: list = list(new)
        to_data: list = list()
        for a in new:
            to_data.append([a])
        self._data = np.array(to_data)

    def get_data(self) -> np.ndarray:
        n: np.ndarray = self.get_components()
        n = n.reshape(self.get_dimension())
        return n

    def length(self) -> float:
        total: float = 0
        for entry in self._data:
            total += entry[0] * entry[0]
        return rnd(total ** (1/2))

    @override
    def __add__(self, other: Matrix) -> Self:
        added: Matrix = super().__add__(other)
        return Vector.from_matrix(added)

    @override
    def __radd__(self, other: Matrix) -> Self:
        added: Matrix = super().__radd__(other)
        return Vector.from_matrix(added)

    @override
    def __sub__(self, other: Matrix) -> Self:
        sub: Matrix = super().__sub__(other)
        return Vector.from_matrix(sub)

    @override
    def __rsub__(self, other: Matrix) -> Self:
        sub: Matrix = super().__rsub__(other)
        return Vector.from_matrix(sub)

    @override
    def __mul__(self, other: Union[Self, *TypesTuple.NUMBER.value]) -> Union[Self, float]:
        assertion.assert_types(other, (Vector, *TypesTuple.NUMBER.value), MathError, code=MathCodes.NOT_VECTOR_NUMBER)
        if isinstance(other, Vector):
            assertion.assert_equals(self.get_dimension(), other.get_dimension(), MathError,
                                    code=MathCodes.UNFIT_DIMENSIONS)
            a: np.ndarray = self.get_components()
            b: np.ndarray = other.get_components()
            c: np.ndarray = a * b
            d: float | int = 0
            if len(c) > 0 and isinstance(c[0], TypesTuple.LISTS.value):
                for sub in c:
                    d += sub[0]
            elif len(c) > 0 and isinstance(c[0], TypesTuple.NUMBER.value):
                print(c)
                for n in c:
                    d += n
            return rnd(d)
        vector: np.ndarray = self.get_data()
        return Vector(list(vector * other), self.get_dimension())

    @override
    def __rmul__(self, other: Union[Matrix, Self, *TypesTuple.NUMBER.value]) -> Self:
        if isinstance(other, (Vector, *TypesTuple.NUMBER.value)):
            return self * other
        multiple: Matrix = super().__rmul__(other)
        return Vector.from_matrix(multiple)

    @override
    def __imul__(self, other: Union[Matrix, *TypesTuple.NUMBER.value]) -> Self:
        if isinstance(other, Vector):
            raise MathError(MathCodes.VECTOR)
        return super().__imul__(other)

    @override
    def __truediv__(self, other: Number) -> Self:
        div: Matrix = super().__truediv__(other)
        return Vector.from_matrix(div)

    @override
    def __pow__(self, power, modulo=None):
        raise MathError(MathCodes.NOT_DEFINED, msg="This Action is not defined.")

    @override
    def __str__(self) -> str:
        return f"{self.get_data()}"

    @override
    def __repr__(self) -> str:
        return f"Vector at {hex(id(self))} with:\n {self.get_data()}"

    @override
    def copy(self) -> Self:
        return Vector.from_matrix(super().copy())

    @override
    def __iter__(self) -> iter:
        return iter(list(self.get_data()))
