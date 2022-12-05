from mahjong.commands.command import Command


class CmdDraw(Command):

    def __init__(self, player, deadwall):
        super().__init__("draw")
        self.player = player
        self.deadwall = deadwall
    
    def execute(self, state):
        tile = state.wall.draw(deadwall=self.deadwall)
        self.player.hand.append(tile)
