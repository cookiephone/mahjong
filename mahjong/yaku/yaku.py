from mahjong.utils.inheritdecoratormixin import InheritDecoratorMixin
from abc import ABC, abstractmethod
from functools import cache


class Yaku(ABC, metaclass=InheritDecoratorMixin):

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
    def applies(self, state, player):
        raise NotImplementedError
