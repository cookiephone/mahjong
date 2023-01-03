from mahjong.commands.command import Command


class CmdRiichi(Command):

    def __init__(self, player):
        super().__init__("riichi")
        self.player = player

    def __call__(self, state):
        pass

    def valid(self, state):
        return True  # TODO

    @staticmethod
    def build(state, positions):
        return []  # TODO
