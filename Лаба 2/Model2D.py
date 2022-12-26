from Matrix import Matrix

class Model2D:
    def __init__(self, point_list, arc_matrix):
        self.buf = point_list[:]
        self.matrix = arc_matrix

    def append(self, point):
        self.buf.append(point)

    def __str__(self):
        return self.buf.__str__()

    def __repr__(self):
        return self.__str__()

    def apply(self, matrix):
        if issubclass(type(matrix), Matrix):
            self.buf = matrix * self.buf
