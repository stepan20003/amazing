from sys import exit, stderr


def validate() -> dict[str, str]:
    text: list[str] = []
    my_dcit: dict[str, str] = {}
    valid_cases: list[str] = ['WIDTH',
                              'HEIGHT',
                              'ENTRY',
                              'EXIT',
                              'OUTPUT_FILE',
                              'PERFECT',
                              'SEED']

    with open("config.txt", "r") as config:
        text = [x for x in config.read().split("\n")]
    try:
        for i in text[:]:
            if i.startswith('#') or not i:
                text.remove(i)
                continue
            if "=" not in i:
                raise ValueError("Invalid Config: Key and"
                                 " Value must seperated with '='")
            k = i.split("=")
            my_dcit.update({k[0].strip(): (k[1].strip())})
        if set(my_dcit.keys()) != set(valid_cases):
            raise ValueError("Invalid Config: Config must "
                             "be have all valid keys")
        return my_dcit
    except ValueError as e:
        raise ValueError(e)


def filldict() -> dict[str, int | str | None | tuple[int, int] | bool]:
    conf: dict[str, str] = {}
    confer: dict[str, int | str | None | tuple[int, int] | bool] = {}
    try:
        conf = validate()
        width = int(conf["WIDTH"])
        height = int(conf['HEIGHT'])
        if width < 1 or height < 1:
            raise ValueError(
                "Invalid Config: WIDTH and HEIGHT must be positive"
            )
        confer['WIDTH'] = width
        confer['HEIGHT'] = height
        my_list: list[str] = str(conf['ENTRY']).split(',')
        entry = (int(my_list[0]), int(my_list[1]))
        my_list2: list[str] = str(conf['EXIT']).split(',')
        exit_point = (int(my_list2[0]), int(my_list2[1]))
        if entry == exit_point:
            raise ValueError("Invalid Config: ENTRY and EXIT must differ")
        for name, point in (('ENTRY', entry), ('EXIT', exit_point)):
            x, y = point
            if not (0 <= x < width and 0 <= y < height):
                raise ValueError(
                    f"Invalid Config: {name} ({x},{y}) is out of bounds"
                )
        confer['ENTRY'] = entry
        confer['EXIT'] = exit_point
        if conf['PERFECT'] == 'True':
            confer['PERFECT'] = True
        elif conf['PERFECT'] == 'False':
            confer['PERFECT'] = False
        else:
            raise ValueError("Invalid Config: PERFECT must be True or False")
        if conf['SEED'] == 'None':
            confer['SEED'] = None
        else:
            confer['SEED'] = int(conf['SEED'])
        confer["OUTPUT_FILE"] = conf["OUTPUT_FILE"]
    except ValueError as e:
        print(e, file=stderr)
        exit(1)
    except OSError as e:
        print(e, file=stderr)
        exit(1)
    return confer
