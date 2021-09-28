import Freelancer
import Input


class FreelancerCollection:

    def __init__(self):
        self.freelancers = []

    def __str__(self):
        if not self.freelancers:
            return "There is no elements yet"
        str_ = "ID\tName\tEmail\tPhone number\thr/week\tsalary\tposition"
        for i in self.freelancers:
            str_ += "\n" + str(i)
        return str_

    def add(self, freelancer):
        if type(freelancer) != Freelancer.Freelancer:
            if type(freelancer) == str:
                freelancer = Freelancer.Freelancer.init_from_str(freelancer)
            else:
                raise ValueError("Invalid input data!!!")
        IDs = [i.id for i in self.freelancers]
        if freelancer.id in IDs:
            raise ValueError("There already is a member with such ID")
        self.freelancers.append(freelancer)

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
                self.add(input(f"Enter element {i+1}: "))
                i += 1
            except ValueError as e:
                print(e)

