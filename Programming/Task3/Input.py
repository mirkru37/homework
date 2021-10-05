import Validation
import Format


# Fields
def name():
    name_ = Format.name(input("Input name: "))
    if Validation.is_name(name_):
        return name_
    print("Invalid name!!!")
    return name()


def id():
    id_ = input("Input id: ")
    if Validation.is_id(id_):
        return id_
    print("Invalid id!!!")
    return id()


def email():
    email_ = input("Input email: ")
    if Validation.is_email(email_):
        return email_
    print("Invalid email!!!")
    return email()


def phone_number():
    phone_ = input("Input phone number: ")
    if Validation.is_phone_number(phone_):
        return phone_
    print("Invalid phone number!!!")
    return phone_number()


def availability():
    av = input("Input availability(hr/week): ")
    if Validation.is_availability(av):
        return int(av)
    print("Invalid hours!!!")
    return availability()


def salary():
    sal = input("Input salary: ")
    if Validation.is_salary(sal):
        return round(float(sal), 2)
    print("Invalid salary!!!")
    return salary()


def position():
    pos = Validation.get_valid_position(input("Input position: "))
    if pos is not None:
        return pos
    print("Invalid position!!!")
    return position()


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


freelancer_fields = {
    "_Freelancer__id": id,
    "_Freelancer__name": name,
    "_Freelancer__email": email,
    "_Freelancer__phone_number": phone_number,
    "_Freelancer__availability": availability,
    "_Freelancer__salary": salary,
    "_Freelancer__position": position,
}
