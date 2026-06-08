from confvalidator import filldict


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


masewrite()


class GenMaze():
    def __init__(self, maze: list[list[str]], entry: tuple[int, int], exit: tuple[int, int]):
        self.maze = maze
        self.entry = entry
        self.exit = exit
    
    def mazeing(self):
        valid: bool = True
        x = 0
        y = 0
        
    

        