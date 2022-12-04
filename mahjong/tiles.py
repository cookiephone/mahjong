from enum import Flag, auto


class Faces(Flag):

    MAN1 = auto()
    MAN2 = auto()
    MAN3 = auto()
    MAN4 = auto()
    MAN5 = auto()
    MAN6 = auto()
    MAN7 = auto()
    MAN8 = auto()
    MAN9 = auto()

    PIN1 = auto()
    PIN2 = auto()
    PIN3 = auto()
    PIN4 = auto()
    PIN5 = auto()
    PIN6 = auto()
    PIN7 = auto()
    PIN8 = auto()
    PIN9 = auto()

    SOU1 = auto()
    SOU2 = auto()
    SOU3 = auto()
    SOU4 = auto()
    SOU5 = auto()
    SOU6 = auto()
    SOU7 = auto()
    SOU8 = auto()
    SOU9 = auto()

    HAKU = auto()
    HATSU = auto()
    CHUN = auto()

    EAST = auto()
    SOUTH = auto()
    WEST = auto()
    NORTH = auto()

    AKADORA = auto()

    MAN5_AKA = MAN5 | AKADORA
    PIN5_AKA = PIN5 | AKADORA
    SOU5_AKA = SOU5 | AKADORA

    MANZU = MAN1 | MAN2 | MAN3 | MAN4 | MAN5 | MAN6 | MAN7 | MAN8 | MAN9 | MAN5_AKA
    PINZU = PIN1 | PIN2 | PIN3 | PIN4 | PIN5 | PIN6 | PIN7 | PIN8 | PIN9 | PIN5_AKA
    SOUZU = SOU1 | SOU2 | SOU3 | SOU4 | SOU5 | SOU6 | SOU7 | SOU8 | SOU9 | SOU5_AKA
    DRAGONS = HAKU | HATSU | CHUN
    WINDS = EAST | SOUTH | WEST | NORTH
    TERMINALS = MAN1 | MAN9 | PIN1 | PIN9 | SOU1 | SOU9
    HONORS = DRAGONS | WINDS

    def __str__(self):
        FACE_STRINGS = {
            Faces.MAN1: "1 man", Faces.MAN2: "2 man", Faces.MAN3: "3 man", Faces.MAN4: "4 man", Faces.MAN5: "5 man", Faces.MAN6: "6 man", Faces.MAN7: "7 man", Faces.MAN8: "8 man", Faces.MAN9: "9 man",
            Faces.PIN1: "1 pin", Faces.PIN2: "2 pin", Faces.PIN3: "3 pin", Faces.PIN4: "4 pin", Faces.PIN5: "5 pin", Faces.PIN6: "6 pin", Faces.PIN7: "7 pin", Faces.PIN8: "8 pin", Faces.PIN9: "9 pin",
            Faces.SOU1: "1 sou", Faces.SOU2: "2 sou", Faces.SOU3: "3 sou", Faces.SOU4: "4 sou", Faces.SOU5: "5 sou", Faces.SOU6: "6 sou", Faces.SOU7: "7 sou", Faces.SOU8: "8 sou", Faces.SOU9: "9 sou",
            Faces.HAKU: "haku", Faces.HATSU: "hatsu", Faces.CHUN: "chun",
            Faces.EAST: "east", Faces.SOUTH: "south", Faces.WEST: "west", Faces.NORTH: "north",
            Faces.MAN5_AKA: "5 man aka", Faces.PIN5_AKA: "5 pin aka", Faces.SOU5_AKA: "5 sou aka",
        }
        return FACE_STRINGS[self]


class Tile():

    def __init__(self, face=None, uid=None):
        self.face = face
        self.uid = uid

    def matches(self, face):
        return self.face in face

    def is_manzu(self):
        return self.face in Faces.MANZU

    def is_pinzu(self):
        return self.face in Faces.PINZU

    def is_souzu(self):
        return self.face in Faces.SOUZU

    def is_dragon(self):
        return self.face in Faces.DRAGONS
    
    def is_wind(self):
        return self.face in Faces.WINDS

    def is_terminal(self):
        return self.face in Faces.TERMINALS

    def is_honor(self):
        return self.face in Faces.HONORS

    def is_akadora(self):
        return Faces.AKADORA in self.face

    def __str__(self):
        return str(self.face)

    def  __repr__(self):
        return f"Tile({self.uid=}, {self.face=})"
