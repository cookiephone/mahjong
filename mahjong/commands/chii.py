from mahjong.commands.command import Command
from mahjong.melds import Meld, Mentsu


class CmdChii(Command):

    def __init__(self, player, tiles, called_player):
        super().__init__("chii")
        self.player = player
        self.tiles = tiles
        self.called_player = called_player

    def __call__(self, state):
        called_tile = self.called_player.discards.pop()
        meld = Meld(
            variant=Mentsu.MINJUN,
            tiles=self.tiles,
            called_tile=called_tile,
            called_player=self.called_player)
        self.player.called_melds.append(meld)

    def valid(self, state):
        return True  # TODO

    @staticmethod
    def build(positions):
        return []  # TODO
