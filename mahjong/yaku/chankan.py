from mahjong.yaku.yaku import Yaku


class Chankan(Yaku):

    name_full = "chankan"
    name_short = "chankan"
    name_en = "robbing a kan"
    value_open = 1
    value_closed = 1
    yakuman = False
    disables = []

    def applies(self, state, player):
        pass #TODO
