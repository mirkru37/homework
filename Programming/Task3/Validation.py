import re

# Field validation
name_specials = ("'", "-")  # special symbols in name
id_format = r'^[0-9]{4}'  # will be useful in case we change id to HEX or etc.
email_format = r'^[a-zA-Z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
phone_number_format = r'\++(' \
                      r'(380+\d{9})|' \
                      r'(7+\d{10})|' \
                      r'(48+\d{9})' \
                      r')'  # Ukrainian, Russia, Poland
positions = ("BE Developer", "FE Developer", "DevOps")

NAME_MIN_LENGTH = 2
MIN_WORK_HOURS = 0
MAX_WORK_HOURS = 24 * 7


def is_name(func):
    # try to make with re in future
    def inner(self, *args):
        exception = ""
        for name in args:
            valid = True
            if len(name) < NAME_MIN_LENGTH:
                valid = False
            for i, ch in enumerate(name):
                if not ch.isalpha():
                    if not (ch in name_specials
                            and i != 0
                            and (i + 1) != len(name)
                            and name[i - 1].isalpha()
                            and name[i + 1].isalpha()):
                        # if char is not available special surrounded with two letters then name is not correct
                        valid = False
            if not valid:
                if not exception:
                    exception = "Invalid arguments ["
                exception += name + ", "
        if exception:
            raise ValueError(exception + "]")
        return func(self, *args)

    return inner


def is_id(func):
    def inner(self, *args):
        exception = fullmatch(id_format, *args)
        if exception:
            exception += "]"
            raise ValueError(exception)
        return func(self, *args)

    return inner


def is_email(func):
    def inner(self, *args):
        exception = fullmatch(email_format, *args)
        if exception:
            raise ValueError(exception + "]")
        return func(self, *args)

    return inner


def is_phone_number(func):
    def inner(self, *args):
        exception = fullmatch(phone_number_format, *args)
        if exception:
            raise ValueError(exception + "]")
        return func(self, *args)

    return inner


def is_salary(func):
    def inner(self, *args):
        exception = ""
        for salary in args:
            if not is_number(salary) or float(salary) < 0:
                if not exception:
                    exception = "Invalid arguments ["
                exception += salary + ", "
        if exception:
            raise ValueError(exception + "]")
        return func(self, *args)

    return inner


def is_position(func):
    """Returns formatted position or None if there isn't one in db"""

    def inner(self, *args):
        pos = [p.lower() for p in positions]
        exception = ""
        for val in args:
            if not val.lower() in pos:
                if not exception:
                    exception = "Invalid arguments ["
                exception += val + ", "
        if exception:
            raise ValueError(exception + "]")
        return func(self, *args)

    return inner


def is_availability(func):
    def inner(self, *args):
        exception = ""
        for value in args:
            if not str(value).isdigit() or not is_in_range(int(value), MIN_WORK_HOURS, MAX_WORK_HOURS):
                if not exception:
                    exception = "Invalid arguments ["
                exception += value + ", "
        if exception:
            raise ValueError(exception + "]")
        return func(self, *args)

    return inner


# General validations
def fullmatch(format_, *args):
    """Check with re.fullmatch for all *args"""
    exception = ""
    for item in args:
        if not re.fullmatch(format_, item):
            if not exception:
                exception = "Invalid arguments ["
            exception += item + ", "
    return exception


def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_in_range(val, min, max):
    return min <= val <= max


def is_path(path):
    try:
        open(path)
        return True
    except FileNotFoundError:
        return False


def is_int(s):
    if s[0] in ('-', '+'):
        s = s[1:]
    if s.isdigit():
        return True
    return False
