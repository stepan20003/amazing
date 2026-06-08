import invenvcheck as inv
from sys import exit


__all__ = ["inv"]


def validate() -> dict[str: str]:
    text: list[str] = []
    my_dcit: dict[str: str] = {}
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
        if not list(my_dcit.keys()) == valid_cases:
            raise ValueError("Invalid Config: Config must "
                             "be have all valid keys")
        return my_dcit
    except ValueError as e:
        raise ValueError(e)


def filldict() -> dict[str: int | str] | None:
    conf: dict[str: str]
    try:
        conf = validate()
        conf['WIDTH'] = int(conf["WIDTH"])
        conf['HEIGHT'] = int(conf['HEIGHT'])
        my_list: list[str | int] = str(conf['ENTRY']).split(',')
        conf['ENTRY'] = int(my_list[0]), int(my_list[1])
        my_list2: list[str | int] = str(conf['EXIT']).split(',')
        conf['EXIT'] = int(my_list2[0]), int(my_list2[1])
        conf['SEED'] = int(conf['SEED'])
        conf['PERFECT'] = bool(conf['PERFECT'])
    except ValueError as e:
        print(e)
        exit()
    except OSError as e:
        print(e)
        exit()
    return conf
