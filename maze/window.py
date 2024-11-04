from tkinter import Tk, BOTH, Canvas
from .line import Line


class Window():
    def __init__(self, width, height):
        canvas_opts = {
            "height": height,
            "width": width,
            "bg": "white"
        }

        self.__root = Tk()
        self.__root.title("A-\"maze\"-ing solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(master=self.__root, **canvas_opts)
        self.__canvas.pack()
        self.__running = False

    def redraw(self):
        self.__root.update()
        self.__root.update_idletasks()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        print("Window closed, exiting program.")
        self.__running = False

    def draw_line(self, line: Line, fill_color="black"):
        line.draw(self.__canvas, fill_color=fill_color)


if __name__ == "__main__":
    w = Window(800, 600)
    w.wait_for_close()
