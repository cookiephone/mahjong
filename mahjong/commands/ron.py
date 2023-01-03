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
        commands = []
        for pos in positions:
            seat = state.last_active_seat(pos)
            player = state.current_hand.get_player(seat)
            called_player = state.current_hand.get_player(state.last_active_seat)
            commands.append(CmdRon(player, called_player))
        return commands
