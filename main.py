from window import Window
from util_objects import Maze

NUM_ROWS = 10
NUM_COLS = 10
CELL_SIZE = 40
PADDING = 40


def main():
    win = Window(NUM_ROWS * CELL_SIZE + PADDING,
                 NUM_COLS * CELL_SIZE + PADDING)

    Maze(win, NUM_ROWS, NUM_COLS, CELL_SIZE, x=PADDING // 2, y=PADDING // 2)

    win.wait_for_close()


main()
