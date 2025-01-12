import tkinter
import time
import random


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Line:
    def __init__(self, point_a: Point, point_b: Point):
        self.point_a = point_a
        self.point_b = point_b

    def draw(self, canvas: tkinter.Canvas, color: str, width: int = 2):
        canvas.create_line(self.point_a.x,
                           self.point_a.y,
                           self.point_b.x,
                           self.point_b.y,
                           fill=color,
                           width=width)


class Cell:
    def __init__(self,
                 point_a: Point,
                 point_b: Point,
                 t_wall: bool = True,
                 r_wall: bool = True,
                 b_wall: bool = True,
                 l_wall: bool = True):
        self.t_wall = t_wall
        self.r_wall = r_wall
        self.b_wall = b_wall
        self.l_wall = l_wall
        self.point_a = point_a
        self.point_b = point_b
        self.visited = False

    def draw(self, win):
        top_wall = Line(Point(self.point_a.x, self.point_a.y),
                        Point(self.point_b.x, self.point_a.y))
        win.draw_line(top_wall, color="black" if self.t_wall else "white")
        right_wall = Line(Point(self.point_b.x, self.point_a.y),
                          Point(self.point_b.x, self.point_b.y))
        win.draw_line(right_wall, color="black" if self.r_wall else "white")
        bottom_wall = Line(Point(self.point_a.x, self.point_b.y),
                           Point(self.point_b.x, self.point_b.y))
        win.draw_line(bottom_wall, color="black" if self.b_wall else "white")
        left_wall = Line(Point(self.point_a.x, self.point_a.y),
                         Point(self.point_a.x, self.point_b.y))
        win.draw_line(left_wall, color="black" if self.l_wall else "white")

    def draw_move(self, to_cell, win, undo=False):
        P1 = Point((self.point_b.x - self.point_a.x) // 2 + self.point_a.x,
                   (self.point_b.y - self.point_a.y) // 2 + self.point_a.y)
        P2 = Point((to_cell.point_b.x - to_cell.point_a.x) // 2 + to_cell.point_a.x,
                   (to_cell.point_b.y - to_cell.point_a.y) // 2 + to_cell.point_a.y)
        L = Line(P1, P2)
        win.draw_line(L, "#497be8" if not undo else "#ea7d7d")

    def has_wall(self, wall):
        return getattr(self, wall, False)

    def __repr__(self):
        return f"Cell({self.point_a}, {self.point_b}, t_wall: {self.t_wall}, r_wall: {self.r_wall}, b_wall: {self.b_wall}, l_wall: {self.l_wall}, visited: {self.visited})"


class Maze:
    def __init__(self, win, num_rows, num_cols, cell_size, x=0, y=0):
        self.win = win
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size = cell_size
        self.x = x
        self.y = y
        self._cells = []
        self._visited = []
        self._directions = {
            "t_wall": (-1, 0),
            "r_wall": (0, 1),
            "b_wall": (1, 0),
            "l_wall": (0, -1)
        }
        self._create_cells()

    def _create_cells(self):
        for i in range(self.num_rows):
            row = []
            for j in range(self.num_cols):
                P1 = Point(j * self.cell_size + self.x,
                           i * self.cell_size + self.y)
                P2 = Point(j * self.cell_size + self.cell_size + self.x,
                           i * self.cell_size + self.cell_size + self.y)
                C = Cell(P1, P2,
                         t_wall=False if i == 0 and j == 0 else True,
                         b_wall=False if (i + 1) == self.num_rows and (j + 1) == self.num_cols else True)
                row.append(C)
            self._cells.append(row)

        self._draw_cells()

    def _draw_cells(self):
        for _, row in enumerate(self._cells):
            for _, c in enumerate(row):
                c.draw(self.win)
                self._animate()
        self._break_walls(current=(0, 0))
        self._reset_visited()
        self._solve()

    def _break_walls(self, current):
        self._cells[current[0]][current[1]].visited = True
        while True:
            to_visit = []
            for d in self._directions.values():
                next_cell = (current[0] + d[0], current[1] + d[1])
                if next_cell[0] in range(self.num_rows) and next_cell[1] in range(self.num_cols) and not self._cells[next_cell[0]][next_cell[1]].visited:
                    to_visit.append(next_cell)
                else:
                    continue
            if len(to_visit) <= 0:
                return
            rand_cell = random.choice(to_visit)
            self._repaint_wall(
                previous_cell=self._cells[current[0]][current[1]], next_cell=self._cells[rand_cell[0]][rand_cell[1]])
            self._break_walls(rand_cell)

    def _repaint_wall(self, previous_cell: Cell, next_cell: Cell):
        if previous_cell.point_a.x == next_cell.point_a.x and previous_cell.point_a.y < next_cell.point_a.y:
            previous_cell.b_wall = False
            next_cell.t_wall = False
            previous_cell.draw(self.win)
            next_cell.draw(self.win)
            self._animate()
        elif previous_cell.point_a.x == next_cell.point_a.x and previous_cell.point_a.y > next_cell.point_a.y:
            previous_cell.t_wall = False
            next_cell.b_wall = False
            previous_cell.draw(self.win)
            next_cell.draw(self.win)
            self._animate()
        elif previous_cell.point_a.y == next_cell.point_a.y and previous_cell.point_a.x < next_cell.point_a.x:
            previous_cell.r_wall = False
            next_cell.l_wall = False
            previous_cell.draw(self.win)
            next_cell.draw(self.win)
            self._animate()
        elif previous_cell.point_a.y == next_cell.point_a.y and previous_cell.point_a.x > next_cell.point_a.x:
            previous_cell.l_wall = False
            next_cell.r_wall = False
            previous_cell.draw(self.win)
            next_cell.draw(self.win)
            self._animate()

    def _reset_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False

    def _solve(self):
        self._solve_r(0, 0)
        is_solved = self._solve_r(0, 0)
        return is_solved

    def _solve_r(self, row, col):
        self._animate()
        self._cells[row][col].visited = True
        if self._cells[self.num_rows - 1][self.num_cols - 1].visited:
            return True
        for k, d in self._directions.items():
            if row + d[0] in range(self.num_rows) and col + d[1] in range(self.num_cols) and not self._cells[row][col].has_wall(k) and not self._cells[row + d[0]][col + d[1]].visited:
                self._cells[row][col].draw_move(
                    self._cells[row + d[0]][col + d[1]], self.win)
                if self._solve_r(row + d[0], col + d[1]):
                    return True

                self._cells[row][col].draw_move(
                    self._cells[row + d[0]][col + d[1]], self.win, True)

        return False

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)
