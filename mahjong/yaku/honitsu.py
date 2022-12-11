from mahjong.yaku.yaku import Yaku


class Honitsu(Yaku):

    name_full = "honiisou"
    name_short = "honitsu"
    name_en = "half flush"
    value_open = 2
    value_closed = 3
    yakuman = False
    disables = []
    enables = []

    def applies(self, state, player):
        pass #TODO
