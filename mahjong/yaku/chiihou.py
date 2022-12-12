from mahjong.yaku.yaku import Yaku
from mahjong.yaku.normalyaku import NORMAL_YAKU


class Chiihou(Yaku):

    name_full = "chiihou"
    name_short = "chiihou"
    name_en = "earthly hand"
    value_open = None
    value_closed = None
    yakuman = True
    disables = NORMAL_YAKU
    enables = {}

    def applies(self, state, player):
        pass #TODO
