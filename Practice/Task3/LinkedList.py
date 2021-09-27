from random import choice


class LinkedList:
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None

        def assign(self, node):
            if type(node) is not type(self):
                raise TypeError
            self.data = node.data
            self.next = node.next

    def __init__(self, data):
        self.root = None
        self.__length = 0
        if data is not None:
            self.add(data)

    @classmethod
    def empty(cls):
        """Create empty list"""
        return cls(None)

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

    def add(self, data):
        """Add element at the front of list"""
        temp = self.root
        self.root = self.Node(data)
        if temp is not None:
            self.root.next = temp
        self.__length += 1

    def delete_at(self, index):
        """Delete element on "index" position"""
        current = self.__get_with_index(index)
        current.assign(current.next)
        self.__length -= 1

    def input_from_console(self, sep=" "):
        """Read element from console, divided by "sep=" """
        array = input()
        array = array.split(sep)
        self.append(array)

    def append(self, data):
        """Adds array of single object to front"""
        try:
            if len(data) >= 1:
                for i in reversed(data):
                    self.add(i)
        except TypeError:
            self.add(data)

    def append_random(self, size, range_):
        """Appends list with random values from "range_" """
        for i in range(size):
            self.add(choice(range_))

    def half_swap(self):
        """Swaps right and left sides of list"""
        if self.__length < 2:
            return
        middle = self.__get_with_index(self.__length // 2)  # divide right side
        end = self.__get_with_index(-1)  # get last element
        self.__get_with_index(self.__length // 2 - 1).next = None  # break the link between left and right
        end.next = self.root  # connect left part to the end of the right
        self.root = middle  # assign new root
