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


# TODO: add info to options about for which player a command is enabled
class CommandOptions:

    def __init__(self, rule_context):
        self._options = {
            CmdEndGame:
                set(),
            CmdStartHand: {
                CmdDraw},
            CmdEndHand: {
                CmdEndGame,
                CmdStartHand},
            CmdDraw: {
                CmdKyuushuKyuuhai,
                CmdDiscard,
                CmdTsumo,
                CmdRiichi,
                CmdAddedKan},
            CmdDiscard: {
                CmdEndHand,
                CmdDraw,
                CmdRon,
                CmdChii,
                CmdKan,
                CmdPon},
            CmdChii: {
                CmdDiscard},
            CmdPon: {
                CmdDiscard},
            CmdKan: {
                CmdEndHand,
                CmdDiscard},
            CmdAddedKan: {
                CmdEndHand,
                CmdDiscard,
                CmdRon},
            CmdRiichi: {
                CmdDiscard},
            CmdRon: {
                CmdEndHand},
            CmdTsumo: {
                CmdEndHand},
            CmdKyuushuKyuuhai: {
                CmdEndHand}
        }
        if rule_context.kokushi_chankan:
            self._options[CmdKan].add(CmdRon)
        if rule_context.suucha_riichi:
            self._options[CmdRiichi].add(CmdEndHand)

    def __call__(self, cmd_type):
        return self._options[cmd_type]
