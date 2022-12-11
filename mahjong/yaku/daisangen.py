from mahjong.yaku.yaku import Yaku
from mahjong.yaku.normalyaku import NORMAL_YAKU


class Daisangen(Yaku):

    name_full = "daisangen"
    name_short = "daisangen"
    name_en = "big three dragons"
    value_open = None
    value_closed = None
    yakuman = True
    disables = NORMAL_YAKU

    def applies(self, state, player):
        pass #TODO
