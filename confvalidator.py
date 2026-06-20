import invenvcheck as inv
from sys import exit, stderr


__all__ = ["inv"]


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
        for i in text:
            if i.startswith('#') or not i:
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


def filldict() -> dict[str, int | str | None | tuple[int, int]]:
    conf: dict[str, str] = {}
    confer: dict[str, int | str | None | tuple[int, int]] = {}
    try:
        conf = validate()
        confer['WIDTH'] = int(conf["WIDTH"])
        confer['HEIGHT'] = int(conf['HEIGHT'])
        my_list: list[str] = str(conf['ENTRY']).split(',')
        confer['ENTRY'] = int(my_list[0]), int(my_list[1])
        my_list2: list[str] = str(conf['EXIT']).split(',')
        confer['EXIT'] = int(my_list2[0]), int(my_list2[1])
        confer["PERFECT"] = conf["PERFECT"].strip().lower() == "true"
        if conf["SEED"] == "None":
            confer["SEED"] = None
        else:
            confer["SEED"] = int(conf["SEED"])
        confer["OUTPUT_FILE"] = conf["OUTPUT_FILE"]
    except ValueError as e:
        print(e, file=stderr)
        exit()
    except OSError as e:
        print(e, file=stderr)
        exit()
    return confer
