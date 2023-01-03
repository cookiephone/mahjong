from mahjong.commands.command import Command


class CmdDraw(Command):

    def __init__(self, player, deadwall):
        super().__init__("draw")
        self.player = player
        self.deadwall = deadwall

    def __call__(self, state):
        tile = state.wall.draw(deadwall=self.deadwall)
        self.player.hand.append(tile)

    def valid(self, state):
        return True #TODO

    @staticmethod
    def build(state, positions):
        return []  # TODO
