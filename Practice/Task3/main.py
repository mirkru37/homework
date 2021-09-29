import LinkedList as List
import Menu


list_ = Menu.menu(Menu.input_list)
print("Before: ", list_)
list_.half_swap()
print("After: ", list_)
Menu.menu(Menu.do, list_)
