from abc import ABC, abstractmethod


class Command(ABC):

    @abstractmethod
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def execute(self, state):
        raise NotImplementedError

    @abstractmethod
    def valid(self, state):
        raise NotImplementedError
