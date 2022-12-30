from types import SimpleNamespace
from mahjong.seats import Seat


class Hand:

    def __init__(self, round_wind, honba, riichi_sticks, wall, players, dealer):
        self.round_wind = round_wind
        self.honba = honba
        self.riichi_sticks = riichi_sticks
        self.wall = wall
        self.players = players
        self.dealer = dealer
        self.abort = False
        self.result = None
        # TODO: dummy result, should be set by endhand command later
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
