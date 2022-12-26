from Graphic2D.Colors.Colors import BASE_FIGURE_COLOR

class Element:
    def __init__(self, fig, color=BASE_FIGURE_COLOR, x_sh=0, y_sh=0, w_scl=0, h_scl=0, k=1):
        self.figure = None
        if not(fig is None):
            self.figure = fig
        self.color = color
        self.x_shift, self.y_shift = x_sh, y_sh
        self.w_scl, self.h_scl = w_scl, h_scl
        self.k = k


class Node:
    def __init__(self, elem, next=None):
        self.data = elem
        self.next = next
