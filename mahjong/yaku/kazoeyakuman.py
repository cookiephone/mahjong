from mahjong.yaku.yaku import Yaku
from mahjong.yaku.normalyaku import NORMAL_YAKU


class KazoeYakuman(Yaku):

    name_full = "kazoe yakuman"
    name_short = "kazoe yakuman"
    name_en = "counted yakuman"
    value_open = None
    value_closed = None
    yakuman = True
    disables = {}
    enables = NORMAL_YAKU

    def applies(self, state, player):
        pass #TODO
