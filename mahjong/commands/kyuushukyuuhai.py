from mahjong.commands.command import Command


class CmdKyuushuKyuuhai(Command):

    def __init__(self, player):
        super().__init__("kyuushu kyuuhai")
        self.player = player

    def execute(self, state):
        pass

    def valid(self, state):
        return True #TODO
