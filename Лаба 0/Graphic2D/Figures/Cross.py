import pygame
from Graphic2D.Figures.Figure import Figure

CROSS_LINE_WIDTH = 10

class Cross(Figure):
    def draw(self):
        kx, ky = 0, 0
        if self._h > self._w:
            kx = CROSS_LINE_WIDTH // 2
        else:
            ky = CROSS_LINE_WIDTH // 2
        if self._h >= 2 * CROSS_LINE_WIDTH and self._w >= 2 * CROSS_LINE_WIDTH:
            pygame.draw.line(self._surf, self._color,
                             (self._x + kx, self._y + ky),
                             (self._x - kx + self._w, self._y - ky + self._h),
                             CROSS_LINE_WIDTH)
            pygame.draw.line(self._surf, self._color,
                             (self._x + kx, self._y - ky + self._h),
                             (self._x - kx + self._w, self._y + ky),
                             CROSS_LINE_WIDTH)
