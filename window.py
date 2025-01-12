import tkinter
from util_objects import Line


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = tkinter.Tk()
        self.__root.title("Maze Solver")
        self.canvas = tkinter.Canvas(
            self.__root, background="white", width=self.width, height=self.height)
        self.canvas.pack(fill="both", expand=1, anchor="center")
        self.is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line: Line, color: str):
        line.draw(self.canvas, color=color, width=2)

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()

    def close(self):
        self.is_running = False
