def print_fields(val):
    i = 0
    for i, key in enumerate(vars(val).keys()):
        op = str(key).split("__")[-1].capitalize()
        print(f"{i + 1}-{op}")
    i += 1
    return i


def get_attr(from_, index):
    """returns index position attribute of from_ at of_"""
    return getattr(from_, list(vars(from_).keys())[index])


def get_attr_name(from_, index):
    """returns name of from_ attribute on index pos"""
    return list(vars(from_).keys())[index]
