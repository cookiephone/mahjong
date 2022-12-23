from mahjong.commands.command import Command
from mahjong.hand import Hand
from mahjong.seats import Seat
from mahjong.players import Player
from mahjong.tiles import Faces
from mahjong.wall import Wall


class CmdStartHand(Command):

    def __init__(self):
        super().__init__("start hand")

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

    @staticmethod
    def _build_players(state):
        players = []
        if not state.hands:
            seats = [Seat.EAST, Seat.SOUTH, Seat.WEST, Seat.NORTH]
            return [Player(seat, state.rule_context.starting_points) for seat in seats]
        # TODO: consider state to compute the correct config for the next hand
        # e.g. rotate seats (seat.KAMICHA) if draw with dealer tenpai or dealer win
        for player in state.current_hand.players:
            players.append(Player(player.seat, player.points))
        return players

    @staticmethod
    def _compute_dealer(players):
        return next(player for player in players if player.seat == Seat.EAST)
