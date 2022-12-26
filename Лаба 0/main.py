import pygame
from Graphic2D import *

# Функция приведения точек к главной диагонали
def correct_point(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x2 <= x1 and y2 <= y1:
        return p2, p1
    elif x2 >= x1 and y2 <= y1:
        return (x1, y2), (x2, y1)
    elif x2 <= x1 and y2 >= y1:
        return (x2, y1), (x1, y2)
    return p1, p2


# Функция печати очереди элементов фигур
def queue_print(cont, fl_hl):
    fl_first = True
    for elem in cont.to_list():
        fig = elem.figure
        fig.scale(elem.w_scl, elem.h_scl)
        fig.shift(elem.x_shift, elem.y_shift)
        fig.color = elem.color
        fig.draw()
        if fl_first and fl_hl:
            fig.draw_highlight()
            fl_first = False


# Инициализируем отрисовочный модуль
pygame.init()

# Набор системных неизменяемых констант
SPEED = 5                                           # Скорость перемещения фигуры при нажатии клавиши
SCALE_SPEED = 3                                     # Скорость роста размера фигуры при масштабировании
FPS = 60                                            # Приблизительное количество повторений цикла в секунду
MOUSE_DRAW_BOTTON = 3                               # Число отвечающее за кнопку для рисования (левая)
MOUSE_MOTION_BOTTON = 1                             # Число отвечающее за кнопку для перемещения (правая)
INFO = pygame.display.Info()                        # Информация о разрешении устройства
START_SCREEN = (INFO.current_w // 2,                # Кортеж стартового окна
                INFO.current_h // 2)

# Набор системных переменных
fl_hl = False                           # Флаг выделения
fl_start_drawing = False                # Флаг начала рисования фигуры мышью
fl_start_motion = False                 # Флаг начала перемещения фигуры мышью
fl_start_wheel = 0                      # Флаг начала масштабирования колесиком мыши
start_point, end_point = None, None     # Диагональные точки границы отрисовываемого фигурного прямоугольника
fl_tab = False                          # Нажат Tab
fl_lalt = False                         # Нажат LALT
fl_ralt = False                         # Нажат RALT
fl_backspace = False                    # Нажат backspace
current_size = START_SCREEN             # Текущий размер окна
last_size = START_SCREEN                # Старый размер окна

type_list = [Rect, Cross, Star, Triangle]

figure_queue = RoundQueue()                     # Циклическая очередь фигур для отрисовки
figure_type = RoundQueue(type_list)             # Циклическая очередь ссылок на тип текущей фигуры для отрисовки
color_queue = RoundQueue(ColorList)             # Циклическая очередь цвета отрисовки текущей фигуры

# Отрисовка рабочего окна приложения
surf = pygame.display.set_mode(START_SCREEN, pygame.RESIZABLE)
surf.fill(BACKGROUND_COLOR)
Figure.display()

# Инициализация стартовой точки для коррекции fps
clock = pygame.time.Clock()

# Основной цикл программы
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Нажата кнопка закрытия окна
            exit(0)
        elif event.type == pygame.VIDEORESIZE:
            # Изменен размер окна
            last_size = current_size
            current_size = surf.get_size()
            kw = current_size[0] / last_size[0]
            kh = current_size[1] / last_size[1]
            for elem in figure_queue.to_list()[::-1]:
                fig = elem.figure
                if int(fig.w * kw) > 0:
                    fig.w = int(fig.w * kw)
                if int(fig.h * kh) > 0:
                    fig.h = int(fig.h * kh)
                if int(fig.x * kw) > 0:
                    fig.x = int(fig.x * kw)
                if int(fig.y * kh) > 0:
                    fig.y = int(fig.y * kh)
                fig.draw()
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Нажата кнопка мыши
            if event.button == MOUSE_DRAW_BOTTON:
                fl_start_drawing = True
                fl_hl = True
                if start_point is None:
                    start_point = event.pos
                    current_type = figure_type.peek()
                    current_color = color_queue.peek()
                    current_figure = current_type(surf, current_color,
                                                  start_point[0], start_point[1],
                                                  0, 0)
                    figure_queue.push(Element(current_figure, current_color))
            elif event.button == MOUSE_MOTION_BOTTON:
                for _ in range(len(figure_queue)):
                    fig = figure_queue.peek().figure
                    if fig.in_fig(*event.pos):
                        fl_start_motion = True
                        fl_hl = True
                        if start_point is None:
                            start_point = event.pos
                        break
                    figure_queue.twist()
                else:
                    fl_hl = False
            elif event.button == 4:
                current_elem = figure_queue.peek()
                if not (current_elem is None) and current_elem.figure.in_fig(*pygame.mouse.get_pos()):
                    fl_start_wheel = 1
                    fl_hl = True
            elif event.button == 5:
                current_elem = figure_queue.peek()
                if not (current_elem is None) and current_elem.figure.in_fig(*pygame.mouse.get_pos()):
                    fl_start_wheel = -1
                    fl_hl = True
            if fl_start_wheel:
                current_elem = figure_queue.peek()
                current_elem.w_scl = fl_start_wheel * SCALE_SPEED * 5
                current_elem.h_scl = fl_start_wheel * SCALE_SPEED * 5
                queue_print(figure_queue, fl_hl)
                fl_start_wheel = 0
                current_elem.w_scl = 0
                current_elem.h_scl = 0
        elif event.type == pygame.MOUSEMOTION:
            # Перемещение колесика мыши
            if fl_start_drawing:
                current_figure = figure_queue.peek().figure
                end_point = event.pos
                p_start, *T = correct_point(start_point, end_point)
                current_figure.w = abs(end_point[0] - start_point[0])
                current_figure.h = abs(end_point[1] - start_point[1])
                current_figure.x = p_start[0]
                current_figure.y = p_start[1]
                surf.fill(BACKGROUND_COLOR)
                queue_print(figure_queue, fl_hl)
                Figure.display()
            elif fl_start_motion:
                current_figure = figure_queue.peek().figure
                end_point = event.pos
                x_sh = end_point[0] - start_point[0]
                y_sh = end_point[1] - start_point[1]
                current_figure.shift(x_sh, y_sh)
                start_point = end_point
                surf.fill(BACKGROUND_COLOR)
                queue_print(figure_queue, fl_hl)
                Figure.display()
        elif event.type == pygame.MOUSEBUTTONUP:
            # Отпущена кнопка мыши
            if event.button == MOUSE_DRAW_BOTTON:
                fl_start_drawing = False
                start_point, end_point = None, None
            elif event.button == MOUSE_MOTION_BOTTON:
                fl_start_motion = False
                start_point, end_point = None, None
        elif event.type == pygame.KEYDOWN:
            # Нажатие клавиши
            current_elem = figure_queue.peek()
            if not (current_elem is None):
                if event.key == pygame.K_TAB:
                    fl_tab = True
                if event.key == pygame.K_LALT:
                    fl_lalt = True
                if event.key == pygame.K_BACKSPACE:
                    fl_backspace = True
                if event.key == pygame.K_RALT:
                    fl_ralt = True
                if fl_hl:
                    if event.key == pygame.K_LEFT:
                        current_elem.x_shift = -SPEED
                    elif event.key == pygame.K_RIGHT:
                        current_elem.x_shift = SPEED
                    if event.key == pygame.K_UP:
                        current_elem.y_shift -= SPEED
                    elif event.key == pygame.K_DOWN:
                        current_elem.y_shift = SPEED
                    if event.key == pygame.K_EQUALS and event.mod == pygame.KMOD_LCTRL:
                        current_elem.w_scl = SCALE_SPEED
                        current_elem.h_scl = SCALE_SPEED
                    elif event.key == pygame.K_MINUS and event.mod == pygame.KMOD_LCTRL:
                        current_elem.w_scl = -SCALE_SPEED
                        current_elem.h_scl = -SCALE_SPEED
                    if event.key == pygame.K_BACKSPACE:
                        fl_backspace = True
        elif event.type == pygame.KEYUP:
            # Поднятие клавиши
            current_elem = figure_queue.peek()
            if not (current_elem is None):
                if event.key == pygame.K_TAB and fl_tab:
                    fl_tab = False
                    if fl_hl:
                        figure_queue.twist()
                    else:
                        fl_hl = True
                if event.key == pygame.K_LALT and fl_lalt:
                    fl_lalt = False
                    color_queue.twist()
                    if fl_hl:
                        figure_queue.peek().color = color_queue.peek()
                if event.key == pygame.K_BACKSPACE and fl_backspace:
                    fl_backspace = False
                    fl_start_wheel = False
                    fl_start_motion = False
                    fl_start_drawing = False
                    start_point, end_point = None, None
                    if fl_hl:
                        figure_queue.pop()
                        fl_hl = False
                if event.key == pygame.K_RALT and fl_ralt:
                    fl_ralt = False
                    figure_type.twist()
                    current_elem = figure_queue.peek()
                    if not (current_elem is None) and fl_hl:
                        cf = current_elem.figure
                        current_elem.figure = figure_type.peek()(surf, color_queue.peek(), cf.x, cf.y, cf.w, cf.h)
                if fl_hl:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        current_elem.y_shift = 0
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        current_elem.x_shift = 0
                    if event.key in [pygame.K_MINUS, pygame.K_EQUALS, pygame.K_RCTRL]:
                        current_elem.w_scl, current_elem.h_scl = 0, 0
    # Отрисовка кадра
    surf.fill(BACKGROUND_COLOR)
    queue_print(figure_queue, fl_hl)
    Figure.display()
    clock.tick(FPS)
