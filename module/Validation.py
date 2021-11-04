import re
from datetime import datetime


def is_int(func):
    def inner(self, *args):
        for s in args:
            try:
                i = int(s)
                if i != float(s):
                    raise ValueError
            except:
                raise ValueError('not Int')
        return func(self, *args)

    return inner


def is_in_enum(enum):
    def dec(func):
        def inner(self, *args):
            for val in args:
                if not hasattr(enum, val):
                    raise ValueError('not in enum')
            return func(self, *args)

        return inner

    return dec


def is_date(func):
    def inner(self, *args):
        for val in args:
            if not type(val) == type(datetime.today()):
                raise ValueError('Not date time')
        return func(self, *args)

    return inner


def is_date_less(ceil):
    def dec(func):
        def inner(self, *args):
            for val in args:
                if val > ceil:
                    raise ValueError(f'Too big date {val} {ceil}')
            if func is not None:
                return func(self, *args)
            else:
                return True

        return inner

    return dec


def is_letters_only(func):
    def inner(self, *args):
        for val in args:
            if not re.match(r'[a-zA-Z]', val):
                raise ValueError('Not letters only')
        return func(self, *args)

    return inner


def is_number(func):
    def inner(self, *args):
        for val in args:
            float(val)
        return func(self, *args)

    return inner
