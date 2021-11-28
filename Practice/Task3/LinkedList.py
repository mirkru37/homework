from abc import ABC, abstractmethod
from copy import copy, deepcopy
import CustomInput as Input
from random import choice
from Observable import Observable
from Observer import Observer


class AppendBehaviour(ABC):

    @abstractmethod
    def append(self, list_):
        pass


class AppendFromRange(AppendBehaviour):
    def append(self, list_):
        n = Input.input_index("Input N: ")
        range_ = [x for x in Input.input_range()]
        pos = Input.input_index("Input position: ")
        generator = list_.append_random(range_)
        list_before = deepcopy(list_)
        for _ in range(n):
            list_.add_at(next(generator), pos)
        list_after = list_
        list_.notify(action="Add from range", position=pos, elements_count=n,
                     list_before=list_before, list_after=list_after)


class AppendFromFile(AppendBehaviour):
    def append(self, list_):
        pos = Input.input_index("Input position: ")
        path = Input.input_file_path("Input file path: ")
        file = open(path)
        list_before = deepcopy(list_)
        for line in file.readlines():
            for i in line.split(" "):
                list_.add_at(i, pos)
        list_after = list_
        list_.notify(action="Add from file", position=pos, file_path=path,
                     list_before=list_before, list_after=list_after)


class LinkedList(Observable):
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None

        def assign(self, node):
            if type(node) is not type(self):
                raise TypeError
            self.data = node.data
            self.next = node.next

    def __init__(self, data=None):
        self.root = None
        self.__length = 0
        self.__iter_element = None
        self.__count_of_iter = 0
        self.__append_behaviour = AppendFromRange()
        self.__observers = []
        if data is not None:
            self.add(data)

    def __str__(self):
        res = []
        current = self.root
        while current is not None:
            res.append(current.data)
            current = current.next
        return str(res)

    def __getitem__(self, item):
        res = self.__get_with_index(item)
        return res.data

    def __setitem__(self, key, value):
        res = self.__get_with_index(key)
        res.data = value

    def __len__(self):
        return self.__length

    def __next__(self):
        if self.__count_of_iter < self.__length:
            self.__count_of_iter += 1
            if self.__iter_element is not None:
                self.__iter_element = self.__iter_element.next
            elif self.root:
                self.__iter_element = self.root
        else:
            self.__count_of_iter = 0
            self.__iter_element = None
            raise StopIteration
        return self.__iter_element.data

    def __iter__(self):
        return self

    def __get_with_index(self, index):
        index = self.__correct_index(index)
        res = self.root
        for i in range(index):
            res = res.next
        return res

    def __correct_index(self, index):
        if index < 0:
            index = self.__length + index
        if index >= self.__length:
            raise IndexError
        return index

    @property
    def length(self):
        """Returns length of list"""
        return self.__length

    @property
    def append_behaviour(self):
        return self.__append_behaviour

    @append_behaviour.setter
    def append_behaviour(self, behaviour):
        self.__append_behaviour = behaviour

    def add(self, data):
        """Add element at the front of list"""
        temp = self.root
        self.root = self.Node(data)
        if temp is not None:
            self.root.next = temp
        self.__length += 1

    def add_at(self, data, index):
        if 0 > index or index >= self.__length:
            if index == self.__length:
                if self.__length == 0:
                    self.add(data)
                else:
                    self.__get_with_index(index - 1).next = self.Node(data)
                    self.__length += 1
                return
            raise ValueError("Wrong index")
        tail = self.Node(self.__get_with_index(index).data)
        tail.next = self.__get_with_index(index).next
        current = self.root
        if index != 0:
            current = self.__get_with_index(index)
        current.assign(self.Node(data))
        current.next = tail
        self.__length += 1

    def delete_at(self, index):
        """Delete element on "index" position"""
        list_before = deepcopy(self)
        if index == self.__length - 1:
            self.__get_with_index(index - 1).next = None
        else:
            current = self.__get_with_index(index)
            current.assign(current.next)
        self.__length -= 1
        self.notify(action="Delete at position", position=index,
                    list_before=list_before, list_after=self)
    # def input_from_console(self, sep=" "):
    #     """Read element from console, divided by "sep=" """
    #     array = input()
    #     array = array.split(sep)
    #     self.append(array)

    def append(self):
        self.__append_behaviour.append(self)

    def delete_range(self, a, b):
        list_before = deepcopy(self)
        if b >= self.__length:
            raise ValueError("Incorrect value!!")
        if a == 0:
            self.root = self.__get_with_index(b).next
        else:
            self.__get_with_index(a - 1).next = self.__get_with_index(b).next
        self.notify(action="Delete range", begin=a, end=b,
                    list_before=list_before, list_after=self)

    @staticmethod
    def append_random(range_):
        """Appends list with random values from "range_" """
        while True:
            yield choice(range_)

    def half_swap(self):
        """Swaps right and left sides of list"""
        if self.__length < 2:
            return
        middle = self.__get_with_index(self.__length // 2)  # divide right side
        end = self.__get_with_index(-1)  # get last element
        self.__get_with_index(self.__length // 2 - 1).next = None  # break the link between left and right
        end.next = self.root  # connect left part to the end of the right
        self.root = middle  # assign new root

    def notify(self, **kwargs):
        for o in self.__observers:
            o.update(self, **kwargs)

    def registerObserver(self, observer: Observer):
        self.__observers.append(observer)

    def removeObserver(self, observer: Observer):
        self.__observers.remove(Observer)
