STR_SEAT_EAST = "EAST"
STR_SEAT_SOUTH = "SOUTH"
STR_SEAT_WEST = "WEST"
STR_SEAT_NORTH = "NORTH"
STR_SEAT_SELF = "SELF"
STR_SEAT_SHIMOCHA = "SHIMOCHA"
STR_SEAT_TOIMEN = "TOIMEN"
STR_SEAT_KAMICHA = "KAMICHA"

ABSOLUTE_SEATS = {STR_SEAT_EAST, STR_SEAT_SOUTH, STR_SEAT_WEST, STR_SEAT_NORTH}
RELATIVE_SEATS = {STR_SEAT_SELF, STR_SEAT_SHIMOCHA, STR_SEAT_TOIMEN, STR_SEAT_KAMICHA}
SEATS = ABSOLUTE_SEATS | RELATIVE_SEATS

SEAT_PAIRINGS = {
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
    STR_SEAT_SELF: {
        STR_SEAT_SELF: STR_SEAT_SELF,
        STR_SEAT_SHIMOCHA: STR_SEAT_SHIMOCHA,
        STR_SEAT_TOIMEN: STR_SEAT_TOIMEN,
        STR_SEAT_KAMICHA: STR_SEAT_KAMICHA,
    },
    STR_SEAT_SHIMOCHA: {
        STR_SEAT_SELF: STR_SEAT_SHIMOCHA,
        STR_SEAT_SHIMOCHA: STR_SEAT_TOIMEN,
        STR_SEAT_TOIMEN: STR_SEAT_KAMICHA,
        STR_SEAT_KAMICHA: STR_SEAT_SELF,
    },
    STR_SEAT_TOIMEN: {
        STR_SEAT_SELF: STR_SEAT_TOIMEN,
        STR_SEAT_SHIMOCHA: STR_SEAT_KAMICHA,
        STR_SEAT_TOIMEN: STR_SEAT_SELF,
        STR_SEAT_KAMICHA: STR_SEAT_SHIMOCHA,
    },
    STR_SEAT_KAMICHA: {
        STR_SEAT_SELF: STR_SEAT_KAMICHA,
        STR_SEAT_SHIMOCHA: STR_SEAT_SELF,
        STR_SEAT_TOIMEN: STR_SEAT_SHIMOCHA,
        STR_SEAT_KAMICHA: STR_SEAT_TOIMEN,
    },
}

SEAT_PAIRINGS_INV = {s1: {s2: rel for rel, s2 in prs.items()} for s1, prs in SEAT_PAIRINGS.items()}


class SeatType(type):

    def __init__(cls, name, bases, attrs):
        for seatstr in SEATS:
            setattr(cls, seatstr, cls.__new__(cls))
            getattr(cls, seatstr).__init__(seatstr)
        super().__init__(name, bases, attrs)


class Seat(metaclass=SeatType):

    def __init__(self, name):
        self.name = name

    def __getattribute__(self, name):
        if name in SEATS:
            try:
                return getattr(self.__class__, SEAT_PAIRINGS[self.name][name])
            except KeyError as exception:
                seat_type = "absolute" if name in ABSOLUTE_SEATS else "relative"
                raise ValueError(f"cannot get {seat_type} seat of an absolute seat") from exception
        return super().__getattribute__(name)

    def __str__(self):
        return self.name.lower()

    def is_absolute(self):
        return self.name in ABSOLUTE_SEATS

    def relative(self, other):
        return getattr(self.__class__, SEAT_PAIRINGS_INV[self.name][other.name])
