from Camera2D import Camera2D
import pygame
from Point import Point
from Matrix import Matrix
from AffineTransform import *
from Model2D import Model2D
from Scene2D import Scene2D
from Camera2D import *
pygame.init()
FPS = 60
SCALE_SPEED = 0.3
point_list = [Point(1, 1, 1),
              Point(5, 1, 1),
              Point(5, 4, 1),
              Point(1, 4, 1),
              Point(3, 5, 1)]

arcs = [[0, 1], [1, 2], [0, 3], [2, 3], [3, 4], [2, 4]]

house = Model2D(point_list, arcs)
surf = Camera2D.create_surface((600, 600))
cam = Camera2D(surf, (600, 600), (-10, 10, -10, 10), None)
scene = Scene2D(cam, [house])
clock = Camera2D.start_fps_tick()
clock = Camera2D.start_fps_tick()

fl_start_shift = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                house.apply(Transfer(0, 0.5))
            elif event.key == pygame.K_DOWN:
                house.apply(Transfer(0, -0.5))
            elif event.key == pygame.K_LEFT:
                house.apply(Transfer(-0.5, 0))
            elif event.key == pygame.K_RIGHT:
                house.apply(Transfer(0.5, 0))
            elif event.key == pygame.K_q:
                house.apply(Rotation(math.pi/6))
            elif event.key == pygame.K_e:
                house.apply(Rotation(-math.pi/6))
            elif event.key == pygame.K_x:
                house.apply(Mapping(Mapping.x))
            elif event.key == pygame.K_y:
                house.apply(Mapping(Mapping.y))
            elif event.key == pygame.K_o:
                house.apply(Mapping(Mapping.o))
            elif event.key == pygame.K_EQUALS:
                house.apply(Scaling(1.2, 1.2))
            elif event.key == pygame.K_MINUS:
                house.apply(Scaling(0.8, 0.8))
            elif event.key == pygame.K_1:
                xw, yw = house.buf[4].decart_coords()
                house.apply(Transfer(xw, yw)*Rotation(math.pi/6)*Transfer(-xw, -yw))
            elif event.key == pygame.K_2:
                xw, yw = house.buf[4].decart_coords()
                house.apply(Transfer(-xw, -yw))
                x, y = house.buf[3].decart_coords()
                A, B = y, x
                A, B = A / (A**2 + B**2) ** 0.5, B / (A**2 + B**2) ** 0.5
                print(f"A = {A}, B = {B}")
                house.apply(Rotation((A, B)))
                house.apply(Mapping(Mapping.y))
                #x, y = house.buf[3].decart_coords()
                #A, B = y, x
                #A, B = A / (A ** 2 + B ** 2) ** 0.5, B / (A ** 2 + B ** 2) ** 0.5
                house.apply(Rotation((A, -B)))
                house.apply(Transfer(xw, yw))

    scene.render()
    clock.tick(FPS)
