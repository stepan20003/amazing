from getpath import MazeError
from drowmaze import DrowMaze
from writefile import mazewrite
from confvalidator import filldict
from sys import stderr, exit


def main() -> None:
    try:
        drow = DrowMaze(filldict())
        mazewrite(drow.maze, drow.road)
        drow.visual()
    except MazeError as e:
        print(e, file=stderr)
        exit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
