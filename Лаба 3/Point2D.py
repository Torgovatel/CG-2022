"""
Point2D - класс точки для модели, заданной в однородных мировых координатах
"""

from Descriptors import IntegerDataDescriptor

class Point2D:
    # Инициализатор точки
    # x, y - мировые координаты точки
    # k - коэффициент однородности
    def __init__(self, x, y, k=1):
        self.x = IntegerDataDescriptor()
        self.y = IntegerDataDescriptor()
        self.k = IntegerDataDescriptor()
        self.x = x
        self.y = y
        self.k = k

    def __len__(self):
        return 3

    # Приведение к декартовым координатам
    def decart_coords(self):
        return self.x / self.k, self.y / self.k

    # Переопределение оператора []
    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.k
        else:
            raise ValueError("Invalid argument")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.k = value
        else:
            raise ValueError("Invalid argument")

    # Пользовательское строковое представление
    def __str__(self):
        return f"({self.x}, {self.y}, {self.k})"

    def __repr__(self):
        return self.__str__()
