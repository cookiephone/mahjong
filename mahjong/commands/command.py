from abc import ABC, abstractmethod
from functools import cache
from mahjong.utils.inheritdecoratormixin import InheritDecoratorMixin


class Command(ABC, InheritDecoratorMixin):

    @abstractmethod
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def __call__(self, state):
        raise NotImplementedError

    @abstractmethod
    @InheritDecoratorMixin.inheritable_decorator(cache)
    def valid(self, state):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def build(positions):
        raise NotImplementedError
