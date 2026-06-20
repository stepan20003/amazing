from confvalidator import filldict
from sys import stderr


def mazewrite(maze: list[list[int]], mazepath: list[tuple[int, int]]) -> None:
    outputf = filldict()["OUTPUT_FILE"]
    
    direct = {
        'N': (0, -1),  # Y-ով վերև
        'S': (0, 1),   # X-ով աջ
        'E': (1, 0),   # Y-ով ներքև
        'W': (-1, 0)   # X-ով ձախ
    }
    try:
        with open(str(outputf), "w") as out:
            # 1. Տպում ենք լաբիրինթոսի մատրիցը
            for i in maze:
                for j in i:
                    out.write(format(j, "x"))
                out.write('\n')
            out.write("\n")
            
            # 2. Տպում ենք Entry և Exit
            out.write(str(filldict()['ENTRY']))
            out.write("\n")
            out.write(str(filldict()['EXIT']))
            out.write("\n")
            
            # 3. Ճիշտ հաշվարկում ենք քայլերը (X, Y)-ով
            for i, j in zip(mazepath, mazepath[1:]):
                ax, ay = i
                cx, cy = j
                for key, (dx, dy) in direct.items():
                    if ax + dx == cx and ay + dy == cy:
                        out.write(key)
                        break
    except OSError as e:
        print(e, file=stderr)