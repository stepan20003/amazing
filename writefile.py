from confvalidator import filldict
from sys import stderr


def mazewrite(maze: list[list[int]], mazepath: list[tuple[int, int]]) -> None:
    outputf = filldict()["OUTPUT_FILE"]
    direct = {
            'N': (-1, 0),
            'E': (0, 1),
            'S': (1, 0),
            'W': (0, -1)
    }
    try:
        with open(str(outputf), "w") as out:
            for i in maze:
                for j in i:
                    out.write(format(j, "x"))
                out.write('\n')
            out.write("\n")
            out.write(str(filldict()['ENTRY']))
            out.write("\n")
            out.write(str(filldict()['EXIT']))
            out.write("\n")
            for i, j in zip(mazepath[::2], mazepath[1::2]):
                a, b = i
                c, d = j
                for key, val in direct.items():
                    g, m = val
                    if a + g == c and b + m == d:
                        out.write(key)
                        break
    except OSError as e:
        print(e, file=stderr)
