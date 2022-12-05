class Player:
    
    def __init__(self, rule_context, seat):
        self.points = rule_context.starting_points
        self.seat = seat
        self.discards = []
        self.hand = []
        self.called_melds = []
