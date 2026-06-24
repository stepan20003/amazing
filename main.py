import sys
from mazemaze import MazeError
from drowed import DrowMaze
from writefile import mazewrite
from confvalidator import filldict
from sys import stderr, exit


def main() -> None:
    try:
        conf = filldict()
        drow = DrowMaze(conf)
        mazewrite(drow.maze, drow.road, conf)
        if not sys.stdout.isatty():
            print(drow.build_terminal_map())
    except MazeError as e:
        print(e, file=stderr)
        exit(1)


if __name__ == "__main__":
    main()
