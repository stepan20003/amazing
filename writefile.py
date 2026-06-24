from sys import stderr
from typing import Any


def mazewrite(
    maze: list[list[int]],
    mazepath: list[tuple[int, int]],
    conf: dict[str, Any],
) -> None:
    outputf = conf["OUTPUT_FILE"]
    direct = {
        'N': (-1, 0),
        'E': (0, 1),
        'S': (1, 0),
        'W': (0, -1)
    }
    try:
        with open(str(outputf), "w") as out:
            for row in maze:
                for cell in row:
                    out.write(format(cell, "x"))
                out.write('\n')
            out.write("\n")
            out.write(str(conf['ENTRY']))
            out.write("\n")
            out.write(str(conf['EXIT']))
            out.write("\n")
            for start, end in zip(mazepath, mazepath[1:]):
                a, b = start
                c, d = end
                for key, val in direct.items():
                    g, m = val
                    if a + g == c and b + m == d:
                        out.write(key)
                        break
    except OSError as e:
        print(e, file=stderr)
