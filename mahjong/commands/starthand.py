from mahjong.commands.command import Command
from mahjong.hand import Hand
from mahjong.seats import Seat
from mahjong.players import Player
from mahjong.tiles import Faces
from mahjong.wall import Wall


class CmdStartHand(Command):

    def __init__(self):
        super().__init__("start hand")

    # TODO: consider state to compute the correct config for the next hand
    def __call__(self, state):
        wall = self._build_wall(state)
        players = self._build_players(state)
        dealer = self._compute_dealer(players)
        hand = Hand(
            round_wind=Faces.EAST,
            honba=0,
            wall=wall,
            players=players,
            dealer=dealer)
        state.hands.append(hand)
        state.current_hand = hand

    def valid(self, state):
        return True  # TODO

    @staticmethod
    def _build_wall(state):
        wall = Wall(akadora=state.rule_context.aka_dora)
        wall.construct(state.rng)
        return wall

    # TODO: consider state to compute the correct config for the next hand
    @staticmethod
    def _build_players(state):
        players = []
        for seat in [Seat.EAST, Seat.SOUTH, Seat.WEST, Seat.NORTH]:
            player = Player(seat, state.rule_context.starting_points)
            players.append(player)
        return players

    @staticmethod
    def _compute_dealer(players):
        return next(player for player in players if player.seat == Seat.EAST)
