import Menu
from Freelancer import Freelancer

a = Menu.menu(Menu.input_freelance_collection)
Menu.menu(Menu.all_ways, a)

# a = Freelancer.init_default()
#
# setattr(a, "id", "1234")
#
# for i, field in enumerate(vars(a).keys()):
#     print(field.split("__")[-1])
#
# print(Freelancer._Freelancer__count_of_fields)