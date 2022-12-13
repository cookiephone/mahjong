from mahjong.commands.command import Command
from mahjong.melds import Meld, Mentsu


# TODO: maybe superclass for kan calls, then easier isinstance check in discard command for kandora
# TODO: handle suukaikan

class CmdKan(Command):

    def __init__(self, player, tiles, called_player):
        super().__init__("kan (called)")
        self.player = player
        self.tiles = tiles
        self.called_player = called_player

    def execute(self, state):
        called_tile = self.called_player.discards.pop()
        meld = Meld(
            variant=Mentsu.MINKAN,
            tiles=self.tiles,
            called_tile=called_tile,
            called_player=self.called_player)
        self.player.called_melds.append(meld)

    def valid(self, state):
        return True  # TODO


class CmdAddedKan(Command):

    def __init__(self, player, tile):
        super().__init__("kan (added)")
        self.player = player
        self.tile = tile

    def execute(self, state):
        for meld in self.player.called_melds:
            if Mentsu.MINKOU in meld.variant and meld.tiles[0].face == self.tile.face:
                meld.into_added_kan(self.tile)

    def valid(self, state):
        return True  # TODO
