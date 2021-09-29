import Freelancer
import Input
from fuzzywuzzy import fuzz


class FreelancerCollection:

    def __init__(self):
        self.__file = None
        self.__link_to_file = False
        self.__freelancers = []

    def __str__(self):
        if not self.__freelancers:
            return "There is no elements yet"
        str_ = "ID\tName\tEmail\tPhone number\thr/week\tsalary\tposition"
        for i in self.__freelancers:
            str_ += "\n" + str(i)
        return str_

    def __getitem__(self, item):
        return self.__freelancers[item]

    def add(self, freelancer):
        if type(freelancer) != Freelancer.Freelancer:
            if type(freelancer) == str:
                freelancer = Freelancer.Freelancer.init_from_str(freelancer)
            else:
                raise ValueError("Invalid input data!!!")
        IDs = [i.id for i in self.__freelancers]
        if freelancer.id in IDs:
            raise ValueError("There already is a member with such ID")
        self.__freelancers.append(freelancer)
        if self.__link_to_file:
            self.__file.write(str(freelancer) + "\n")

    def read_from_file(self, path):
        file = open(path)
        line = file.readline().rstrip()
        unread = 0
        lines_count = 0
        while line:
            lines_count += 1
            try:
                self.add(line)
            except ValueError:
                unread += 1
            line = file.readline().rstrip()
        if unread:
            print(f"{unread} of {lines_count} was ignored")
        file.close()

    def read_from_console(self):
        n = Input.upper(0, "Input count of elements: ")
        print("ID\tName\tEmail\tPhone number\thr/week\tsalary\tposition")
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
        return res

    def sort(self, compare=lambda a: a.id):
        self.__freelancers = sorted(self.__freelancers, key=compare)
        self.update_file()

    def delete(self, exception):
        self.__freelancers = list(filter(exception, self.__freelancers))
        self.update_file()

    def get_index(self, where):
        """return index of element we want to edit"""
        for i, freelancer in enumerate(self.__freelancers):
            if where(freelancer):
                return i
        return -1

    def edit(self, index, what, value):
        if what == "id":
            IDs = [i.id for i in self.__freelancers]
            if value in IDs:
                raise ValueError("There already is a member with such ID")
            self.__freelancers[index].id = value
        elif what == "name":
            self.__freelancers[index].name = value
        elif what == "email":
            self.__freelancers[index].email = value
        elif what == "phone":
            self.__freelancers[index].phone_number = value
        elif what == "hours":
            self.__freelancers[index].availability = value
        elif what == "salary":
            self.__freelancers[index].salary = value
        elif what == "position":
            self.__freelancers[index].position = value
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

    def __clear_file(self):
        self.__file.seek(0)
        self.__file.truncate()
