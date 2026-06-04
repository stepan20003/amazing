from confvalidator import filldict


def createmase():
    conf: dict[str: str] = filldict()
    width = conf['WIDTH']
    height = conf['HEIGHT']
    try:
        width = int(width)
        height = int(width)
    except ValueError as e:
        print(f"Invalid value for {e}")
        return
    mase: list[list[str]]
    mase = ['F' for i in range(width)]
    mase = [mase for i in range(height)]
    return mase


def masewrite() -> None:
    conf: dict[str: str] = filldict()
    outputf = conf["OUTPUT_FILE"]
    mase = createmase()
    try:
        with open(outputf, "w") as out:
            for i in mase:
                out.write(i)
    except OSError as e:
        print(e)


masewrite()
