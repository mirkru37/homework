import Validation
import Format


# Fields

# general
def upper(min_, message=""):
    n = int_(message)
    if n <= min_:
        return upper(min_, message)
    return n


def between(min_, max_, message=""):
    if max_ < min_:
        max_, min_ = min_, max_
    n = int_(message)
    if min_ <= n <= max_:
        return n
    print("Invalid value")
    return between(min_, max_, message)


def int_(message=""):
    s = input(message)
    if Validation.is_int(s):
        return int(s)
    print("Invalid number!!!")
    return int_(message)


def file_path(message=""):
    path = input(message)
    if Validation.is_path(path):
        return path
    print("Invalid path!!!")
    return file_path(message)


def field(class_fields, field_):
    """all_fields - dict with input functions"""
    return class_fields[field_]()


def all_fields(class_fields):
    res = []
    for i in class_fields:
        res.append(class_fields[i]())
    return res


