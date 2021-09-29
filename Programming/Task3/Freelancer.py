import Validation
import Input


class Freelancer:
    __count_of_fields = 7

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
    def init_from_console(cls, message=""):
        if message:
            print(message)
        return cls(*Input.all_fields(Input.freelancer_fields))

    @classmethod
    def init_from_str(cls, str_):
        """init all data from str. Data must be separated by space"""
        str_ = str_.replace('\t', " ").split(" ")
        str_ = [i for i in str_ if i.strip()]  # remove spaces
        if len(str_) - 1 == cls.__count_of_fields:
            # case when split as [... "BE", "Developer"]
            str_[cls.__count_of_fields - 1:len(str_)] = [" ".join(str_[cls.__count_of_fields - 1:len(str_)])]
        if len(str_) != cls.__count_of_fields:
            raise ValueError("Invalid amount of data!!!")
        return cls(*str_)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not Validation.is_id(value):
            raise ValueError("Invalid ID")
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not Validation.is_name(value):
            raise ValueError("Invalid name")
        self.__name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not Validation.is_email(value):
            raise ValueError("Invalid email")
        self.__email = value

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        if not Validation.is_phone_number(value):
            raise ValueError("Invalid phone number")
        self.__phone_number = value

    @property
    def availability(self):
        return self.__availability

    @availability.setter
    def availability(self, value):
        if not Validation.is_availability(value):
            raise ValueError("Invalid availability")
        self.__availability = int(value)

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):
        if not Validation.is_salary(value):
            raise ValueError("Invalid Salary")
        self.__salary = round(float(value), 2)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        value = Validation.get_valid_position(value)
        if value is None:
            raise ValueError("Invalid Position")
        self.__position = value

    def get_all_fields(self):
        """returns all fields of class as array in initialization order"""
        return [x for x in vars(self).values()]
