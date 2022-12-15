from mahjong.yaku.yaku import Yaku
from mahjong.yaku.normalyaku import NORMAL_YAKU


class Tenhou(Yaku):

    name_full = "tenhou"
    name_short = "tenhou"
    name_en = "heavenly hand"
    value_open = None
    value_closed = None
    yakuman = True
    disables = NORMAL_YAKU
    enables = {}

    @staticmethod
    def applies(state, player):
        pass #TODO
