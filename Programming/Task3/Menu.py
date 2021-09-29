import FreelancerCollection
import Input
import Tools


def get_menu_option(message=""):
    if message:
        print(message)
    return input("-->").strip()


def invalid_option(*_):
    print("Invalid choice!!")
    raise ValueError("Invalid menu option")


def menu(template, data=None, greet_message='', message_for_get=''):
    if greet_message:
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


def input_manually(*_):
    res = FreelancerCollection.FreelancerCollection()
    res.read_from_console()
    return res


def input_from_file(*_):
    path = Input.file_path("Input file path: ")
    res = FreelancerCollection.FreelancerCollection()
    res.read_from_file(path)
    return res


def collection_find(collection, *_):
    res = collection.find_all(input("Input search parameter: "))
    if not res:
        print("There is no such data")
        menu(all_ways, collection)
        return
    print("Search results:")
    for i in res:
        print(i)
    menu(all_ways, collection)


def collection_show(collection, *_):
    print(collection)
    menu(all_ways, collection)


def collection_sort(collection, *_):
    if len(collection) != 0:
        print("Sort by?")
        i, option = get_menu_option_and_fields(collection[0])
        if option == i:
            exit()
        collection.sort(lambda b: str(Tools.get_attr(b, option-1)).lower() if
                                      type(Tools.get_attr(b, option-1)) is str
                                      else Tools.get_attr(b, option-1))
    else:
        print("Empty list!!!")
    menu(all_ways, collection)


def collection_delete(collection, *_):
    if len(collection) != 0:
        print("Delete by?")
        i, option = get_menu_option_and_fields(collection[0])
        if option == i:
            exit()
        what = input("Input value: ")
        collection.delete(lambda b: str(Tools.get_attr(b, option - 1)).lower() != what.lower())
    else:
        print("Empty list!!!")
    menu(all_ways, collection)


def collection_add(collection, *_):
    collection.read_from_console()
    menu(all_ways, collection)


def get_menu_option_and_fields(val):
    i = Tools.print_fields(val) + 1
    print(f"{i}-Back")
    option = Input.between(1, i, "-->")
    return i, option


def collection_edit(collection, *_):
    print("Input id of element to change")
    id_ = Input.id()
    index = collection.get_index(lambda f: f.id == id_)
    if index == -1:
        print("There is no such id!!!")
        menu(all_ways, collection)
        return
    print("Choose what to edit:")
    i, option = get_menu_option_and_fields(collection[0])
    if option != i:
        try:
            collection.edit(index, Tools.get_attr_name(collection[0], option-1))
        except ValueError as e:
            print(e)
            collection_edit(collection)
    menu(all_ways, collection)


def connect_to_file(collection, *_):
    path = Input.file_path("Input path: ")
    collection.link_to_file(path)
    menu(all_ways, collection)


def disconnect_to_file(collection, *_):
    collection.unlink_from_file()
    menu(all_ways, collection)


input_freelance_collection = {
    "1": ("Input manually", input_manually),
    "2": ("Input from file", input_from_file),
    "3": ("Exit", exit)
}

all_ways = {
    "1": ("Show", collection_show),
    "2": ("Find", collection_find),
    "3": ("Sort", collection_sort),
    "4": ("Delete elements", collection_delete),
    "5": ("Add elements", collection_add),
    "6": ("Edit element", collection_edit),
    "7": ("Connect to file", connect_to_file),
    "8": ("Disconnect to file", disconnect_to_file),
    "9": ("Exit", close)
}
