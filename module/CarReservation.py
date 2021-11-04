from enum import Enum
from datetime import datetime
import Validation


class Car(Enum):
    Audi_A3 = 'Audi_A3'
    BMW_X1 = 'BMW_X1'
    Toyota_Yaris = 'Toyota_Yaris'
    Volkswagen_T_Roc = 'Volkswagen_T-Roc'
    Ford_Fiesta = 'Ford_Fiesta'
    Honda_Civic = 'Honda_Civic'
    Volkswagen_Golf = 'Volkswagen_Golf'


class CarReservation:

    def __init__(self, id_: int, car: str, start_datetime: datetime, end_datetime: datetime, name: str, price: float):
        self.id = id_
        self.car = car
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.name = name
        self.price = price

    @property
    def id(self):
        return self.__id

    @id.setter
    @Validation.is_int
    def id(self, value):
        self.__id = value

    @property
    def car(self):
        return self.__car

    @car.setter
    @Validation.is_in_enum(Car)
    def car(self, val):
        self.__car = val

    @property
    def start_datetime(self):
        return self.__start_datetime

    @start_datetime.setter
    @Validation.is_date
    @Validation.is_date_less(datetime.today())
    def start_datetime(self, val):
        self.__start_datetime = val

    @property
    def end_datetime(self):
        return self.__end_datetime

    @end_datetime.setter
    @Validation.is_date
    def end_datetime(self, val):
        valid = Validation.is_date_less(self.__start_datetime)
        valid = valid(None)
        if valid(self, val):
            self.__end_datetime = val

    @property
    def name(self):
        return self.__name

    @name.setter
    @Validation.is_letters_only
    def name(self, value):
        self.__name = value

    @property
    def price(self):
        return self.__name

    @price.setter
    @Validation.is_number
    def price(self, value):
        self.__price = round(float(value), 2)
