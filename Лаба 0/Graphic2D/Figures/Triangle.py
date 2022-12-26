import pygame
from Graphic2D.Figures.Figure import Figure
from math import floor
from math import ceil


class Triangle(Figure):
    def draw(self):
        p_top = (self._x + self._w // 2, self._y)
        p_left = (self._x, self._y + self._h)
        p_right = (self._x + self._w, self._y + self._h)
        for y in range(self._y, self._y + self._h + 1):
            for x in range(self._x, self._x + self._w + 1):
                if y >= ceil(Figure._cyb2p_(x, p_top, p_left)) and y >= floor(
                        Figure._cyb2p_(x, p_top, p_right)):
                    self._surf.set_at((x, y), self._color)