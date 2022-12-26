from Model2D import Model2D
from Scene2D import Scene2D
from Model3D import Model3D

class Scene3D(Scene2D):
    def __init__(self, cam, model_list):
        super().__init__(cam, model_list)

    def append(self, model):
        if type(model) == Model3D:
            self.buf.append(model)

    def render(self):
        self.cam.clear_work_space()
        for model in self.buf:
            self.cam.plot_model(model)
        self.cam.display()