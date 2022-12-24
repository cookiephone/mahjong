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
        hand = CmdStartHand._make_hand(state)
        state.hands.append(hand)
        state.current_hand = hand

    def valid(self, state):
        return True  # TODO

    @staticmethod
    def _make_hand(state):
        if not state.hands:
            return CmdStartHand._make_initial_hand(state)
        rotation = not CmdStartHand._is_renchan(state)
        honba = state.current_hand.honba + 1
        round_wind = state.current_hand.round_wind
        if rotation:
            honba = 0
            if state.round == 4:
                round_wind = round_wind.SHIMOCHA
        wall = CmdStartHand._build_wall(state)
        players = CmdStartHand._build_players(state, rotation)
        dealer = CmdStartHand._compute_dealer(players)
        return Hand(
            round_wind=round_wind,
            honba=honba,
            wall=wall,
            players=players,
            dealer=dealer)

    @staticmethod
    def _make_initial_hand(state):
        wall = CmdStartHand._build_wall(state)
        seats = [Seat.EAST, Seat.SOUTH, Seat.WEST, Seat.NORTH]
        players = [Player(seat, state.rule_context.starting_points) for seat in seats]
        dealer = CmdStartHand._compute_dealer(players)
        return Hand(
            round_wind=Faces.EAST,
            honba=0,
            wall=wall,
            players=players,
            dealer=dealer)

    @staticmethod
    def _is_renchan(state):
        return False  # TODO

    @staticmethod
    def _build_wall(state):
        wall = Wall(akadora=state.rule_context.aka_dora)
        wall.construct(state.rng)
        return wall

    @staticmethod
    def _build_players(state, rotation):
        players = []
        for player in state.current_hand.players:
            seat = player.seat.KAMICHA if rotation else player.seat
            players.append(Player(seat, player.points))
        return players

    @staticmethod
    def _compute_dealer(players):
        return next(player for player in players if player.seat == Seat.EAST)
