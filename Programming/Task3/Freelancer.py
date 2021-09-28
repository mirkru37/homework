class Freelancer:

    def __inti__(self, id_, name, email, phone_number, availability, salary, position):
        self.id = id_
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.availability = availability
        self.salary = salary
        self.position = position

    @property
    def id(self):
        return self.id

    @id.setter
    def id(self, value):
        # valid
        self.id = value

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, value):
        # valid
        self.name = value

    @property
    def email(self):
        return self.email

    @email.setter
    def email(self, value):
        # valid
        self.email = value

    @property
    def phone_number(self):
        return self.phone_number

    @phone_number.setter
    def phone_number(self, value):
        # valid
        self.phone_number = value

    @property
    def availability(self):
        return self.availability

    @availability.setter
    def availability(self, value):
        # valid
        self.availability = value

    @property
    def salary(self):
        return self.salary

    @salary.setter
    def salary(self, value):
        # valid
        self.salary = value

    @property
    def position(self):
        return self.position

    @position.setter
    def position(self, value):
        # valid
        self.position = value