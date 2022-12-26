from Descriptors import *
import pygame
import math

DEF_BACKGROUND_COLOR = (255, 255, 255)
DEF_AXES_COLOR = (0, 0, 0)
DEF_CHART_COLOR = (255, 0, 0)

def set_pixel(surf, x, y, r, g, b):
    surf.set_at((x, y), (r, g, b))

def frange(start, stop, step):
    lst = []
    i = start
    while i <= stop:
        lst.append(i)
        i += step
    return tuple(lst)

class Camera2D:
    __pygame_was_init = False

    # Инициализатор
    def __init__(self, surf, wh, lrbt, colors):
        self.L = IntegerDataDescriptor()
        self.R = IntegerDataDescriptor()
        self.B = IntegerDataDescriptor()
        self.T = IntegerDataDescriptor()
        self.H = IntegerDataDescriptor()
        self.W = IntegerDataDescriptor()
        self.surf = SurfaceDataDescriptor()
        self.background_color = ColorDataDescriptor()
        self.axes_color = ColorDataDescriptor()
        self.chart_color = ColorDataDescriptor()
        if colors is None or len(colors) < 3:
            colors = (DEF_BACKGROUND_COLOR, DEF_CHART_COLOR, DEF_AXES_COLOR)
        if lrbt is None or len(lrbt) < 4:
            lrbt = (None, None, None, None)
        self.surf = surf
        self.L, self.R, self.B, self.T = lrbt
        self.W, self.H = wh
        self.background_color, self.chart_color, self.axes_color = colors
        self.__TB = self.T - self.B
        self.__LR = self.R - self.L

    # Очистка рабочей области окна
    def clear_work_space(self):
        self.surf.fill(self.background_color)

    # Отрисовка координатных осей
    def plot_axes(self):
        # сколько в пикселе реальной длины
        kx = self.W / self.__LR
        ky = self.H / self.__TB
        x_step = max(abs(self.R), abs(self.L)) / 5
        zero_p = (-self.L / self.__LR * self.W, self.T / self.__TB * self.H)
        # OX
        f = pygame.font.Font(None, 24)
        if self.B <= 0 <= self.T:
            ys = int(self.T / self.__TB * self.H)
            pygame.draw.line(self.surf, self.axes_color, (0, ys), (self.W, ys))
            x_start_s = zero_p[0] + x_step * kx
            x_start_w = x_step
            while x_start_w < self.R:
                pygame.draw.line(self.surf, self.axes_color, (x_start_s, ys-5), (x_start_s, ys+5))
                txt = f.render(str(x_start_w)[:4], False, (0, 0, 0))
                self.surf.blit(txt, (x_start_s-5, ys+7))
                x_start_s += x_step * kx
                x_start_w += x_step
            x_start_s = zero_p[0] - x_step * kx
            x_start_w = x_step
            while x_start_w > self.L:
                pygame.draw.line(self.surf, self.axes_color, (x_start_s, ys-5), (x_start_s, ys+5))
                x_start_s -= x_step * kx
                x_start_w -= x_step
        # OY
        if self.L <= 0 <= self.R:
            xs = int(-self.L / self.__LR * self.W)
            pygame.draw.line(self.surf, self.axes_color, (xs, 0), (xs, self.H))

    # Отрисовка отрезка в мировых координатах по декарту
    def decart_plot_segment(self, func, x_st=None, x_end=None):
        if x_st is None:
            x_st = self.L
        if x_end is None:
            x_end = self.R
        step = (x_end - x_st) / self.W
        for xw in frange(x_st, x_end, step):
            xs = int((xw - self.L) / self.__LR * self.W)
            ys = int((self.T - func(xw)) / self.__TB * self.H)
            set_pixel(self.surf, xs, ys, *self.chart_color)


    # Отрисовка отрезка в мировых координатах полярная
    def polar_plot_segment(self, func, x_st=None, x_end=None):
        if x_st is None:
            x_st = 0
        if x_end is None:
            x_end = 2 * math.pi
        step = (x_end - x_st) / self.W
        for fi in frange(x_st, x_end, step):
            r = func(fi)
            xw = r * math.cos(fi)
            yw = r * math.sin(fi)
            xs = int((xw - self.L) / self.__LR * self.W)
            ys = int((self.T - yw) / self.__TB * self.H)
            set_pixel(self.surf, xs, ys, *self.chart_color)


    def start_shift(self):
        self.__last_motion_point = pygame.mouse.get_pos()

    # Свдиг
    def shift(self):
        cur_pos = pygame.mouse.get_pos()
        dx = cur_pos[0] - self.__last_motion_point[0]
        dy = -(cur_pos[1] - self.__last_motion_point[1])
        self.__last_motion_point = cur_pos
        self.L = self.L - self.__LR * dx / self.W
        self.R = self.R - self.__LR * dx / self.W
        self.B = self.B - self.__TB * dy / self.H
        self.T = self.T - self.__TB * dy / self.H
        self.__LR = self.R - self.L
        self.__TB = self.T - self.B


    # Приближение
    def zoom(self, arg):
        if self.__LR + 2 * arg > 0 and self.__TB + 2 * arg > 0:
            x, y = pygame.mouse.get_pos()
            xw = self.L + self.__LR * (x / self.W)
            yw = self.T - self.__TB * (y / self.H)
            k_g = self.__LR / (self.__LR + 2 * arg)
            k_v = self.__TB / (self.__TB + 2 * arg)
            k = 1 - arg
            k_g = k_v = k
            self.L = xw - (xw - self.L) / k_g
            self.R = xw + (self.R - xw) / k_g
            self.B = yw - (yw - self.B) / k_v
            self.T = yw + (self.T - yw) / k_v
            self.__LR = self.R - self.L
            self.__TB = self.T - self.B

    # Масштабируемость
    def scale(self, nW, nH):
        self.W = nW
        self.H = nH
        RL2 = (self.R + self.L) / 2
        TB2WH = (self.T - self.B) / 2 * nW / nH
        self.L = RL2 - TB2WH
        self.R = RL2 + TB2WH
        self.__LR = self.R - self.L


    # Отображение
    @staticmethod
    def display():
        pygame.display.flip()

    # Создание экрана
    @staticmethod
    def create_surface(size):
        if not Camera2D.__pygame_was_init:
            pygame.init()
            Camera2D.__pygame_was_init = True
        return pygame.display.set_mode(size, pygame.RESIZABLE)

    @staticmethod
    def start_fps_tick():
        return pygame.time.Clock()
