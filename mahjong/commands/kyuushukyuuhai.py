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
    def build(state, positions):
        commands = []
        for pos in positions:
            seat = state.last_active_seat(pos)
            player = state.current_hand.get_player(seat)
            commands.append(CmdKyuushuKyuuhai(player))
        return commands
