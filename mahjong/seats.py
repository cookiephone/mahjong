from mahjong.tiles import Faces


STR_SEAT_EAST = "EAST"
STR_SEAT_SOUTH = "SOUTH"
STR_SEAT_WEST = "WEST"
STR_SEAT_NORTH = "NORTH"
STR_SEAT_SELF = "SELF"
STR_SEAT_SHIMOCHA = "SHIMOCHA"
STR_SEAT_TOIMEN = "TOIMEN"
STR_SEAT_KAMICHA = "KAMICHA"

STRS_ABSOLUTE_SEATS = [STR_SEAT_EAST, STR_SEAT_SOUTH, STR_SEAT_WEST, STR_SEAT_NORTH]
STRS_RELATIVE_SEATS = [STR_SEAT_SELF, STR_SEAT_SHIMOCHA, STR_SEAT_TOIMEN, STR_SEAT_KAMICHA]

NAME2ID = {
    STR_SEAT_EAST: 0, STR_SEAT_SOUTH: 1, STR_SEAT_WEST: 2, STR_SEAT_NORTH: 3, 
    STR_SEAT_SELF: 4, STR_SEAT_SHIMOCHA: 5, STR_SEAT_TOIMEN: 6, STR_SEAT_KAMICHA: 7
}
ID2NAME = {v: k for k, v in NAME2ID.items()}


class SeatType(type):

    def __getattr__(cls, name):
        if name in STRS_ABSOLUTE_SEATS:
            seat = cls.__new__(cls)
            seat.__init__(name)
            return seat
        raise AttributeError(name)


class Seat(metaclass=SeatType):

    def __init__(self, name):
        self.name = name
        self.id = NAME2ID[self.name]

    def __getattr__(self, name):
        if name in STRS_RELATIVE_SEATS:
            return Seat(ID2NAME[(self.id + NAME2ID[name]) % 4])
        raise AttributeError(name)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.name.lower()
