from mahjong.yaku.yaku import Yaku
from mahjong.yaku.normalyaku import NORMAL_YAKU


class Ryuuiisou(Yaku):

    name_full = "ryuuiisou"
    name_short = "ryuuiisou"
    name_en = "all green"
    value_open = None
    value_closed = None
    yakuman = True
    disables = NORMAL_YAKU
    enables = {}

    @staticmethod
    def applies(state, player):
        pass #TODO
