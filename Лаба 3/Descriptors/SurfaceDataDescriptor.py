import pygame


class SurfaceDataDescriptor:
    """Вспомогательный класс для обработки protected атрибутов типа pygame.Surface"""
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = None
        if type(value) == pygame.Surface:
            instance.__dict__[self.name] = value
