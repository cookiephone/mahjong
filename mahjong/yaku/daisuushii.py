from mahjong.yaku.yaku import Yaku
from mahjong.yaku.shousuushii import Shousuushii
from mahjong.yaku.normalyaku import NORMAL_YAKU


class Daisuushii(Yaku):

    name_full = "daisuushii"
    name_short = "daisuushii"
    name_en = "big four winds"
    value_open = None
    value_closed = None
    yakuman = True
    disables = NORMAL_YAKU | {Shousuushii}
    enables = {}

    @staticmethod
    def applies(state, player):
        pass #TODO
