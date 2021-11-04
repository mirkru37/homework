from datetime import datetime

from CarReservation import CarReservation, Car


class CarReservationCollection:

    def __init__(self):
        self.__reservations = []

    def __str__(self):
        res = ''
        for val in self.__reservations:
            res += str(val) + '\n'
        return res

    def add(self, res: CarReservation):
        for reser in self.__reservations:
            if reser.car == res.car:
                if res.start_datetime < reser.end_datetime < res.end_datetime or res.start_datetime < reser.start_datetime < res.end_datetime:
                    raise ValueError('Invalid date')
            if reser.id == res.id:
                raise ValueError('Invalid id')
        self.__reservations.append(res)

    def read_file(self, path):
        file = open(path)
        line = file.readline().rstrip()
        while line:
            vals = line.split(' ')
            id = int(vals[0])
            car = vals[1]
            start = datetime.strptime(vals[2], '%Y/%m/%d')
            end = datetime.strptime(vals[3], '%Y/%m/%d')
            name = vals[4]
            price = float(vals[5])
            self.add(CarReservation(id, car, start, end, name, price))
            line = file.readline().rstrip()