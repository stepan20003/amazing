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
        confer['WIDTH'] = int(conf["WIDTH"])
        confer['HEIGHT'] = int(conf['HEIGHT'])
        my_list: list[str] = str(conf['ENTRY']).split(',')
        confer['ENTRY'] = int(my_list[0]), int(my_list[1])
        my_list2: list[str] = str(conf['EXIT']).split(',')
        confer['EXIT'] = int(my_list2[0]), int(my_list2[1])
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
