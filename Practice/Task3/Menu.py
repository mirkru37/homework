import LinkedList as List
import CustomInput as Input


def get_menu_option(message=""):
    print(message)
    return input("-->").strip()


def invalid_option(*_):
    print("Invalid choice!!")
    raise ValueError("Invalid menu option")


def menu(template, data=None, greet_message='', message_for_get=''):
    print(greet_message)
    for key in template:
        print(f"{key}: {template[key][0]}")
    option = get_menu_option(message_for_get)
    try:
        return template.get(option, [None, invalid_option])[1](data)
    except ValueError as e:
        print(e)
        return menu(template, data, greet_message, message_for_get)


def close(*_):
    exit()


# def list_manually(*_):
#     """Input linked list from console"""
#     print("Please input separation element:")
#     sep = input("-->")
#     res = List.LinkedList.empty()
#     print("Input elements: ")
#     res.input_from_console(sep)
#     return res


# def list_from_range(*_):
#     n = Input.input_upper_zero_num("Input N: ")
#     range_ = [x for x in Input.input_range()]
#     res = List.LinkedList.empty()
#     generator = res.append_random(range_)
#     for _ in range(n):
#         next(generator)
#     return res


# def list_add(list_, *_):
#     i = Input.input_upper_zero_num("Input i: ")
#     data = input("Input element: ")
#     try:
#         list_.add_at(data, i)
#     except ValueError as e:
#         print(e)
#         return list_add(list_)
#     print(list_)
#     menu(do, list_)


def list_delete(list_, *_):
    i = Input.input_index("Input i: ")
    try:
        list_.delete_at(i)
    except IndexError as e:
        print("Invalid index!!!")
        return list_delete(list_)
    print(list_)
    menu(do, list_)


def list_swap(list_, *_):
    print("Before: ", list_)
    list_.half_swap()
    print("After: ", list_)
    menu(do, list_)


# input_list = {
#     "1": ("Generate from range", list_from_range),
#     "2": ("Input manually", list_manually),
#     "3": ("Exit", close)
# }

def list_choose_append_with_range(list_, *_):
    list_.append_behaviour = List.AppendFromRange()
    print("Strategy selected!!")
    menu(do, list_)


def list_append(list_, *_):
    list_.append()
    menu(do, list_)


def list_delete_range(list_, *_):
    a = Input.input_index("Input A:")
    b = Input.input_index("Input B:")
    if a > b:
        a, b = b, a
    list_.delete_range(a, b)
    menu(do, list_)


def list_choose_append_from_file(list_, *_):
    list_.append_behaviour = List.AppendFromFile()
    print("Strategy selected!!")
    menu(do, list_)


def list_show(list_, *_):
    print(list_)
    menu(do, list_)


do = {
    # "1": ("Add to i", list_add),
    # "2": ("Delete at i", list_delete),
    # "3": ("Swap", list_swap),
    # "4": ("Exit", close)
    "1": ("Choose append with range(default)", list_choose_append_with_range),
    "2": ("Choose append from file", list_choose_append_from_file),
    "3": ("Append", list_append),
    "4": ("Delete at i", list_delete),
    "5": ("Delete at range", list_delete_range),
    "6": ("Swap", list_swap),
    "7": ("Show", list_show),
    "8": ("Exit", close)
}
