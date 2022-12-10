from mahjong.utils.inheritdecoratormixin import InheritDecoratorMixin
from abc import ABC, abstractmethod
from functools import cache


class Command(ABC, InheritDecoratorMixin):

    @abstractmethod
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def execute(self, state):
        raise NotImplementedError

    @abstractmethod
    @InheritDecoratorMixin.inheritable_decorator(cache)
    def valid(self, state):
        raise NotImplementedError
