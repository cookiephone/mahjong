from mahjong.commands.command import Command
from mahjong.melds import Meld, Mentsu
from mahjong.utils import helpers


class CmdKanGeneric(Command):

    def __call__(self, state):
        self._handle_suukaikan(state)

    @staticmethod
    def _handle_suukaikan(state):
        if state.rule_context.suukaikan and not state.rule_context.suukaikan_after_discard:
            if helpers.filter_commands_by_type(state.last_command_batch, (CmdKan, CmdAddedKan)):
                state.current_hand.abort = True


class CmdKan(CmdKanGeneric):

    def __init__(self, player, tiles, called_player=None):
        super().__init__("kan (called)")
        self.player = player
        self.tiles = tiles
        self.called_player = called_player

    def __call__(self, state):
        if self.called_player:
            self._call_open()
        else:
            self._call_closed()

    def _call_open(self):
        called_tile = self.called_player.discards.pop()
        meld = Meld(
            variant=Mentsu.MINKAN,
            tiles=self.tiles,
            called_tile=called_tile,
            called_player=self.called_player)
        self.player.called_melds.append(meld)

    def _call_closed(self):
        meld = Meld(
            variant=Mentsu.ANKAN,
            tiles=self.tiles)
        self.player.called_melds.append(meld)

    def valid(self, state):
        return True  # TODO

    @staticmethod
    def build(state, positions):
        return []  # TODO


class CmdAddedKan(CmdKanGeneric):

    def __init__(self, player, tile):
        super().__init__("kan (added)")
        self.player = player
        self.tile = tile

    def __call__(self, state):
        for meld in self.player.called_melds:
            if Mentsu.MINKOU in meld.variant and meld.tiles[0].face == self.tile.face:
                meld.into_added_kan(self.tile)

    def valid(self, state):
        return True  # TODO

    @staticmethod
    def build(state, positions):
        return []  # TODO
