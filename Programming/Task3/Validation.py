import re

# Field validation
name_specials = ("'", "-")  # special symbols in name
id_format = r'^[0-9]{4,}'  # will be useful in case we change id to HEX or etc.
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


def is_name(name):
    if len(name) < NAME_MIN_LENGTH:
        return False
    for i, ch in enumerate(name):
        if not ch.isalpha():
            if not (ch in name_specials
                    and i != 0
                    and (i + 1) != len(name)
                    and name[i - 1].isalpha()
                    and name[i + 1].isalpha()):
                # if char is not available special surrounded with two letters then name is not correct
                return False
    return True


def is_id(id):
    return re.fullmatch(id_format, id)


def is_email(email):
    return re.fullmatch(email_format, email)


def is_phone_number(number):
    return re.fullmatch(phone_number_format, number)


def is_salary(value):
    if is_number(value):
        return float(value) >= 0
    return False


def get_valid_position(position):
    """Returns formatted position or None if there isn't one in db"""
    for i in positions:
        if position.lower() == i.lower():
            return i
    return None


def is_availability(value):
    if str(value).isdigit():
        return is_in_range(int(value), MIN_WORK_HOURS, MAX_WORK_HOURS)
    return None


# General validations

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
