from mahjong.commands.command import Command
from mahjong.commands.kan import CmdKan, CmdAddedKan
from mahjong.utils import helpers

class CmdDraw(Command):

    def __init__(self, player, deadwall):
        super().__init__("draw")
        self.player = player
        self.deadwall = deadwall

    def __call__(self, state):
        tile = state.wall.draw(deadwall=self.deadwall)
        self.player.hand.append(tile)

    def valid(self, state):
        return True #TODO

    @staticmethod
    def build(state, positions):
        commands = []
        for pos in positions:
            seat = state.last_active_seat(pos)
            player = state.current_hand.get_player(seat)
            deadwall = bool(helpers.filter_commands_by_type(state.last_command_batch,
                                                            (CmdKan, CmdAddedKan)))
            commands.append(CmdDraw(player, deadwall=deadwall))
        return commands
