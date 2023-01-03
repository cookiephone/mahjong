from mahjong.commands.command import Command


class CmdRon(Command):

    def __init__(self, player, called_player):
        super().__init__("ron")
        self.player = player
        self.called_player = called_player

    def __call__(self, state):
        pass

    def valid(self, state):
        return True  # TODO

    @staticmethod
    def build(state, positions):
        return []  # TODO
