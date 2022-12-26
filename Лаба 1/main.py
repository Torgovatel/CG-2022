from Camera2D import Camera2D
import pygame
import Data

FPS = 60
SCALE_SPEED = 0.3
surf = Camera2D.create_surface((1000, 600))
cam = Camera2D(surf, (1000, 600), (-10, 10, -10, 10), None)
fl_motion = False
last_pos = (None, None)
clock = Camera2D.start_fps_tick()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.VIDEORESIZE:
            cam.scale(*surf.get_size())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            speed = 0
            if event.button == 1:
                fl_motion = True
                cam.start_shift()
            elif event.button == 4 or event.button == 5:
                speed = SCALE_SPEED * (-1, 1)[event.button == 5]
            if speed != 0:
                cam.zoom(speed)
        elif fl_motion and event.type == pygame.MOUSEMOTION:
            cam.shift()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            fl_motion = False
    cam.clear_work_space()
    cam.decart_plot_segment(Data.sin)
    cam.decart_plot_segment(Data.decart_line)
    cam.decart_plot_segment(Data.decart_parab)
    cam.polar_plot_segment(Data.polar_roza1)
    cam.plot_axes()
    cam.display()
    clock.tick(FPS)
