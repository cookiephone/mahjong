from mahjong.yaku.yaku import Yaku


class Haitei(Yaku):

    name_full = "haitei raoyue"
    name_short = "haitei"
    name_en = "win by last draw"
    value_open = 1
    value_closed = 1
    yakuman = False
    disables = []
    enables = []

    def applies(self, state, player):
        pass #TODO
