import unittest

from maze.maze import Maze
from pprint import pprint


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        self.assertEqual(
            len(m1._cells),
            num_cols
        )

        self.assertEqual(
            len(m1._cells[0]),
            num_rows
        )

    def test_maze_rectangular_cells(self):
        num_rows = 5
        num_cols = 5
        m1 = Maze(0, 0, num_rows, num_cols, 5, 10)

        self.assertEqual(
                len(m1._cells),
                num_cols
        )
        self.assertEqual(
                len(m1._cells[0]),
                num_rows
        )

    def test_break_entrance_and_exit(self):
        num_rows = 5
        num_cols = 5
        m1 = Maze(0, 0, num_rows, num_cols, 5, 10)

        entrance_i, entrace_j = 0, 0
        exit_i, exit_j = len(m1._cells) - 1, len(m1._cells) - 1

        m1._break_entrance_and_exit()

        self.assertEqual(
            m1._cells[entrance_i][entrace_j].top_wall_active,
            False,
            "Entrance top wall expected to be False"
        )
        self.assertEqual(
                m1._cells[exit_i][exit_j].bottom_wall_active,
                False,
                "Exit bottom wall expected to be false"
        )

    def test_reset_cells_visited(self):
        num_rows = 5
        num_cols = 5
        m1 = Maze(0, 0, num_rows, num_cols, 5, 10)
        m1._reset_cells_visited()

        valid_matrix = True

        for column in m1._cells:
            for cell in column:
                if cell.visited:
                    valid_matrix = False

        self.assertTrue(valid_matrix, "Not all cells were reset")


if __name__ == "__main__":
    unittest.main()
