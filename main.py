import typing


def validate() -> bool:
    text: list[str] = []
    my_dcit: dict[str: int] = {}
    valid_cases: list[str] = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE',
                              'PERFECT', 'SEED']

    try:
        with open("config.txt", "r") as config:
            text = [x for x in config.read().split("\n")]
    except OSError as a:
        print(a)
    try:
        for i in text:
            if i.startswith('#') or not i:
                continue
            if "=" not in i:
                raise ValueError("Invalid Config: Key and"
                                 " Value must seperated with '='")
            i = i.split("=")

            my_dcit.update({i[0].strip(): (i[1].strip())})
        if list(my_dcit.keys()) == valid_cases:
            raise ValueError("Invalid Config: Config must "
                             "be have all valid keys")
    except ValueError as e:
        print(e)
    
        


validate()
