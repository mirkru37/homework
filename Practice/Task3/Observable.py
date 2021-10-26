from abc import ABC, abstractmethod


class Observable(ABC):
    """Interface for observer subject"""

    @abstractmethod
    def notify(self, **kwargs):
        """Method to notify observer that state changed"""
        pass

    @abstractmethod
    def registerObserver(self, observer):
        """Add an observer to observers list """
        pass

    @abstractmethod
    def removeObserver(self, observer):
        """Remove an observer from observers list """
        pass
