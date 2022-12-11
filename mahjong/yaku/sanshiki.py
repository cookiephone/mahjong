from mahjong.yaku.yaku import Yaku


class Sanshiki(Yaku):

    name_full = "sanshoku doujun"
    name_short = "sanshiki"
    name_en = "three colored straight"
    value_open = 1
    value_closed = 2
    yakuman = False
    disables = []
    enables = []

    def applies(self, state, player):
        pass #TODO
