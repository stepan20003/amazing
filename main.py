from getpath import PathFinder, MazeError
from writefile import mazewrite
from confvalidator import filldict
from sys import stderr, exit


def main() -> None:
    full_maze: list[list[int]]
    try:
        maze = PathFinder(filldict())
        full_maze = maze.mazegen()
        mazewrite(full_maze, maze.find_short_path())
    except MazeError as e:
        print(e, file=stderr)
        exit()


if __name__ == "__main__":
    main()
