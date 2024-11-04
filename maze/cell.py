from .window import Window
from .pointer import Pointer
from .line import Line


class Cell():

    def __init__(self, window: Window):
        self.left_wall_active = True
        self.right_wall_active = True
        self.top_wall_active = True
        self.bottom_wall_active = True
        self._win = window
        self.visited = False

        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        top_wall_color = "pink"
        left_wall_color = "pink"
        right_wall_color = "pink"
        bottom_wall_color = "pink"

        if not self.left_wall_active:
            left_wall_color = "white"
        self._win.draw_line(Line(
                Pointer(x=self._x1, y=self._y1),  # start
                Pointer(x=self._x1, y=self._y2),  # stop
            ),
            left_wall_color
        )

        if not self.top_wall_active:
            top_wall_color = "white"
        self._win.draw_line(Line(
                Pointer(x=self._x1, y=self._y1),  # start
                Pointer(x=self._x2, y=self._y1),  # stop
            ),
            top_wall_color
        )

        if not self.right_wall_active:
            right_wall_color = "white"
        self._win.draw_line(Line(
                Pointer(x=self._x2, y=self._y1),  # start
                Pointer(x=self._x2, y=self._y2),  # stop
            ),
            right_wall_color
        )

        if not self.bottom_wall_active:
            bottom_wall_color = "white"
        self._win.draw_line(Line(
                Pointer(x=self._x1, y=self._y2),  # start
                Pointer(x=self._x2, y=self._y2),  # stop
            ),
            bottom_wall_color
        )

    def draw_move(self, to_cell, undo=False):
        self_mx = (self._x2 - self._x1) / 2 + self._x1
        self_my = (self._y2 - self._y1) / 2 + self._y1
        other_mx = (to_cell._x2 - to_cell._x1) / 2 + to_cell._x1
        other_my = (to_cell._y2 - to_cell._y1) / 2 + to_cell._y1

        start = Pointer(x=self_mx, y=self_my)
        stop = Pointer(x=other_mx, y=other_my)

        if undo:
            self._win.draw_line(Line(start, stop), fill_color="white")
            return

        self._win.draw_line(Line(start, stop))
