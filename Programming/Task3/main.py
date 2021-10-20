import Menu
import Tools
from Freelancer import Freelancer
from FreelancerCollection import FreelancerCollection

if __name__ == "__main__":
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