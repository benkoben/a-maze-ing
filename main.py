from maze.window import Window

from maze.maze import Maze


def main():
    window_width = 805
    window_heigth = 605
    win = Window(window_width, window_heigth)

    m1 = Maze(
        x1=5,
        y1=5,
        num_rows=12,
        num_cols=16,
        cell_size_x=50,
        cell_size_y=50,
        win=win,
    )
    m1.solve()

    win.wait_for_close()


if __name__ == "__main__":
    main()
