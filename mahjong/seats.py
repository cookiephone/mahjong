class Seat(int):

    SEAT_STRINGS = {
        0: "east", 1: "south", 2: "west", 3: "north",
        4: "self", 5: "shimocha", 6: "toimen", 7: "kamicha",
    }

    def __new__(cls, value):
        return super().__new__(cls, value)
    
    def is_absolute(self):
        return self < 4
    
    def is_relative(self):
        return self >= 4

    def apply(self, relative):
        seat = (self + relative) % 4
        if self.is_relative():
            seat = seat + 4
        return seat

    def __add__(self, other):
        return self.__class__(super().__add__(other))
    
    def __mod__(self, other):
        return self.__class__(super().__mod__(other))

    def __str__(self):
        return self.__class__.SEAT_STRINGS[self]


Seat.EAST = Seat(0)
Seat.SOUTH = Seat(1)
Seat.WEST = Seat(2)
Seat.NORTH = Seat(3)

Seat.SELF = Seat(4)
Seat.SHIMOCHA = Seat(5)
Seat.TOIMEN = Seat(6)
Seat.KAMICHA = Seat(7)
