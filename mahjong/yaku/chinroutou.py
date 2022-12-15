from mahjong.yaku.yaku import Yaku
from mahjong.yaku.normalyaku import NORMAL_YAKU


class Chinroutou(Yaku):

    name_full = "chinroutou"
    name_short = "chinroutou"
    name_en = "all terminals"
    value_open = None
    value_closed = None
    yakuman = True
    disables = NORMAL_YAKU
    enables = {}

    @staticmethod
    def applies(state, player):
        pass #TODO
