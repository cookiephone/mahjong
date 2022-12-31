from mahjong.commands.command import Command


class CmdKyuushuKyuuhai(Command):

    def __init__(self, player):
        super().__init__("kyuushu kyuuhai")
        self.player = player

    def __call__(self, state):
        pass

    def valid(self, state):
        return True  # TODO

    @staticmethod
    def build(positions):
        return []  # TODO
