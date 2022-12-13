from mahjong.commands.command import Command
from mahjong.commands.kan import CmdKan, CmdAddedKan
from mahjong.utils import helpers


#TODO: handle suufon renda

class CmdDiscard(Command):

    def __init__(self, player, tile):
        super().__init__("discard")
        self.player = player
        self.tile = tile

    def execute(self, state):
        self.player.hand.remove(self.tile)
        self.player.discards.append(self.tile)
        self._handle_kandora(state)

    def valid(self, state):
        return True #TODO

    @staticmethod
    def _handle_kandora(state):
        if state.rule_context.kan_dora:
            if helpers.filter_commands_by_type(state.history[-1], (CmdKan, CmdAddedKan)):
                state.current_hand.wall.reveal_kandora()
