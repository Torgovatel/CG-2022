from Matrix import Matrix
from Model2D import Model2D

class Model3D(Model2D):
    poligonal = 0
    carcas = 1
    def __init__(self, type, point_list, arc_matrix):
        super().__init__(point_list, arc_matrix)
        self.type = type
