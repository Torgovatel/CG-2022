import pygame
from Graphic2D.Figures.Figure import Figure


class Rect(Figure):
    def draw(self):
        pygame.draw.rect(self._surf, self._color, (self._x, self._y, self._w, self._h))