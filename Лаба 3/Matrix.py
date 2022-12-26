"""
Класс Matrix - для реализации афинных преобразований модели
"""
from Descriptors import IntegerDataDescriptor
from Point2D import Point2D
from Point3D import Point3D

class Matrix:
    # Конструктор матрицы
    def __init__(self, n, m=None):
        if m is None:
            m = n
        self.m = IntegerDataDescriptor()
        self.n = IntegerDataDescriptor()
        self.n = n
        self.m = m
        self.buf = [[0 for _ in range(m)] for _ in range(n)]

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
        if other.n != self.n or other.m != self.m:
            raise ValueError("Invalid size")
        res = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                res.buf[i][j] = self.buf[i][j] + other.buf[i][j]
        return res

    def __neg__(self, other):
        res = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                res.buf[i][j] = -self.buf[i][j]
        return res

    def __sub__(self, other):
        return self + (-other)


    def __mulmatrix__(self, other):
        # Для матриц одинакового размера!!!
        if other.n != self.m:
            raise ValueError("Invalid size")
        res = Matrix(self.n, other.m)
        for i in range(self.n):
            for j in range(other.m):
                for k in range(self.m):
                    res[i][j] += self.buf[i][k] * other.buf[k][j]
        return res


    def __mulpoint__(self, other):
        if self.n == 3:
            res = Point2D(0, 0, 0)
        elif self.n == 4:
            res = Point3D(0, 0, 0, 0)
        for i in range(self.n):
            for k in range(self.m):
                res[i] += self.buf[i][k] * other[k]
        return res

    def __mulvector__(self, other):
        if len(other[0]) == 3:
            res = [Point2D(0, 0, 0) for _ in range(len(other))]
        elif len(other[0]) == 4:
            res = [Point3D(0, 0, 0, 0) for _ in range(len(other))]
        for i in range(len(other)):
            for j in range(len(other[0])):
                for k in range(len(other[0])):
                    res[i][j] += self.buf[j][k] * other[i][k]
        return res

    def __mul__(self, other):
        if issubclass(type(other), Matrix):
            return self.__mulmatrix__(other)
        elif issubclass(type(other), Point2D):
            return self.__mulpoint__(other)
        elif type(other) == list or type(other) == tuple:
            return self.__mulvector__(other)
        else:
            raise TypeError("Invalid type")

    def __str__(self):
        return self.buf.__str__()

    def __repr__(self):
        return self.__str__()