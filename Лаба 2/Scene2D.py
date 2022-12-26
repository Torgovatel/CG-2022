from Model2D import Model2D

class Scene2D:
    def __init__(self, cam, model_list):
        if model_list is None or not(type(model_list) in (list, tuple)):
            model_list = []
        self.buf = model_list[:]
        self.cam = cam

    def append(self, model):
        if type(model) == Model2D:
            self.buf.append(model)

    def render(self):
        self.cam.clear_work_space()
        for model in self.buf:
            self.cam.plot_model(model)
        self.cam.plot_axes()
        self.cam.display()