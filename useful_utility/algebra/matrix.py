from typing import override

import numpy as np

from useful_utility.errors import ArgumentError, MathError, ArgumentCodes, assertion, MathCodes
from useful_utility.algebra.statics import rnd

def add_matrix(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]

def sub_matrix(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A))] for i in range(len(A))]

def strassen_multiply(A, B):
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    mid = n // 2
    A11 = [[A[i][j] for j in range(mid)] for i in range(mid)]
    A12 = [[A[i][j] for j in range(mid, n)] for i in range(mid)]
    A21 = [[A[i][j] for j in range(mid)] for i in range(mid, n)]
    A22 = [[A[i][j] for j in range(mid, n)] for i in range(mid, n)]

    B11 = [[B[i][j] for j in range(mid)] for i in range(mid)]
    B12 = [[B[i][j] for j in range(mid, n)] for i in range(mid)]
    B21 = [[B[i][j] for j in range(mid)] for i in range(mid, n)]
    B22 = [[B[i][j] for j in range(mid, n)] for i in range(mid, n)]

    M1 = strassen_multiply(add_matrix(A11, A22), add_matrix(B11, B22))
    M2 = strassen_multiply(add_matrix(A21, A22), B11)
    M3 = strassen_multiply(A11, sub_matrix(B12, B22))
    M4 = strassen_multiply(A22, sub_matrix(B21, B11))
    M5 = strassen_multiply(add_matrix(A11, A12), B22)
    M6 = strassen_multiply(sub_matrix(A21, A11), add_matrix(B11, B12))
    M7 = strassen_multiply(sub_matrix(A12, A22), add_matrix(B21, B22))

    C11 = add_matrix(sub_matrix(add_matrix(M1, M4), M5), M7)
    C12 = add_matrix(M3, M5)
    C21 = add_matrix(M2, M4)
    C22 = add_matrix(sub_matrix(add_matrix(M1, M3), M2), M6)

    C = [[0] * n for _ in range(n)]
    for i in range(mid):
        for j in range(mid):
            C[i][j] = C11[i][j]
            C[i][j + mid] = C12[i][j]
            C[i + mid][j] = C21[i][j]
            C[i + mid][j + mid] = C22[i][j]

    return C

def matrix_multiply_opt(A, B):
    m, n = len(A), len(A[0])
    p = len(B[0])
    C = [[0] * p for _ in range(m)]

    for i in range(m):
        for k in range(n):  # Äußere Schleife über `k` verbessert den Cache-Zugriff
            for j in range(p):
                C[i][j] += A[i][k] * B[k][j]

    return C


class Matrix:
    def __init__(self, columns: int = 2, rows: int = 2, data: list = None):
        default_data: bool = False
        if data is None:
            data = np.zeros(shape=(2, 2))
            default_data = True
        assertion.assert_type(rows, int, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_type(columns, int, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_types(data, (list, np.ndarray), ArgumentError, code=ArgumentCodes.NOT_LIST_NP_ARRAY)
        assertion.assert_is_positiv(rows, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        assertion.assert_is_positiv(columns, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        assertion.assert_not_zero(columns, ArgumentError, code=ArgumentCodes.ZERO)
        assertion.assert_not_zero(rows, ArgumentError, code=ArgumentCodes.ZERO)
        if len(data) > 0:
            assertion.assert_layer_list(data, assertion.assert_types,
                                        {"types": (int, float, list, np.ndarray)}, ArgumentError,
                                        code=ArgumentCodes.LIST_LAYER_NOT_INT_FLOAT_LIST_ND_ARRAY)
        if len(data) > 0 and (isinstance(data[0], list) or isinstance(data[0], np.ndarray)):
            for d in data:
                assertion.assert_types(d, (list, np.ndarray), ArgumentError,
                                       code=ArgumentCodes.NOT_LIST_NP_ARRAY)
                assertion.assert_layer_list(d, assertion.assert_types,
                                            {"types": (int, float)}, ArgumentError,
                                            code=ArgumentCodes.LIST_LAYER_NOT_INT_FLOAT)
        if len(data) > 0 and (isinstance(data[0], int) or isinstance(data[0], float)):
            for d in data:
                assertion.assert_types(d, (int, float), ArgumentError,
                                       code=ArgumentCodes.NOT_INT_FLOAT)

        self._rows: int = rows
        self._columns: int = columns

        if not default_data and rows == 2:
            self._rows: int = len(data[0])
        elif not default_data and len(data) > 0 and rows != len(data[0]):
            self._rows: int = len(data[0])
        elif not default_data and len(data) == 0:
            self._rows: int = 0
        if not default_data and columns == 2:
            self._columns: int = len(data)
        elif not default_data and columns != len(data):
            self._columns: int = len(data)

        self._data = np.array(data)
        if default_data and (rows != 2 or columns != 2):
            self._data = np.zeros(shape=(self._columns, self._rows))

    def get_rows(self) -> int:
        return self._rows

    def get_columns(self) -> int:
        return self._columns

    def get_dimension(self) -> tuple:
        return self._columns, self._rows

    def get_component(self, column: int, row: int) -> float:
        assertion.assert_range(column, 0, len(self._data) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        assertion.assert_range(row, 0, len(self._data[column]) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        return float(self._data[column][row])

    def set_component(self, column: int, row: int, value: int | float | np.float64) -> None:
        assertion.assert_range(column, 0, len(self._data) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        assertion.assert_range(row, 0, len(self._data[column]) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        self._data[column][row] = value

    def get_components(self) -> np.ndarray:
        return self._data.copy()

    def set_components(self, data: list | np.ndarray) -> None:
        assertion.assert_types(data, (list, tuple, np.ndarray), ArgumentError,
                               code=ArgumentCodes.NOT_LIST_NP_ARRAY)
        if len(data) > 0:
            assertion.assert_layer_list(data, assertion.assert_types,
                                        {"types": (int, float, list, np.ndarray)}, ArgumentError,
                                        code=ArgumentCodes.LIST_LAYER_NOT_INT_FLOAT_LIST_ND_ARRAY)
        if len(data) > 0 and (isinstance(data[0], list) or isinstance(data[0], np.ndarray)):
            for d in data:
                assertion.assert_types(d, (list, np.ndarray), ArgumentError,
                                       code=ArgumentCodes.NOT_LIST_NP_ARRAY)
                assertion.assert_layer_list(d, assertion.assert_types,
                                            {"types": (int, float)}, ArgumentError,
                                            code=ArgumentCodes.LIST_LAYER_NOT_INT_FLOAT)
        if len(data) > 0 and (isinstance(data[0], int) or isinstance(data[0], float)):
            for d in data:
                assertion.assert_types(d, (int, float), ArgumentError,
                                       code=ArgumentCodes.NOT_INT_FLOAT)
        if len(data) != self._columns:
            self._columns = len(data)
        if len(data) > 0 and len(data[0]) != self._rows:
            self._rows = len(data[0])
        elif len(data[0]) == 0:
            self._rows = 0
        self._data = np.array(data)

    def copy(self):
        return Matrix(data=list(self.get_components()))

    def __eq__(self, other):
        if isinstance(other, Matrix):
            if self.get_rows() != other.get_rows() and self.get_columns() != other.get_columns():
                return False
            bools = self.get_components() == other.get_components()
            fin = list()
            for column in bools:
                fin.append(all(column))
            return all(fin)
        elif isinstance(other, np.ndarray):
            if self.get_components().shape != other.shape:
                return False
            bools = self.get_components() == other
            fin = list()
            for column in bools:
                fin.append(all(column))
            return all(fin)
        raise ArgumentError(ArgumentCodes.NOT_MATRIX_NP_ARRAY, msg="Only matrices or np.ndarray can be compared.", wrong_argument=type(other))

    def __add__(self, other) -> "Matrix":
        assertion.assert_type(other, Matrix, MathError, code=MathCodes.NOT_MATRIX,
                              msg="Only a matrix can be added to a matrix.")
        if self.get_dimension() != other.get_dimension():
            raise MathError(MathCodes.UNFIT_DIMENSIONS, "The dimensions of the matrices do not fit!", other)
        matrixA = self.get_components()
        matrixB = other.get_components()
        return Matrix(self._columns, self._rows, data=list(matrixA + matrixB))

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        assertion.assert_type(other, Matrix, MathError, code=MathCodes.NOT_MATRIX,
                              msg="Only a matrix can be added to a matrix.")
        if self.get_dimension() != other.get_dimension():
            raise MathError(MathCodes.UNFIT_DIMENSIONS, "The dimensions of the matrices do not fit!", other)
        temp: Matrix = self + other
        self.set_components(temp.get_components())
        return self

    def __sub__(self, other):
        assertion.assert_type(other, Matrix, MathError, code=MathCodes.NOT_MATRIX,
                              msg="Only a matrix can be subtracted to a matrix.")
        if self.get_dimension() != other.get_dimension():
            raise MathError(MathCodes.UNFIT_DIMENSIONS, "The dimensions of the matrices do not fit!", other)
        matrixA = self.get_components()
        matrixB = other.get_components()
        return Matrix(self._columns, self._rows, data=list(matrixA - matrixB))

    def __rsub__(self, other):
        return self.__sub__(other)

    def __isub__(self, other):
        temp: Matrix = self - other
        self.set_components(temp.get_components())
        return self

    def __mul__(self, other):
        assertion.assert_types(other, (Matrix, int, float), MathError, code=MathCodes.NOT_MATRIX_INT_FLOAT,
                               msg="Only matrices, int, float can be multiplied to a matrix.")
        multiplied: Matrix = Matrix()

        if isinstance(other, Matrix):
            assertion.assert_equals(self.get_rows(), other.get_columns(), MathError,
                                    code=MathCodes.UNFIT_DIMENSIONS,
                                    msg="Rows of self do not equal columns of other.")

            a: list = list(self.get_components())
            b: list = list(other.get_components())
            c: list = list()
            if self._rows == self._columns:
                c: list = strassen_multiply(a, b)
            else:
                c: list = matrix_multiply_opt(a, b)
            multiplied.set_components(c)

        if isinstance(other, int) or isinstance(other, float):
            temp: list = list()
            if self._rows > 1:
                for column_index, column in enumerate(self._data):
                    temp.append(list())
                    for component in self._data[column_index]:
                        temp.append(component * other)
            else:
                for component in self._data:
                    temp.append(component * other)
            multiplied.set_components(temp)
        return multiplied

    def __rmul__(self, other):
        assertion.assert_types(other, (Matrix, int, float), MathError, code=MathCodes.NOT_MATRIX_INT_FLOAT,
                               msg="Only matrices, int, float can be multiplied to a matrix.")
        multiplied: Matrix = Matrix()

        if isinstance(other, Matrix):
            assertion.assert_equals(other.get_rows(), self.get_columns(), MathError,
                                    code=MathCodes.UNFIT_DIMENSIONS,
                                    msg="Rows of self do not equal columns of other.")

            b: list = list(self.get_components())
            a: list = list(other.get_components())
            c: list = list()
            if self._rows == self._columns:
                c: list = strassen_multiply(a, b)
            else:
                c: list = matrix_multiply_opt(a, b)
            multiplied.set_components(c)

        if isinstance(other, int) or isinstance(other, float):
            temp: list = list()
            if self._rows > 1:
                for column_index, column in enumerate(self._data):
                    temp.append(list())
                    for component in self._data[column_index]:
                        temp.append(component * other)
            else:
                for component in self._data:
                    temp.append(component * other)
            multiplied.set_components(temp)
        return multiplied

    def __imul__(self, other):
        assertion.assert_types(other, (Matrix, int, float), MathError, code=MathCodes.NOT_MATRIX_INT_FLOAT,
                               msg="Only matrices, int, float can be multiplied to a matrix.")

        if isinstance(other, Matrix):
            multiplied: Matrix = self * other
            self.set_components(multiplied.get_components())

        if isinstance(other, int) or isinstance(other, float):
            multiplied: Matrix = self * other
            self.set_components(multiplied.get_components())
        return self

    def __truediv__(self, other):
        assertion.assert_types(other, (int, float), MathError,
                               code=MathCodes.NOT_INT_FLOAT)
        return self * (1/other)

    def __idiv__(self, other):
        assertion.assert_types(other, (int, float), MathError,
                               code=MathCodes.NOT_INT_FLOAT)
        dived: Matrix = self / other
        self.set_components(dived.get_components())
        return self

    def __pow__(self, power, modulo=None):
        assertion.assert_false(modulo, MathCodes, code=MathCodes.NOT_FALSE, msg="Modulo not defined.")
        assertion.assert_is_positiv(power, MathError, code=MathCodes.NOT_POSITIV)
        assertion.assert_type(power, int, MathError, code=MathCodes.NOT_INT)
        multiplied: Matrix = self.copy()
        for _ in range(power):
            multiplied *= self
        return multiplied

    def __ipow__(self, other):
        multiplied: Matrix = self ** other
        self.set_components(multiplied.get_components())
        return self
