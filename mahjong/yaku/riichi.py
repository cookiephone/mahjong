from mahjong.yaku.yaku import Yaku


class Riichi(Yaku):

    name_full = "riichi"
    name_short = "riichi"
    name_en = "ready hand"
    value_open = 0
    value_closed = 1
    yakuman = False
    disables = {}
    enables = {}

    @staticmethod
    def applies(state, player):
        pass #TODO
