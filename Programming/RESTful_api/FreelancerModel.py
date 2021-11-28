from init import *


class FreelancerModel(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    availability = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    position = db.Column(db.String(30), nullable=False)

    def __init__(self, id_, name, email, phone_number, availability, salary, position):
        self.id = id_
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.availability = availability  # hr/week
        self.salary = salary
        self.position = position


class FreelancerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'phone_number', 'availability', 'salary', 'position')
