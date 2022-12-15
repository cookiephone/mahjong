from abc import ABC, abstractmethod
from functools import cache
from mahjong.utils.inheritdecoratormixin import InheritDecoratorMixin


class Yaku(ABC, InheritDecoratorMixin):

    @property
    @abstractmethod
    def name_full(self):
        pass

    @property
    @abstractmethod
    def name_short(self):
        pass

    @property
    @abstractmethod
    def name_en(self):
        pass

    @property
    @abstractmethod
    def value_open(self):
        pass

    @property
    @abstractmethod
    def value_closed(self):
        pass

    @property
    @abstractmethod
    def yakuman(self):
        pass

    @property
    @abstractmethod
    def disables(self):
        pass

    @property
    @abstractmethod
    def enables(self):
        pass

    @abstractmethod
    @InheritDecoratorMixin.inheritable_decorator(cache)
    @staticmethod
    def applies(state, player):
        raise NotImplementedError
