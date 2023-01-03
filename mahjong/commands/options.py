from mahjong.commands.endgame import CmdEndGame
from mahjong.commands.endhand import CmdEndHand
from mahjong.commands.starthand import CmdStartHand
from mahjong.commands.discard import CmdDiscard
from mahjong.commands.kyuushukyuuhai import CmdKyuushuKyuuhai
from mahjong.commands.draw import CmdDraw
from mahjong.commands.chii import CmdChii
from mahjong.commands.pon import CmdPon
from mahjong.commands.kan import CmdKan, CmdAddedKan
from mahjong.commands.riichi import CmdRiichi
from mahjong.commands.ron import CmdRon
from mahjong.commands.tsumo import CmdTsumo
from mahjong.seats import Seat


class CommandOptions:

    def __init__(self, rule_context):
        self._initial_options = {(CmdStartHand, None)}
        self._options = {
            CmdEndGame:
                set(),
            CmdStartHand: {
                (CmdDraw, None)},
            CmdEndHand: {
                (CmdEndGame, None),
                (CmdStartHand, None)},
            CmdDraw: {
                (CmdKyuushuKyuuhai, (Seat.SELF,)),
                (CmdDiscard, (Seat.SELF,)),
                (CmdTsumo, (Seat.SELF,)),
                (CmdRiichi, (Seat.SELF,)),
                (CmdAddedKan, (Seat.SELF,))},
            CmdDiscard: {
                (CmdEndHand, None),
                (CmdDraw, (Seat.SHIMOCHA,)),
                (CmdRon, (Seat.SHIMOCHA, Seat.TOIMEN, Seat.KAMICHA)),
                (CmdChii, (Seat.SHIMOCHA,)),
                (CmdKan, (Seat.SHIMOCHA, Seat.TOIMEN, Seat.KAMICHA)),
                (CmdPon, (Seat.SHIMOCHA, Seat.TOIMEN, Seat.KAMICHA))},
            CmdChii: {
                (CmdDiscard, (Seat.SELF,))},
            CmdPon: {
                (CmdDiscard, (Seat.SELF,))},
            CmdKan: {
                (CmdEndHand, None),
                (CmdDraw, (Seat.SELF,))},
            CmdAddedKan: {
                (CmdEndHand, None),
                (CmdDraw, (Seat.SELF,)),
                (CmdRon, (Seat.SHIMOCHA, Seat.TOIMEN, Seat.KAMICHA))},
            CmdRiichi: {
                (CmdDiscard, (Seat.SELF,))},
            CmdRon: {
                (CmdEndHand, None)},
            CmdTsumo: {
                (CmdEndHand, None)},
            CmdKyuushuKyuuhai: {
                (CmdEndHand, None)}
        }
        if rule_context.kokushi_chankan:
            self._options[CmdKan].add((CmdRon, (Seat.SHIMOCHA, Seat.TOIMEN, Seat.KAMICHA)))
        if rule_context.suucha_riichi:
            self._options[CmdRiichi].add((CmdEndHand, None))

    def from_command_batch(self, batch):
        try:
            return set().union(*(self(type(cmd)) for cmd in batch))
        except TypeError:
            return self._initial_options

    def __call__(self, cmd_type):
        return self._options[cmd_type]
