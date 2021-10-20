import Tools
import Validation


def input_int(message):
    try:
        val = int(input(message))
    except ValueError:
        print("Invalid value. Try again!!")
        return input_int(message)
    return val


def input_upper_zero_num(message=""):
    res = input_int(message)
    if res <= 0:
        # raise ValueError("Invalid array size")
        print("You've entered wrong value. Try again!!")
        return input_upper_zero_num(message)
    return res


def input_index(message=""):
    res = input_int(message)
    if res < 0:
        # raise ValueError("Invalid array size")
        print("You've entered wrong value. Try again!!")
        return input_upper_zero_num(message)
    return res


def input_range():
    a = input("Input A: ")
    b = input("Input B: ")
    if a > b:
        a, b = b, a
    if Validation.is_num(a) and Validation.is_num(b):
        return range(int(a), int(b))
    if len(a) == 1 and len(b) == 1:
        return Tools.char_range(a, b)
    print("Invalid range!!!")
    return input_range()


def input_file_path(message=""):
    path = input(message)
    if Validation.is_path(path):
        return path
    print("Invalid path!!!")
    return input_file_path(message)
