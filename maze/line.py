from maze.pointer import Pointer
from tkinter import Canvas


class Line():

    def __init__(self, p1: Pointer, p2: Pointer):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: str = "black"):
        canvas.create_line(
            self.p1.x,
            self.p1.y,
            self.p2.x,
            self.p2.y,
            fill=fill_color,
            width=2
        )

