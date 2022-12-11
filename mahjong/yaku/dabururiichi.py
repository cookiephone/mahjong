from mahjong.yaku.yaku import Yaku


class DaburuRiichi(Yaku):

    name_full = "daburu riichi"
    name_short = "daburu riichi"
    name_en = "double ready"
    value_open = 0
    value_closed = 2
    yakuman = False
    disables = []
    enables = []

    def applies(self, state, player):
        pass #TODO
