import mahjong.rules as rules
from mahjong.tiles import Faces
from mahjong.seats import Seat
from mahjong.wall import Wall
from mahjong.players import Player


class GameState:

    def __init__(self, seed=None, ruleset="default"):
        self.rule_context = rules.get_ruleset_context(ruleset)
        self.wall = Wall(seed, akadora=self.rule_context.aka_dora)
        self.round_wind = Faces.EAST
        self.players = []
        for seat in [Seat.EAST, Seat.SOUTH, Seat.WEST, Seat.NORTH]:
            player = Player(self.rule_context, seat)
            self.players.append(player)
        self.dealer = self.players[0]
        self.history = []
