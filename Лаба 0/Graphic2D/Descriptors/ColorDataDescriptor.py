from Graphic2D.Colors import Colors


class ColorDataDescriptor:
    """Вспомогательный класс для обработки protected атрибутов типа Color"""
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = None
        if type(value) == tuple:
            instance.__dict__[self.name] = Colors.BASE_FIGURE_COLOR
        if type(value) == tuple and len(value) == 3 and all(map(lambda x: 0 <= x <= 255, value)):
            instance.__dict__[self.name] = self._color = value
