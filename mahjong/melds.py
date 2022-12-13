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
        return {
            Mentsu.ANJUN: "chii (closed)",
            Mentsu.MINJUN: "chii (open)",
            Mentsu.ANKOU: "pon (closed)",
            Mentsu.MINKOU: "pon (open)",
            Mentsu.ANKAN: "kan (closed)",
            Mentsu.MINKAN: "kan (open)",
            Mentsu.SHOUMINKAN: "kan (open, added)",
        }[self]


class Meld:

    def __init__(self, variant=None, tiles=None, called_tile=None, called_player=None):
        self.variant = variant
        self.tiles = tiles
        self.called_tile = called_tile
        self.called_player = called_player

    def into_added_kan(self, tile):
        if Mentsu.MINKOU in self.variant:
            self.tiles.append(tile)
            self.variant = Mentsu.SHOUMINKAN

    def is_chii(self):
        return Mentsu.CHII in self.variant

    def is_pon(self):
        return Mentsu.PON in self.variant

    def is_kan(self):
        return Mentsu.KAN in self.variant

    def is_closed(self):
        return Mentsu.CLOSED in self.variant

    def is_open(self):
        return Mentsu.OPEN in self.variant

    def is_added(self):
        return Mentsu.ADDED in self.variant

    def __str__(self):
        return str(self.variant)

    def __repr__(self):
        return f"Meld({self.variant=}, {self.tiles=}, {self.called_tile=}, {self.called_player=})"
