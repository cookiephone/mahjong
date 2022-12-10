from mahjong.wall import Wall
from mahjong.seats import Seat
from mahjong.players import Player
from mahjong.tiles import Faces


class Hand:

    def __init__(self, state):
        self.wall = Wall(akadora=state.rule_context.aka_dora)
        self.wall.construct(state.rng)
        #TODO: consider state to compute the correct config for the next hand
        self.round_wind = Faces.EAST
        self.players = self._build_players(state)
        self.dealer = self._compute_dealer()

    #TODO: consider state to compute the correct config for the next hand
    def _build_players(self, state):
        players = []
        for seat in [Seat.EAST, Seat.SOUTH, Seat.WEST, Seat.NORTH]:
            player = Player(seat, state.rule_context.starting_points)
            players.append(player)
        return players

    def _compute_dealer(self):
        for player in self.players:
            if player.seat == Seat.EAST:
                return player

    def get_player(self, seat):
        for player in self.players:
            if player.seat == seat:
                return player
