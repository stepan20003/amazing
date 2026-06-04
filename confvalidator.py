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
    new_dict: dict[str: str | int] = {}
    try:
        conf = validate()
        conf['WIDTH'] = int(conf["WIDTH"])
    except ValueError as e:
        print(e)
        exit()
    except OSError as e:
        print(e)
        exit()
    print(conf)
    return conf


print(filldict())
