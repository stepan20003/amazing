from getpath import PathFinder, MazeError
from writefile import mazewrite
from confvalidator import filldict
from sys import stderr, exit
from drowmaze import visualize


def main() -> None:
    full_maze: list[list[int]]
    try:
        maze = PathFinder(filldict())
        full_maze = maze.mazegen()
        path = maze.find_short_path()
        mazewrite(full_maze, path)
        visualize(full_maze, path, maze.entry, maze.exit)
    except MazeError as e:
        print(e, file=stderr)
        exit()


if __name__ == "__main__":
    main()
