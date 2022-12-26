class IntegerDataDescriptor:
    """Вспомогательный класс для обработки protected атрибутов типа Int"""
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = None
        if type(value) == int:
            instance.__dict__[self.name] = value
