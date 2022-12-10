from enum import Flag, auto


class Mentsu(Flag):

    CHII = auto()
    PON = auto()
    KAN = auto()

    OPEN = auto()
    CLOSED = auto()

    ADDED = auto()

    ANJUN = CHII | CLOSED
    MINJUN = CHII | OPEN

    ANKOU = PON | CLOSED
    MINKOU = PON | OPEN

    ANKAN = KAN | CLOSED
    MINKAN = KAN | OPEN
    SHOUMINKAN = KAN | OPEN | ADDED

    def __str__(self):
        MENTSU_STRINGS = {
            Mentsu.ANJUN: "chii (closed)",
            Mentsu.MINJUN: "chii (open)",
            Mentsu.ANKOU: "pon (closed)",
            Mentsu.MINKOU: "pon (open)",
            Mentsu.ANKAN: "kan (closed)",
            Mentsu.MINKAN: "kan (open)",
            Mentsu.SHOUMINKAN: "kan (open, added)",
        }
        return MENTSU_STRINGS[self]


class Meld:

    def __init__(self, type=None, tiles=None, called_tile=None, called_player=None):
        self.type = type
        self.tiles = tiles
        self.called_tile = called_tile
        self.called_player = called_player

    def into_added_kan(self, tile):
        if Mentsu.MINKOU in self.type:
            self.tiles.append(tile)
            self.type = Mentsu.SHOUMINKAN

    def is_chii(self):
        return Mentsu.CHII in self.type
    
    def is_pon(self):
        return Mentsu.PON in self.type
    
    def is_kan(self):
        return Mentsu.KAN in self.type

    def is_closed(self):
        return Mentsu.CLOSED in self.type

    def is_open(self):
        return Mentsu.OPEN in self.type

    def is_added(self):
        return Mentsu.ADDED in self.type

    def __str__(self):
        return str(self.type)

    def __repr__(self):
        return f"Meld({self.type=}, {self.tiles=}, {self.called_tile=}, {self.called_player=})"
