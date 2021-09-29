import FreelancerCollection
import Input


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
    print("Sort by?")
    print("1-ID", "2-Name", "3-Email", "4-Phone", "5-Hours per week", "6-Salary", "7-Position", "...-back")
    option = get_menu_option()
    if option == "1":
        collection.sort(lambda a: a.id)
    elif option == "2":
        collection.sort(lambda a: a.name.lower())
    elif option == "3":
        collection.sort(lambda a: a.email.lower())
    elif option == "4":
        collection.sort(lambda a: a.phone_number)
    elif option == "5":
        collection.sort(lambda a: str(a.availability))
    elif option == "6":
        collection.sort(lambda a: str(a.salary))
    elif option == "7":
        collection.sort(lambda a: a.position.lower())
    menu(all_ways, collection)


def collection_delete(collection, *_):
    print("Delete by?")
    print("1-ID", "2-Name", "3-Email", "4-Phone", "5-Hours per week", "6-Salary", "7-Position", "...-back")
    option = get_menu_option()
    what = input("Input identifier: ")
    if option == "1":
        collection.delete(lambda a: a.id.lower() != what)
    elif option == "2":
        collection.delete(lambda a: a.name.lower() != what)
    elif option == "3":
        collection.delete(lambda a: a.email.lower() != what)
    elif option == "4":
        collection.delete(lambda a: a.phone_number != what)
    elif option == "5":
        collection.delete(lambda a: str(a.availability) != what)
    elif option == "6":
        collection.delete(lambda a: str(a.salary) != what)
    elif option == "7":
        collection.delete(lambda a: a.position.lower() != what)
    menu(all_ways, collection)


def collection_add(collection, *_):
    collection.read_from_console()
    menu(all_ways, collection)


def collection_edit(collection, *_):
    print("Input id of element to change")
    id_ = Input.id()
    index = collection.get_index(lambda f: f.id == id_)
    if index == -1:
        print("There is no such id!!!")
        menu(all_ways, collection)
        return
    print("Choose what to edit:")
    print("1-ID", "2-Name", "3-Email", "4-Phone", "5-Hours per week", "6-Salary", "7-Position", "...-back")
    option = get_menu_option()
    if option == "1":
        try:
            collection.edit(index, "id", Input.id())
        except ValueError as e:
            print(e)
            collection_edit(collection)
    elif option == "2":
        collection.edit(index, "name", Input.name())
    elif option == "3":
        collection.edit(index, "email", Input.email())
    elif option == "4":
        collection.edit(index, "phone", Input.phone_number())
    elif option == "5":
        collection.edit(index, "hours", Input.availability())
    elif option == "6":
        collection.edit(index, "salary", Input.salary())
    elif option == "7":
        collection.edit(index, "position", Input.position())
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
