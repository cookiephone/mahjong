from mahjong.yaku.yaku import Yaku


class Pinfu(Yaku):

    name_full = "pinfu"
    name_short = "pinfu"
    name_en = "all sequences"
    value_open = 0
    value_closed = 1
    yakuman = False
    disables = {}
    enables = {}

    @staticmethod
    def applies(state, player):
        pass #TODO
