STR_SEAT_EAST = "EAST"
STR_SEAT_SOUTH = "SOUTH"
STR_SEAT_WEST = "WEST"
STR_SEAT_NORTH = "NORTH"
STR_SEAT_SELF = "SELF"
STR_SEAT_SHIMOCHA = "SHIMOCHA"
STR_SEAT_TOIMEN = "TOIMEN"
STR_SEAT_KAMICHA = "KAMICHA"

RELATIVE_SEATS = {
    STR_SEAT_EAST: {
        STR_SEAT_SELF: STR_SEAT_EAST,
        STR_SEAT_SHIMOCHA: STR_SEAT_SOUTH,
        STR_SEAT_TOIMEN: STR_SEAT_WEST,
        STR_SEAT_KAMICHA: STR_SEAT_NORTH,
    },
    STR_SEAT_SOUTH: {
        STR_SEAT_SELF: STR_SEAT_SOUTH,
        STR_SEAT_SHIMOCHA: STR_SEAT_WEST,
        STR_SEAT_TOIMEN: STR_SEAT_NORTH,
        STR_SEAT_KAMICHA: STR_SEAT_EAST,
    },
    STR_SEAT_WEST: {
        STR_SEAT_SELF: STR_SEAT_WEST,
        STR_SEAT_SHIMOCHA: STR_SEAT_NORTH,
        STR_SEAT_TOIMEN: STR_SEAT_EAST,
        STR_SEAT_KAMICHA: STR_SEAT_SOUTH,
    },
    STR_SEAT_NORTH: {
        STR_SEAT_SELF: STR_SEAT_NORTH,
        STR_SEAT_SHIMOCHA: STR_SEAT_EAST,
        STR_SEAT_TOIMEN: STR_SEAT_SOUTH,
        STR_SEAT_KAMICHA: STR_SEAT_WEST,
    },
}


class SeatType(type):

    def __init__(cls, name, bases, attrs):
        setattr(cls, STR_SEAT_EAST, cls.__new__(cls))
        getattr(cls, STR_SEAT_EAST).__init__(STR_SEAT_EAST)
        setattr(cls, STR_SEAT_SOUTH, cls.__new__(cls))
        getattr(cls, STR_SEAT_SOUTH).__init__(STR_SEAT_SOUTH)
        setattr(cls, STR_SEAT_WEST, cls.__new__(cls))
        getattr(cls, STR_SEAT_WEST).__init__(STR_SEAT_WEST)
        setattr(cls, STR_SEAT_NORTH, cls.__new__(cls))
        getattr(cls, STR_SEAT_NORTH).__init__(STR_SEAT_NORTH)
        super().__init__(name, bases, attrs)


class Seat(metaclass=SeatType):

    def __init__(self, name):
        self.name = name

    def __getattr__(self, name):
        if name in [STR_SEAT_SELF, STR_SEAT_SHIMOCHA, STR_SEAT_TOIMEN, STR_SEAT_KAMICHA]:
            return getattr(self.__class__, RELATIVE_SEATS[self.name][name])
        raise AttributeError(name)

    def __str__(self):
        return self.name.lower()
