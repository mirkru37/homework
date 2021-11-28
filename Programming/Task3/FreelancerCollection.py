from copy import deepcopy
import Format
import Freelancer
import Input
from Memento import Memento
from Caretaker import Caretaker
from fuzzywuzzy import fuzz


class FreelancerCollection:

    def __init__(self):
        self.__file = None
        self.__link_to_file = False
        self.__freelancers = []
        self.__caretaker_freelancers = Caretaker()
        self.__save_exceptions = ["_FreelancerCollection__caretaker_freelancers", "_FreelancerCollection__file",
                                  "_FreelancerCollection__link_to_file"]

    def __str__(self):
        if not self.__freelancers:
            return "There is no elements yet"
        str_ = ""
        for i in vars(self.__freelancers[0]).keys():
            str_ += i.split("__")[-1].capitalize() + "\t"
        for i in self.__freelancers:
            str_ += "\n" + str(i)
        return str_

    def __getitem__(self, item):
        return self.__freelancers[item]

    def __len__(self):
        return len(self.__freelancers)

    def __eq__(self, other):
        if len(self.__freelancers) != len(other.__freelancers):
            return False
        for s, o in zip(self.__freelancers, other.__freelancers):
            if str(s) != str(o):
                return False
        return True

    def add(self, freelancer):
        self.save()
        if type(freelancer) != Freelancer.Freelancer:
            if type(freelancer) == str:
                dummy = Freelancer.Freelancer.init_default()
                freelancer = Format.freelancer_fields(freelancer)
                if len(freelancer) != dummy.count_of_fields:
                    raise ValueError("Invalid amount of data!!!")
                exception_message = ""
                for i, field in enumerate(vars(dummy).keys()):
                    try:
                        setattr(dummy, field.split("__")[-1], freelancer[i])
                    except ValueError as e:
                        exception_message += str(e) + "\n"
                if exception_message:
                    raise ValueError(exception_message)
                freelancer = dummy
            else:
                raise ValueError("Invalid input data!!!")
        IDs = [i.id for i in self.__freelancers]
        if freelancer.id in IDs:
            raise ValueError("There already is a member with such ID")
        self.__freelancers.append(freelancer)
        if self.__link_to_file:
            self.__file.write(str(freelancer) + "\n")

    def add_from_array(self, array):
        for f in array:
            self.add(f)

    def read_from_file(self, path):
        file = open(path)
        line = file.readline().rstrip()
        lines_count = 0
        while line:
            lines_count += 1
            try:
                self.add(line)
            except ValueError as e:
                print(f"Error at line {lines_count}\n", e)
            line = file.readline().rstrip()
        file.close()

    def read_from_console(self):
        n = Input.upper(0, "Input count of elements: ")
        str_ = ""
        for i in vars(Freelancer.Freelancer.init_default()).keys():
            str_ += i.split("__")[-1].capitalize() + "\t"
        print(str_)
        i = 0
        while i < n:
            try:
                self.add(input(f"Enter element {i + 1}: "))
                i += 1
            except ValueError as e:
                print(e)

    def find_all(self, val, ratio=80):
        res = []
        for i in self.__freelancers:
            fields = i.get_all_fields()
            for j in fields:
                if fuzz.partial_ratio(str(j).lower(), str(val).lower()) >= ratio:
                    res.append(str(i))
                    break
        return res

    def sort(self, compare=lambda a: a.id):
        self.save()
        self.__freelancers = sorted(self.__freelancers, key=compare)
        self.update_file()

    def delete(self, exception):
        self.save()
        self.__freelancers = list(filter(exception, self.__freelancers))
        self.update_file()

    def get_index(self, where):
        """return index of element we want to edit
            where is a lambda for comparison
        """
        for i, freelancer in enumerate(self.__freelancers):
            if where(freelancer):
                return i
        return -1

    def edit(self, index, what, value=None):
        self.save()
        if not value:
            value = Input.field(Input.freelancer_fields, what)
        if what == "_Freelancer__id":
            IDs = [i.id for i in self.__freelancers]
            if value in IDs:
                raise ValueError("There already is a member with such ID")
        setattr(self.__freelancers[index], what, value)
        self.update_file()

    def link_to_file(self, path):
        self.__file = open(path, "a")
        self.__link_to_file = True
        self.update_file()

    def unlink_from_file(self):
        if self.__file:
            self.__file.close()
            self.__link_to_file = False

    def update_file(self):
        if self.__link_to_file:
            self.__clear_file()
            for i in self.__freelancers:
                self.__file.write(str(i) + "\n")

    def save(self):
        items_to_save = self.__get_attrs_to_save()
        self.__caretaker_freelancers.save(Memento(**items_to_save))

    def undo(self):
        items_to_save = self.__get_attrs_to_save()
        try:
            previous = self.__caretaker_freelancers.undo(Memento(**items_to_save))
        except IndexError:
            print("The undo stack is empty")
            return
        self.__dict__.update(vars(previous))
        self.update_file()

    def redo(self):
        items_to_save = self.__get_attrs_to_save()
        try:
            previous = self.__caretaker_freelancers.redo(Memento(**items_to_save))
        except IndexError:
            print("The undo stack is empty")
            return
        self.__dict__.update(vars(previous))
        self.update_file()

    def __clear_file(self):
        self.__file.seek(0)
        self.__file.truncate()

    def __get_attrs_to_save(self):
        res = {x: vars(self)[x] for x in vars(self) if x not in self.__save_exceptions} # problem with copy of not None file !!!!
        return res
