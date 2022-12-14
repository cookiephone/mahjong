from mahjong.melds import Mentsu


class Player:

    def __init__(self, seat, points):
        self.points = points
        self.seat = seat
        self.discards = []
        self.hand = []
        self.called_melds = []

    def drawn_tile(self):
        total_tiles = len(self.hand) + sum(len(meld.tiles) for meld in self.called_melds)
        n_kans = sum(1 for meld in self.called_melds if Mentsu.KAN in meld.variant)
        if total_tiles - n_kans > 13:
            return self.hand[-1]
        return None

    def __eq__(self, other):
        return self.seat == other.seat
