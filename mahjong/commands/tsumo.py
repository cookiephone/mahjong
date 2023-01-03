from mahjong.commands.command import Command


class CmdTsumo(Command):

    def __init__(self, player):
        super().__init__("tsumo")
        self.player = player

    def execute(self, state):
        pass

    def valid(self, state):
        return True  # TODO

    @staticmethod
    def build(state, positions):
        commands = []
        for pos in positions:
            seat = state.last_active_seat(pos)
            player = state.current_hand.get_player(seat)
            commands.append(CmdTsumo(player))
        return commands
