"""
Набор матриц задающих базовые афинные преобразования
"""

from Matrix import Matrix
from math import sin, cos
class Transfer(Matrix):
    def __init__(self, ax, ay):
        super().__init__(3)
        self.buf = [[1, 0, ax],
                    [0, 1, ay],
                    [0, 0, 1]]


class Rotation(Matrix):
    def __init__(self, fi):
        super().__init__(3)
        if type(fi) in [tuple, list]:
            # fi = (A, B)
            sn, cs = fi[1], fi[0]
            self.buf = [[cs, -sn, 0],
                        [sn, cs, 0],
                        [0, 0, 1]]
        else:
            self.buf = [[cos(fi), -sin(fi), 0],
                        [sin(fi), cos(fi), 0],
                        [0, 0, 1]]


class Scaling(Matrix):
    def __init__(self, kx, ky):
        super().__init__(3)
        self.buf = [[kx, 0, 0],
                    [0, ky, 0],
                    [0, 0, 1]]


class Mapping(Matrix):
    x = 0
    y = 1
    o = 2

    def __init__(self, flag):
        super().__init__(3)
        if flag == Mapping.x:
            self.buf = [[1, 0, 0],
                        [0, -1, 0],
                        [0, 0, 1]]
        elif flag == Mapping.y:
            self.buf = [[-1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 1]]
        elif flag == Mapping.o:
            self.buf = [[-1, 0, 0],
                        [0, -1, 0],
                        [0, 0, 1]]
