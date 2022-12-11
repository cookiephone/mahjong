from abc import ABC, abstractmethod


class Yaku(ABC):

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
