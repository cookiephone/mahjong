from mahjong.yaku.yaku import Yaku
from mahjong.yaku.normalyaku import NORMAL_YAKU


class Shousuushii(Yaku):

    name_full = "shousuushii"
    name_short = "shousuushii"
    name_en = "little four winds"
    value_open = None
    value_closed = None
    yakuman = True
    disables = NORMAL_YAKU
    enables = []

    def applies(self, state, player):
        pass #TODO
