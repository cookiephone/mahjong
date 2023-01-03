from mahjong.commands.command import Command


class CmdEndHand(Command):

    def __init__(self):
        super().__init__("end hand")

    def __call__(self, state):
        pass  # TODO

    def valid(self, state):
        return True  # TODO

    @staticmethod
    def build(state, positions):
        return [CmdEndHand()]
