import time
import random

from .cell import Cell

class Maze():
    def __init__(self,
                 x1, y1,
                 num_rows, num_cols,
                 cell_size_x, cell_size_y,
                 win=None, seed=None):

        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self.seed = random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = list()
        for col in range(self._num_cols):
            column = list()
            for i in range(0, self._num_rows):
                column.append(Cell(self._win))
            self._cells.append(column)

        for i in range(0, len(self._cells)):
            for j in range(0, len(self._cells[i])):
                self._draw_cell(i, j)

    def __repr__(self):
        current_maze = []
        for column in self._cells:
            rows = []
            for cell in column:
                rows.append({
                    "x1": cell._x1,
                    "y1": cell._y1,
                    "x2": cell._x2,
                    "y2": cell._y2,
                    "top": cell.top_wall_active,
                    "right": cell.right_wall_active,
                    "bottom": cell.bottom_wall_active,
                    "left": cell.left_wall_active,
                })
            current_maze.append(rows)
        return current_maze

    def _draw_cell(self, i, j):
        if self._win is None:
            return

        cell_x1 = i * self._cell_size_x + self._x1
        cell_y1 = j * self._cell_size_y + self._y1
        cell_x2 = cell_x1 + self._cell_size_x
        cell_y2 = cell_y1 + self._cell_size_y

        self._cells[i][j].draw(cell_x1, cell_y1, cell_x2, cell_y2)
        self._animate(0.01)

    def _animate(self, speed=0.05):
        self._win.redraw()
        time.sleep(speed)

    def _reset_cells_visited(self):
        for i in range(0, len(self._cells)):
            for j in range(0, len(self._cells[i])):
                self._cells[i][j].visited = False

    def _break_entrance_and_exit(self):
        # set locations for entrance and exit in the maze matrix
        self.entrance_i, self.entrace_j = 0, 0
        self.exit_i, self.exit_j = len(self._cells)-1, len(self._cells[0])-1
        # toggle the walls
        self._cells[self.entrance_i][self.entrace_j].top_wall_active = False
        self._cells[self.exit_i][self.exit_j].bottom_wall_active = False
        # if a window has been injected to the constructor then
        # then visualize the changes
        if self._win is not None:
            self._draw_cell(self.entrance_i, self.entrace_j)
            self._draw_cell(self.exit_i, self.exit_j)

    def _break_walls_r(self, i, j):
        # mark current cell as visited
        self._cells[i][j].visited = True

        while True:
            to_visit = self._find_unvisited_possible_directions(i, j)
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return

            # Pick next neighbor/direction to visit
            direction = random.randint(0, len(to_visit) - 1)
            next = to_visit.pop(direction)
            next_i, next_j = next["locations"]
            # Knock down walls between current and next
            if next["neigbor_type"] == "top":
                # current cell
                self._cells[i][j].top_wall_active = False
                # chosen cell
                self._cells[next_i][next_j].bottom_wall_active = False
            if next["neigbor_type"] == "bottom":
                # current cell
                self._cells[i][j].bottom_wall_active = False
                # chosen cell
                self._cells[next_i][next_j].top_wall_active = False
            if next["neigbor_type"] == "left":
                # current cell
                self._cells[i][j].left_wall_active = False
                # chosen cell
                self._cells[next_i][next_j].right_wall_active = False
            if next["neigbor_type"] == "right":
                # current cell
                self._cells[i][j].right_wall_active = False
                # chosen cell
                self._cells[next_i][next_j].left_wall_active = False
            self._break_walls_r(next_i, next_j)

    def _find_unvisited_possible_directions(self, i, j):
        unvisited = list()
        # find top neighbor
        if j > 0:
            neighbor_i, neighbor_j = i, j - 1
            if not self._cells[neighbor_i][neighbor_j].visited:
                unvisited.append({
                    "neigbor_type": "top",
                    "locations": (neighbor_i, neighbor_j)
                })

        # find bottom neighbor
        if j < len(self._cells[i]) - 1:
            neighbor_i, neighbor_j = i, j + 1
            if not self._cells[neighbor_i][neighbor_j].visited:
                unvisited.append({
                    "neigbor_type": "bottom",
                    "locations": (neighbor_i, neighbor_j)
                })

        # find left neighbor
        if i > 0:
            neighbor_i, neighbor_j = i - 1, j
            if not self._cells[neighbor_i][neighbor_j].visited:
                unvisited.append({
                    "neigbor_type": "left",
                    "locations": (neighbor_i, neighbor_j)
                })

        # find right neighbor
        if i < len(self._cells) - 1:
            neighbor_i, neighbor_j = i + 1, j
            if not self._cells[neighbor_i][neighbor_j].visited:
                unvisited.append({
                    "neigbor_type": "right",
                    "locations": (neighbor_i, neighbor_j)
                })
        return unvisited

    def active_wall(self, current, neighbor):
        return current and neighbor

    def solve(self):
        i, j = 0, 0
        return self._solve_r(i, j)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        # When we are at the end cell then return True, we are done.
        if self._cells[i][j] == self._cells[self.exit_i][self.exit_j]:
            return True

        possible_directions = self._find_unvisited_possible_directions(i, j)
        while len(possible_directions) > 0:
            index = random.randint(0, len(possible_directions) - 1)
            # check if there is a wall opening in direction
            next_i, next_j = possible_directions[index]["locations"]

            if possible_directions[index]["neigbor_type"] == "top":
                current_wall = self._cells[i][j].top_wall_active
                neighbor_wall = self._cells[next_i][next_j].bottom_wall_active

            if possible_directions[index]["neigbor_type"] == "bottom":
                current_wall = self._cells[i][j].bottom_wall_active
                neighbor_wall = self._cells[next_i][next_j].top_wall_active

            if possible_directions[index]["neigbor_type"] == "right":
                current_wall = self._cells[i][j].right_wall_active
                neighbor_wall = self._cells[next_i][next_j].left_wall_active

            if possible_directions[index]["neigbor_type"] == "left":
                current_wall = self._cells[i][j].left_wall_active
                neighbor_wall = self._cells[next_i][next_j].right_wall_active

            if self.active_wall(current_wall, neighbor_wall):
                # if there is an active wall the remove
                # the neighbor from possible directions
                possible_directions.pop(index)
                continue

            if not self.active_wall(current_wall, neighbor_wall):
                print(f"move from {i, j} to {next_i, next_j}")
                self._cells[i][j].draw_move(self._cells[next_i][next_j])

            move = self._solve_r(next_i, next_j)
            if move:
                return True

            self._cells[i][j].draw_move(
                    self._cells[next_i][next_j],
                    undo=True
            )
            possible_directions.pop(index)
            continue
        return False
