from mahjong.yaku.yaku import Yaku


class RinshanKaihou(Yaku):

    name_full = "rinshan kaihou"
    name_short = "rinshan kaihou"
    name_en = "deadwall draw"
    value_open = 1
    value_closed = 1
    yakuman = False
    disables = []
    enables = []

    def applies(self, state, player):
        pass #TODO
