from confvalidator import filldict


def createmase():
    conf: dict[str: str] = filldict()
    width = conf['WIDTH']
    height = conf['HEIGHT']
    mase: list[list[str]]
    mase = ['F' for i in range(width)]
    mase = [mase for i in range(height)]
    return mase


def masewrite(mase: list[str | int]) -> None:
    conf: dict[str: str] = filldict()
    outputf = conf["OUTPUT_FILE"]
    x, y = conf["ENTRY"]
    a, b = conf["EXIT"]
    try:
        with open(outputf, "w") as out:
            for i in mase:
                for j in i:
                    out.write(format(j, "x"))
                out.write('\n')
            for i in mase:
                for j in i:
                    print((hex(j).strip("0x")), end="")
                print()
    except OSError as e:
        print(e)
