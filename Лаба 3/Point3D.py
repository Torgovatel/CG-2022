"""
Point3D - класс точки для модели, заданной в однородных мировых координатах
"""

from Descriptors import IntegerDataDescriptor
from Point2D import Point2D

class Point3D(Point2D):
    # Инициализатор точки
    # x, y, z - мировые координаты точки
    # k - коэффициент однородности
    def __init__(self, x, y, z, k=1):
        super().__init__(x, y, k)
        self.z = IntegerDataDescriptor()
        self.z = z

    def __len__(self):
        return 4

    # Приведение к декартовым координатам
    def decart_coords(self):
        return self.x / self.k, self.y / self.k, self.z / self.k

    # Переопределение оператора []
    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        elif item == 3:
            return self.k
        else:
            raise ValueError("Invalid argument")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        elif key == 3:
            self.k = value
        else:
            raise ValueError("Invalid argument")

    # Пользовательское строковое представление
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z}, {self.k})"

    def __repr__(self):
        return self.__str__()
