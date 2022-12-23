from mahjong.commands.command import Command


class CmdEndGame(Command):

    def __init__(self):
        super().__init__("end game")

    def __call__(self, state):
        pass  # TODO

    def valid(self, state):
        return True  # TODO
