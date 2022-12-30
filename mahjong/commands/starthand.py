from functools import cache
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
        round_wind = CmdStartHand._compute_round_wind(state)
        honba = CmdStartHand._compute_honba(state)
        riichi_sticks = CmdStartHand._compute_riichi_sticks(state)
        wall = CmdStartHand._build_wall(state)
        players = CmdStartHand._build_players(state)
        dealer = CmdStartHand._compute_dealer(players)
        return Hand(
            round_wind=round_wind,
            honba=honba,
            riichi_sticks=riichi_sticks,
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
            riichi_sticks=0,
            wall=wall,
            players=players,
            dealer=dealer)

    @staticmethod
    def _compute_round_wind(state):
        if CmdStartHand._is_rotation(state) and state.round == 4:
            return state.current_hand.round_wind.SHIMOCHA
        return state.current_hand.round_wind

    @staticmethod
    def _compute_riichi_sticks(state):
        if CmdStartHand._is_riichi_stick_reset(state):
            return 0
        return state.current_hand.riichi_sticks

    @staticmethod
    def _compute_honba(state):
        if CmdStartHand._is_honba_reset(state):
            return 0
        return state.current_hand.honba + 1

    @cache
    @staticmethod
    def _is_rotation(state):
        return (
            not CmdStartHand._is_dealer_win(state)
            or (
                state.current_hand.result.exhaustive_draw
                and not state.current_hand.result.tenpai[Seat.East]
            )
        )

    @staticmethod
    def _is_honba_reset(state):
        return (
            not CmdStartHand._is_dealer_win(state)
            and not state.current_hand.result.exhaustive_draw
            and not state.current_hand.result.aboritve_draw
        )

    @staticmethod
    def _is_riichi_stick_reset(state):
        return state.current_hand.result.winner is not None

    @cache
    @staticmethod
    def _is_dealer_win(state):
        return state.current_hand.result.winner and state.current_hand.result.winner.is_dealer()

    @staticmethod
    def _build_wall(state):
        wall = Wall(akadora=state.rule_context.aka_dora)
        wall.construct(state.rng)
        return wall

    @staticmethod
    def _build_players(state):
        players = []
        for player in state.current_hand.players:
            seat = player.seat.KAMICHA if CmdStartHand._is_rotation(state) else player.seat
            players.append(Player(seat, player.points))
        return players

    @staticmethod
    def _compute_dealer(players):
        return next(player for player in players if player.seat == Seat.EAST)
