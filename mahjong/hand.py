from types import SimpleNamespace
from typing import Any
from dataclasses import dataclass
from mahjong.seats import Seat


@dataclass
class Hand:

    round_wind: Any
    honba: Any
    riichi_sticks: Any
    wall: Any
    players: Any
    dealer: Any
    abort: Any = False
    result: Any = None


    # TODO: dummy result, should be set by endhand command later
    def __post_init__(self):
        self.result = SimpleNamespace(
            abortive_draw=False,
            exhaustive_draw=False,
            winner=self.players[1],
            tenpai={
                Seat.EAST: False,
                Seat.SOUTH: False,
                Seat.WEST: False,
                Seat.NORTH: False,
            }
        )

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
