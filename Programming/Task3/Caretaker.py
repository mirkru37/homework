from copy import deepcopy


class Caretaker:

    def __init__(self):
        self.__undo_stack = []
        self.__redo_stack = []
        self.__MAX_SIZE = 5

    def __save_to_redo(self, memento):
        self.__redo_stack.insert(0, deepcopy(memento))
        if len(self.__redo_stack) > self.__MAX_SIZE:
            self.__redo_stack.pop()

    def __save_to_undo(self, memento):
        self.__undo_stack.insert(0, deepcopy(memento))
        if len(self.__undo_stack) > self.__MAX_SIZE:
            self.__undo_stack.pop()

    def save(self, memento):
        self.__save_to_undo(memento)
        self.__redo_stack.clear()

    def undo(self, current):
        state = self.__undo_stack[0]
        self.__undo_stack.pop(0)
        self.__save_to_redo(current)
        return state

    def redo(self, current):
        state = self.__redo_stack[0]
        self.__redo_stack.pop(0)
        self.__save_to_undo(current)
        return state
