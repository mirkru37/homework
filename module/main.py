from CarReservation import CarReservation, Car
from CarReservationCollection import CarReservationCollection
from datetime import datetime

if __name__ == "__main__":
    #a = CarReservation(1223, 'Audi_A3', datetime(2021, 10, 4), datetime(2021, 10, 4),'a', 1)
    list_ = CarReservationCollection
    list_.read_file(list_, "Cars.txt")
    #print(list_)
    #print(type(datetime.today()))  