from abc import ABC, abstractmethod
from Logger import Logger


class Observer(ABC):

    @abstractmethod
    def update(self, observable, **kwargs):
        """Get update from subject"""
        pass


class ObserverLogger(Observer):
    def update(self, observable, **kwargs):
        Logger.Log(**kwargs)

