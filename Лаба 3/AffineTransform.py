"""
Набор матриц задающих базовые афинные преобразования
"""

from Matrix import Matrix
from math import sin, cos
class Transfer(Matrix):
    def __init__(self, ax, ay, az):
        super().__init__(4)
        self.buf = [[1, 0, 0, ax],
                    [0, 1, 0, ay],
                    [0, 0, 1, az],
                    [0, 0, 0, 1]]


class Rotation(Matrix):
    x = 0
    y = 1
    z = 2
    def __init__(self, flag, fi):
        super().__init__(4)
        sn, cs = 0, 0
        if type(fi) in [tuple, list]:
            # fi = (A, B)
            sn, cs = fi[1], fi[0]
        else:
            sn, cs = sin(fi), cos(fi)
        if flag == Rotation.x:
            self.buf = [[1, 0, 0, 0],
                        [0, cs, -sn, 0],
                        [0, sn, cs, 0],
                        [0, 0, 0, 1]]
        elif flag == Rotation.y:
            self.buf = [[cs, 0, sn, 0],
                        [0, 1, 0, 0],
                        [-sn, 0, cs, 0],
                        [0, 0, 0, 1]]
        elif flag == Rotation.z:
            self.buf = [[cs, -sn, 0, 0],
                        [sn, cs, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]]
        else:
            raise ValueError(r"Такой поворот не существует (выберите ось x/y/z)")


class Scaling(Matrix):
    def __init__(self, kx=1, ky=1, kz=1):
        super().__init__(4)
        self.buf = [[kx, 0, 0, 0],
                    [0, ky, 0, 0],
                    [0, 0, kz, 0],
                    [0, 0, 0, 1]]


class Mapping(Matrix):
    o = 0
    x = 1
    y = 2
    z = 3
    xy = 4
    xz = 5
    yz = 6

    def __init__(self, flag):
        super().__init__(4)
        if flag == Mapping.o:
            self.buf = [[-1, 0, 0, 0],
                        [0, -1, 0, 0],
                        [0, 0, -1, 0],
                        [0, 0, 0, 1]]
        elif flag == Mapping.x:
            self.buf = [[1, 0, 0, 0],
                        [0, -1, 0, 0],
                        [0, 0, -1, 0],
                        [0, 0, 0, 1]]
        elif flag == Mapping.y:
            self.buf = [[-1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, -1, 0],
                        [0, 0, 0, 1]]
        elif flag == Mapping.z:
            self.buf = [[-1, 0, 0, 0],
                        [0, -1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]]
        elif flag == Mapping.xy:
            self.buf = [[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, -1, 0],
                        [0, 0, 0, 1]]
        elif flag == Mapping.xz:
            self.buf = [[1, 0, 0, 0],
                        [0, -1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]]
        elif flag == Mapping.yz:
            self.buf = [[-1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]]
