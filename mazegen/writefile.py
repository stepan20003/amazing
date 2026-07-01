from sys import stderr
from typing import Any


def mazewrite(
    maze: list[list[int]],
    mazepath: list[tuple[int, int]],
    conf: dict[str, Any],
) -> None:
    """
Writes the generated maze and solution path to an output file.

The function exports the maze grid using hexadecimal encoding,
followed by entry and exit coordinates, and finally the shortest
path encoded as directional characters (N, E, S, W).

File format:
    1. Maze grid (hex values per cell, row by row)
    2. Empty line
    3. Entry coordinates
    4. Exit coordinates
    5. Path as sequence of directions

Args:
    maze (list[list[int]]): 2D grid representing maze walls.
    mazepath (list[tuple[int, int]]): Shortest path from entry to exit.
    conf (dict[str, Any]): Configuration dictionary containing output file name
        and entry/exit coordinates.

Returns:
    None

Raises:
    OSError: If the output file cannot be created or written.
"""

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
