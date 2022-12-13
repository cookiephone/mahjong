from mahjong.commands.command import Command


class CmdRon(Command):

    def __init__(self, player, called_player):
        super().__init__("ron")
        self.player = player
        self.called_player = called_player

    def execute(self, state):
        pass

    def valid(self, state):
        return True  # TODO
