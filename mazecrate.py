from confvalidator import filldict
import random


def createmase():
    conf: dict[str: str] = filldict()
    width = conf['WIDTH']
    height = conf['HEIGHT']
    mase: list[list[str]]
    mase = ['F' for i in range(width)]
    mase = [mase for i in range(height)]
    return mase


def masewrite() -> None:
    conf: dict[str: str] = filldict()
    outputf = conf["OUTPUT_FILE"]
    mase = createmase()
    x, y = conf["ENTRY"]
    a, b = conf["EXIT"]
    try:
        with open(outputf, "w") as out:
            for i in mase:
                for j in i:
                    out.write(j)
                out.write('\n')
            out.write('\n')
            out.write(str(x))
            out.write(",")
            out.write(str(y))
            out.write("\n")
            out.write(str(a))
            out.write(",")
            out.write(str(b))
    except OSError as e:
        print(e)


class GenMaze():
    def __init__(
            self, maze: list[list[str]],
            conf: dict[str: int | str | tuple]
            ):
        self.maze = maze
        self.up = 1
        self.right = 2
        self.down = 4
        self.left = 8
        self.visited = set()
        self.stack: list[tuple[int, int]] = []
        self.conf = conf

    def mazeing(self) -> None:
        x, y = self.conf['ENTRY']
        self.visited.add(self.conf['ENTRY'])
        self.stack.append(self.conf['ENTRY'])
        while self.stack:
            x1, y1 = self.stack[-1]
