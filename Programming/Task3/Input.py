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
        return av
    print("Invalid hours!!!")
    return availability()


def salary():
    sal = input("Input salary: ")
    if Validation.is_salary(sal):
        return sal
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


def int_(message=""):
    n = input(message)
    if n.isdigit():
        return int(n)
    print("Invalid number!!!")
    return int_(message)
