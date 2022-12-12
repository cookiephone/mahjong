from mahjong.yaku.yaku import Yaku
from mahjong.yaku.normalyaku import NORMAL_YAKU


class Suuankou(Yaku):

    name_full = "suuankou"
    name_short = "suuankou"
    name_en = "four concealed triplets"
    value_open = None
    value_closed = None
    yakuman = True
    disables = NORMAL_YAKU
    enables = {}

    def applies(self, state, player):
        pass #TODO
