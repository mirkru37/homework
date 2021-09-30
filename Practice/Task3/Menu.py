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
    except ValueError:
        return menu(template, data, greet_message, message_for_get)


def close(*_):
    exit()


def list_manually(*_):
    """Input linked list from console"""
    print("Please input separation element:")
    sep = input("-->")
    res = List.LinkedList.empty()
    print("Input elements: ")
    res.input_from_console(sep)
    return res


def list_from_range(*_):
    n = Input.input_upper_zero_num("Input N: ")
    range_ = [x for x in Input.input_range()]
    res = List.LinkedList.empty()
    res.append_random(n, range_)
    return res


def list_add(list_, *_):
    i = Input.input_upper_zero_num("Input i: ")
    data = input("Input element: ")
    try:
        list_.add_at(data, i)
    except ValueError as e:
        print(e)
        return list_add(list_)
    print(list_)
    menu(do, list_)


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


input_list = {
    "1": ("Generate from range", list_from_range),
    "2": ("Input manually", list_manually),
    "3": ("Exit", close)
}

do = {
    "1": ("Add to i", list_add),
    "2": ("Delete at i", list_delete),
    "3": ("Swap", list_swap),
    "4": ("Exit", close)
}
