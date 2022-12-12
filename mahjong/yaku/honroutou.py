from mahjong.yaku.yaku import Yaku


class Honroutou(Yaku):

    name_full = "honroutou"
    name_short = "honroutou"
    name_en = "terminals and honors"
    value_open = 2
    value_closed = 2
    yakuman = False
    disables = {}
    enables = {}

    def applies(self, state, player):
        pass #TODO