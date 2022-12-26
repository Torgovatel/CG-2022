"""
Класс Matrix - для реализации афинных преобразований модели
"""
from Descriptors import IntegerDataDescriptor
from Point import Point

class Matrix:
    # Конструктор матрицы
    def __init__(self, n):
        self.n = IntegerDataDescriptor()
        self.n = n
        self.buf = [[0 for _ in range(n)] for _ in range(n)]

    # Переопределение оператора []
    def __getitem__(self, item):
        return self.buf[item]

    # Переопределение оператора []
    def __setitem__(self, key, value):
        self.buf[key] = value

    # Переорпделение оператора +
    def __add__(self, other):
        if not(type(other) == Matrix):
            raise TypeError("Invalid argument")
        if other.n != self.n:
            raise ValueError("Invalid size")
        res = Matrix(self.n)
        for i in range(self.n):
            for j in range(self.n):
                res.buf[i][j] = self.buf[i][j] + other.buf[i][j]
        return res

    def __neg__(self, other):
        for i in range(self.n):
            for j in range(self.n):
                self.buf[i][j] = -self.buf[i][j]

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if issubclass(type(other), Matrix):
            # Для матриц одинакового размера!!!
            if other.n != self.n:
                raise ValueError("Invalid size")
            res = Matrix(self.n)
            for i in range(self.n):
                for j in range(self.n):
                    for k in range(self.n):
                        res[i][j] += self.buf[i][k] * other.buf[k][j]
            return res
        elif type(other) == list or type(other) == tuple:
            # Для Vertices of points NxM
            if self.n != 3:
                raise ValueError("Invalid size")
            res = [Point(0, 0, 0) for _ in range(len(other))]
            for i in range(len(other)):
                for j in range(3):
                    for k in range(3):
                        res[i][j] += self.buf[j][k] * other[i][k]
            return res
        else:
            raise TypeError("Invalid type")

    def __str__(self):
        return self.buf.__str__()

    def __repr__(self):
        return self.__str__()