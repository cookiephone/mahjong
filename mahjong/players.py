class Player:

    def __init__(self, seat, points):
        self.points = points
        self.seat = seat
        self.discards = []
        self.hand = []
        self.called_melds = []

    def __eq__(self, other):
        return self.seat == other.seat
