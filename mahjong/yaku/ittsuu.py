from mahjong.yaku.yaku import Yaku


class Ittsuu(Yaku):

    name_full = "ikkitsuukan"
    name_short = "ittsuu"
    name_en = "straight"
    value_open = 1
    value_closed = 2
    yakuman = False
    disables = {}
    enables = {}

    def applies(self, state, player):
        pass #TODO
