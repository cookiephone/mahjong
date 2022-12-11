from mahjong.yaku.yaku import Yaku


class Chanta(Yaku):

    name_full = "honchantaiyaochuu"
    name_short = "chanta"
    name_en = "terminal or honor in each group"
    value_open = 1
    value_closed = 2
    yakuman = False
    disables = []
    enables = []

    def applies(self, state, player):
        pass #TODO
