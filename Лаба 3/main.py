from Camera2D import Camera2D
import pygame
from Point2D import Point2D
from Point3D import Point3D
from Matrix import Matrix
from AffineTransform import *
from Model2D import Model2D
from Scene2D import Scene2D
from Camera2D import *
from Camera3D import *
from Scene3D import *

pygame.init()
FPS = 60
SCALE_SPEED = 0.3
point_list = [Point3D(-3, -3, -3),
              Point3D(-3, 3, -3),
              Point3D(3, -3, -3),
              Point3D(3, 3, -3),
              Point3D(0, 0, 5)]

arcs = [[0, 1], [1, 3], [2, 3], [0, 2], [0, 4], [1, 4], [2, 4], [3, 4]]

piramida = Model3D(Model3D.carcas, point_list, arcs)
surf = Camera3D.create_surface((600, 600))
cam = Camera3D(surf, (600, 600), (-40, 40, -40, 40), Ov=(0, 0, 0), N=(0, 0, 1))
scene = Scene3D(cam, [piramida])
clock = Camera3D.start_fps_tick()
clock = Camera3D.start_fps_tick()

fl_start_shift = False
motion_step = 1
fi = math.pi / 6
scale_big = 1.5
scale_small = 0.5

while True:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            exit(0)
        if keys[pygame.K_x] and not keys[pygame.K_RCTRL]:
            # Перенос по х
            if keys[pygame.K_UP]:
                piramida.apply(Transfer(motion_step, 0, 0))
            elif keys[pygame.K_DOWN]:
                piramida.apply(Transfer(-motion_step, 0, 0))
            # Масштабирование по х
            if keys[pygame.K_s] and keys[pygame.K_EQUALS]:
                piramida.apply(Scaling(scale_big, 1, 1))
            elif keys[pygame.K_s] and keys[pygame.K_MINUS]:
                piramida.apply(Scaling(scale_small, 1, 1))
            else:
                # Поворот по х
                if keys[pygame.K_MINUS]:
                    piramida.apply(Rotation(Rotation.x, fi))
                elif keys[pygame.K_EQUALS]:
                    piramida.apply(Rotation(Rotation.x, -fi))
        if keys[pygame.K_y] and not keys[pygame.K_RCTRL]:
            # Перенос по y
            if keys[pygame.K_UP]:
                piramida.apply(Transfer(0, motion_step, 0))
            elif keys[pygame.K_DOWN]:
                piramida.apply(Transfer(0, -motion_step, 0))
            # Масштабирование по y
            if keys[pygame.K_s] and keys[pygame.K_EQUALS]:
                piramida.apply(Scaling(1, scale_big, 1))
            elif keys[pygame.K_s] and keys[pygame.K_MINUS]:
                piramida.apply(Scaling(1, scale_small, 1))
            else:
                # Поворот по y
                if keys[pygame.K_MINUS]:
                    piramida.apply(Rotation(Rotation.y, fi))
                elif keys[pygame.K_EQUALS]:
                    piramida.apply(Rotation(Rotation.y, -fi))
        if keys[pygame.K_z] and not keys[pygame.K_RCTRL]:
            # Перенос по z
            if keys[pygame.K_UP]:
                piramida.apply(Transfer(0, 0, motion_step))
            elif keys[pygame.K_DOWN]:
                piramida.apply(Transfer(0, 0, -motion_step))
            # Масштабирование по z
            if keys[pygame.K_s] and keys[pygame.K_EQUALS]:
                piramida.apply(Scaling(1, 1, scale_big))
            elif keys[pygame.K_s] and keys[pygame.K_MINUS]:
                piramida.apply(Scaling(1, 1, scale_small))
            else:
                # Поворот по z
                if keys[pygame.K_MINUS]:
                     piramida.apply(Rotation(Rotation.z, fi))
                elif keys[pygame.K_EQUALS]:
                    piramida.apply(Rotation(Rotation.z, -fi))
        if keys[pygame.K_RCTRL]:
            if keys[pygame.K_o]:
                piramida.apply(Mapping(Mapping.o))
            elif keys[pygame.K_2]:
                piramida.apply(Mapping(Mapping.xz))
            elif keys[pygame.K_1]:
                piramida.apply(Mapping(Mapping.xy))
            elif keys[pygame.K_3]:
                piramida.apply(Mapping(Mapping.yz))
            elif keys[pygame.K_x]:
                piramida.apply(Mapping(Mapping.x))
            elif keys[pygame.K_y]:
                piramida.apply(Mapping(Mapping.y))
            elif keys[pygame.K_z]:
                piramida.apply(Mapping(Mapping.z))
        if keys[pygame.K_9]:
            p1 = Point3D(0, -2, 0)
            p2 = Point3D(1, 1, 0)
            piramida.apply(Transfer(-p1[0]/p1[3], -p1[1]/p1[3], -p1[2]/p1[3]))
            p2 = Transfer(-p1[0]/p1[3], -p1[1]/p1[3], -p1[2]/p1[3]) * p2
            x1, y1, z1 = p2.decart_coords()
            l = (x1**2 + y1**2 + z1**2)**0.5
            cos_a = (x1**2 + y1**2)**0.5/l
            sin_a = (1 - cos_a**2)**0.5
            cos_b = (z1**2 + y1**2)**0.5/l
            sin_b = (x1**2)**0.5/l
            print(sin_a, cos_a)
            A1, A2, A3, A4, A5, A6 = (None for i in range(6))
            A1 = Rotation(Rotation.z, (-sin_a, cos_a))
            A2 = Rotation(Rotation.y, (sin_b, cos_b))
            A3 = Rotation(Rotation.z, math.pi/6)
            A4 = Rotation(Rotation.y, (-sin_b, cos_b))
            A5 = Rotation(Rotation.z, (sin_a, cos_a))
            A6 = Transfer(p1[0]/p1[3], p1[1]/p1[3], p1[2]/p1[3])
            piramida.apply(A6*A5*A4*A3*A2*A1)
        if keys[pygame.K_8]:
            #отражение от плоскости
            pass

    scene.render()
    clock.tick(FPS)
