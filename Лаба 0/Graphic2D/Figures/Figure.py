import pygame
from Graphic2D.Descriptors import IntegerDataDescriptor
from Graphic2D.Descriptors import ColorDataDescriptor
from Graphic2D.Descriptors import SurfaceDataDescriptor
from Graphic2D.Colors import *

# Основной класс фигуры
class Figure:
    # Набор параметров характеризующих местоположение фигуры
    x = IntegerDataDescriptor()
    y = IntegerDataDescriptor()
    # Набор пораметров характеризующих размер фигуры
    w = IntegerDataDescriptor()
    h = IntegerDataDescriptor()
    # Плоскость отрисовки фигуры
    surf = SurfaceDataDescriptor()
    # Цвет
    color = ColorDataDescriptor()

    # Инициализатор фигуры
    def __init__(self, surf, color, x, y, w, h):
        self.surf, self.color, self.x, self.y, self.w, self.h = surf, color, x, y, w, h

    # Метод отрисовки фугуры (попадает под переопределение)
    def draw(self):
        pass

    # Метод отрисовки выделения фигуры
    def draw_highlight(self):
        pygame.draw.line(self.surf,
                         HIGHLIGHTING,
                         (self._x, self._y),
                         (self._x + self._w, self._y),
                         HIGHLIGHTING_WIDTH)
        pygame.draw.line(self.surf,
                         HIGHLIGHTING,
                         (self._x + self._w, self._y),
                         (self._x + self._w, self._y + self._h),
                         HIGHLIGHTING_WIDTH)
        pygame.draw.line(self.surf,
                         HIGHLIGHTING,
                         (self._x + self._w, self._y + self._h),
                         (self._x, self._y + self._h),
                         HIGHLIGHTING_WIDTH)
        pygame.draw.line(self.surf,
                         HIGHLIGHTING,
                         (self._x, self._y + self._h),
                         (self._x, self._y),
                         HIGHLIGHTING_WIDTH)

    # Принадлежность точки фигуре
    def in_fig(self, x, y):
        return self.x <= x <= self.x + self.w and \
               self.y <= y <= self.y + self.h

    # Метод перемещения фигуры на плоскости
    def shift(self, x_shift, y_shift):
        self.x += x_shift
        self.y += y_shift

    # Метод изменения размеров фигуры
    def scale(self, w_scale, h_scale):
        if (self.w + w_scale > 0 and self.h + h_scale > 0):
            self.w += w_scale
            self.h += h_scale

    @staticmethod
    def display():
        pygame.display.flip()

    @staticmethod
    def _cyb2p_(x, p1, p2):
        return ((x - p1[0]) * (p2[1] - p1[1])) / (p2[0] - p1[0]) + p1[1]

    @staticmethod
    def _fyb4p_(p1, p2, p3, p4):
        kx12 = p2[0] - p1[0]
        ky12 = p2[1] - p1[1]
        kx34 = p4[0] - p3[0]
        ky34 = p4[1] - p3[1]
        return ((p3[0] - p1[0]) * ky12 * ky34 - p3[1] * kx34 * ky12 + p1[1] * kx12 * ky34) / (kx12 * ky34 - kx34 * ky12)