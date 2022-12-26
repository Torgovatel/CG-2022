import pygame
from Graphic2D.Figures.Figure import Figure
from math import floor
from math import ceil

class Star(Figure):
    def draw(self):
        if self._w <= 10 or self._h <= 10:
            pass
        p_top = (self._x + self._w // 2, self._y)
        k = self._y + 33 * self._h // 100
        koef = self._w // 10
        p_left_mid = (self._x, k)
        p_right_mid = (self._x + self._w, k)
        p_left_low = (self._x + koef, self._y + self._h)
        p_right_low = (self._x + self._w - koef, self._y + self._h)
        y_mid = Figure._fyb4p_(p_top, p_right_low, p_right_mid, p_left_low)
        y_pre_low = Figure._fyb4p_(p_right_mid, p_left_low, p_left_mid, p_right_low)
        for y in range(self._y, self._y + self._h + 1):
            for x in range(self._x, self._x + self._w + 1):
                if self._y <= y <= k:
                    # 1 zone
                    if y >= ceil(Figure._cyb2p_(x, p_top, p_left_low)) and y >= floor(Figure._cyb2p_(x, p_top, p_right_low)):
                        self._surf.set_at((x, y), self._color)
                elif k < y <= y_mid:
                    # 2 zone
                    if (ceil(Figure._cyb2p_(x, p_left_mid, p_right_low)) >= y and
                        floor(Figure._cyb2p_(x, p_right_mid, p_left_low)) >= y):
                            self._surf.set_at((x, y), self._color)
                elif y_mid < y <= y_pre_low:
                    # 3 zone
                    if ceil(Figure._cyb2p_(x, p_top, p_left_low)) <= y  and y >= floor(Figure._cyb2p_(x, p_top, p_right_low)):
                        self._surf.set_at((x, y), self._color)
                else:
                    # 4 zone
                    if ((ceil(Figure._cyb2p_(x, p_top, p_left_low)) <= y and
                        y <= floor(Figure._cyb2p_(x, p_right_mid, p_left_low))) or
                        (ceil(Figure._cyb2p_(x, p_left_mid, p_right_low)) >= y and
                        y >= floor(Figure._cyb2p_(x, p_top, p_right_low)))):
                        self._surf.set_at((x, y), self._color)