import Format
import Validation
import Input


class Freelancer:
    count_of_fields = 7

    def __init__(self, id_, name, email, phone_number, availability, salary, position):
        self.id = id_
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.availability = availability  # hr/week
        self.salary = salary
        self.position = position

    def __str__(self):
        return " ".join(str(i) for i in self.get_all_fields())

    @classmethod
    def init_default(cls):
        return cls("0000", "Name", "e@mail.com", "+380000000000", 0, 0, "devops")

    # @classmethod
    # def init_from_console(cls, message=""):
    #     if message:
    #         print(message)
    #     return cls(*Input.all_fields(Input.freelancer_fields))

    # @classmethod
    # def init_from_str(cls, str_):
    #     """init all data from str. Data must be separated by space"""
    #     str_ = str_.replace('\t', " ").split(" ")
    #     str_ = [i for i in str_ if i.strip()]  # remove spaces
    #     if len(str_) - 1 == cls.__count_of_fields:
    #         # case when split as [... "BE", "Developer"]
    #         str_[cls.__count_of_fields - 1:len(str_)] = [" ".join(str_[cls.__count_of_fields - 1:len(str_)])]
    #     if len(str_) != cls.__count_of_fields:
    #         raise ValueError("Invalid amount of data!!!")
    #     return cls(*str_)

    @property
    def id(self):
        return self.__id

    @id.setter
    @Validation.is_id
    def id(self, value):
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    @Validation.is_name
    def name(self, value):
        self.__name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    @Validation.is_email
    def email(self, value):
        self.__email = value

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    @Validation.is_phone_number
    def phone_number(self, value):
        self.__phone_number = value

    @property
    def availability(self):
        return self.__availability

    @availability.setter
    @Validation.is_availability
    def availability(self, value):
        self.__availability = int(value)

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    @Validation.is_salary
    def salary(self, value):
        self.__salary = round(float(value), 2)

    @property
    def position(self):
        return self.__position

    @position.setter
    @Validation.is_position
    def position(self, value):
        self.__position = Format.position(value)

    def get_all_fields(self):
        """returns all fields of class as array in initialization order"""
        return [x for x in vars(self).values()]
