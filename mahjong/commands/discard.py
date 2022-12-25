from collections import defaultdict
from mahjong.commands.command import Command
from mahjong.commands.starthand import CmdStartHand
from mahjong.commands.kan import CmdKan, CmdAddedKan
from mahjong.utils import helpers


# TODO: handle suufon renda (should make valid() fail for non-EndHand commands)

class CmdDiscard(Command):

    def __init__(self, player, tile):
        super().__init__("discard")
        self.player = player
        self.tile = tile

    def __call__(self, state):
        self.player.hand.remove(self.tile)
        self.player.discards.append(self.tile)
        self._handle_kandora(state)

    def valid(self, state):
        return True  # TODO

    @staticmethod
    def _handle_kandora(state):
        if state.rule_context.kan_dora:
            if helpers.filter_commands_by_type(state.history[-1], (CmdKan, CmdAddedKan)):
                state.current_hand.wall.reveal_kandora()

    @staticmethod
    def _handle_suukaikan(state):
        if state.rule_context.suukaikan and state.rule_context.suukaikan_after_discard:
            if helpers.filter_commands_by_type(state.history[-1], (CmdKan, CmdAddedKan)):
                state.current_hand.abort = True

    @staticmethod
    def _handle_suufon_renda(state):
        if state.rule_context.suufon_renda:
            history_generator = reversed(state.history)
            winds = defaultdict(int)
            ndiscards = 0
            while batch := next(history_generator) and ndiscards <= 4:
                if any(isinstance(cmd, CmdStartHand) for cmd in batch):
                    return
                if discards := helpers.filter_commands_by_type(batch, CmdDiscard):
                    if not discards[0].tile.is_wind():
                        return
                    ndiscards += 1
                    winds[discards[0].tile.face] += 1
            if any(n == 4 for n in winds.values()):
                state.current_hand.abort = True
