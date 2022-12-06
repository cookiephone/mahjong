from mahjong.commands.command import Command


class CmdDiscard(Command):

    def __init__(self, player, tile):
        super().__init__("discard")
        self.player = player
        self.tile = tile
    
    def execute(self, state):
        self.player.hand.remove(self.tile)
        self.player.discards.append(self.tile)

    def valid(self, state):
        return True #TODO
