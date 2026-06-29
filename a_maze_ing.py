import sys
import os
from mazemaze import MazeError
from drowed import DrowMaze
from writefile import mazewrite
from confvalidator import filldict
from sys import stderr, exit
import time


def main() -> None:
    try:
        os.system("clear")
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.flush()
        conf = filldict()
        if "color_index" not in conf:
            conf["color_index"] = 0
        drow = DrowMaze(conf)
        mazewrite(drow.maze, drow.road, conf)
        show_path = True
        os.system("clear")
        while True:
            sys.stdout.write("\033[H")
            sys.stdout.flush()
            print(drow.build_terminal_map(show_path=show_path))
            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze color")
            print("4. Quit")
            b = input("Choice (1-5): ")
            if b == "1":
                conf = filldict()
                drow = DrowMaze(conf)
                mazewrite(drow.maze, drow.road, conf)
                os.system("clear")
            elif b == "2":
                show_path = not show_path
            elif b == "3":
                if hasattr(drow, "colors") and len(drow.colors) > 0:
                    idx = getattr(drow, "color_index", 0)
                    idx = (idx + 1) % len(drow.colors)
                    drow.color_index = idx
                    conf["color_index"] = idx
            elif b == "4":
                break
            else:
                print("\033[31mEnter correct command\033[0m")
                time.sleep(0.3)
                sys.stdout.write("\033[2J")
                sys.stdout.flush()
    except MazeError as e:
        sys.stdout.write("\033[?1049l\033[?25h")
        sys.stdout.flush()
        print(e, file=stderr)
        exit(1)


if __name__ == "__main__":
    main()
