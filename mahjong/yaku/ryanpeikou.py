from mahjong.yaku.yaku import Yaku
from mahjong.yaku.iipeikou import Iipeikou


class Ryanpeikou(Yaku):

    name_full = "ryanpeikou"
    name_short = "ryanpeikou"
    name_en = "two sets of identical sequences"
    value_open = 0
    value_closed = 3
    yakuman = False
    disables = {Iipeikou}
    enables = {}

    @staticmethod
    def applies(state, player):
        pass #TODO
