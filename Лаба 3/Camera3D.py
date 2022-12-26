from Descriptors import *
import pygame
import math
from Camera2D import *
from Point3D import Point3D
from Matrix import Matrix

class Camera3D(Camera2D):
    # Инициализатор
    def __init__(self,
                 surf,              # Окно отрисовки
                 wh,                # Разрешение окна
                 lrbt,              # Параметры центрирования окна в 2D
                 Ov=(0, 0, 0),      # Точка плоскости напротив наблюдателя
                 Tv=(0, 1, 0),      # Вектор вверх от наблюдающего
                 N=(0, 0, 1),       # Вектор нормали от плоскости проектирования
                 D=16,              # Дистанция от точки наблюдения до плоскости проектирования
                 colors=None):      # Массив цветов для (фона, осей, пера)
        super().__init__(surf, wh, lrbt, colors)
        self.Ov = Ov
        self.Tv = Tv
        self.N = N
        self.D = D
        self.calc_ijk()

    @staticmethod
    def VectorNorm(v):
        return (v[0]**2 + v[1]**2 + v[2]**2) ** 0.5

    @staticmethod
    def VectorMul(v1, v2):
        return v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0]


    # Пересчет базисных векторов и матриц переходов
    def calc_ijk(self):
        # Пересчет базисных векторов
        n_norm = Camera3D.VectorNorm(self.N)
        self.kv = list(map(lambda x: x / n_norm, self.N))
        TN = Camera3D.VectorMul(self.Tv, self.N)
        TN_norm = Camera3D.VectorNorm(TN)
        self.iv = list(map(lambda x: x / TN_norm, TN))
        self.jv = Camera3D.VectorMul(self.kv, self.iv)
        # Матрица перевода мировых в видовые
        self.S_w_in_v = Matrix(4)
        i_expr, j_expr, k_expr = 0, 0, 0
        Ov = self.Ov
        i_expr = self.iv[0] * Ov[0] + self.iv[1] * Ov[1] + self.iv[2] * Ov[2]
        j_expr = self.jv[0] * Ov[0] + self.jv[1] * Ov[1] + self.jv[2] * Ov[2]
        k_expr = self.kv[0] * Ov[0] + self.kv[1] * Ov[1] + self.kv[2] * Ov[2]
        self.S_w_in_v.buf = [[self.iv[0], self.iv[1], self.iv[2], -i_expr],
                             [self.jv[0], self.jv[1], self.jv[2], -j_expr],
                             [self.kv[0], self.kv[1], self.kv[2], -k_expr],
                             [0, 0, 0, 1]]
        # Матрицы перевода мировых в проекционные
        self.S_v_in_p_ort = Matrix(3, 4)
        self.S_v_in_p_ort.buf = [[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 0, 1]]
        self.S_v_in_p_persp = Matrix(3, 4)
        self.S_v_in_p_persp.buf = [[1, 0, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, -1/self.D, 1]]


    def to_screen_coord(self, p):
        # перевод в видовые
        Uv = self.S_w_in_v * p
        # перевод в проекционные
        if Uv[2] == self.D:
            Up = self.S_v_in_p_ort * Uv
        elif Uv[2] < self.D:
            Up = self.S_v_in_p_persp * Uv
        else:
            return None
        # перевод в экранные
        return super().to_screen_coord(Up[0]/Up[2], Up[1]/Up[2])

    # Отрисовка координатных осей
    def plot_axes(self):
        # сколько в пикселе реальной длины
        kx = self.W / (self.R - self.L)
        ky = self.H / (self.T - self.B)
        # OX
        if self.B <= 0 <= self.T:
            ys = int(self.T / (self.T - self.B) * self.H)
            pygame.draw.line(self.surf, self.axes_color, (0, ys), (self.W, ys))
        # OY
        if self.L <= 0 <= self.R:
            xs = int(-self.L / (self.R - self.L) * self.W)
            pygame.draw.line(self.surf, self.axes_color, (xs, 0), (xs, self.H))

    def plot_model(self, model):
        points = model.buf
        arcs = model.matrix
        for p in points:
            res = self.to_screen_coord(p)
            if not (res is None):
                xs, ys = res[0], res[1]
                set_pixel(self.surf, xs, ys, *DEF_MODEL_COLOR)
        for num1, num2 in arcs:
            p1, p2 = points[num1], points[num2]
            res1 = self.to_screen_coord(p1)
            res2 = self.to_screen_coord(p2)
            if not(res1 is None or res2 is None):
                xs1, ys1 = res1[0], res1[1]
                xs2, ys2 = res2[0], res2[1]
                pygame.draw.line(self.surf, DEF_MODEL_COLOR, (xs1, ys1), (xs2, ys2))
        self.plot_axes()