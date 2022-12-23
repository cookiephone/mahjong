class Hand:

    def __init__(self, round_wind, honba, wall, players, dealer):
        self.round_wind = round_wind
        self.honba = honba
        self.wall = wall
        self.players = players
        self.dealer = dealer

    def get_player(self, seat):
        for player in self.players:
            if player.seat == seat:
                return player
        raise ValueError(f"could not find player with seat {seat}")

    def bump_order(self, player):
        return [
            player,
            self.get_player(player.seat.SHIMOCHA),
            self.get_player(player.seat.TOIMEN),
            self.get_player(player.seat.KAMICHA)]
