from mahjong.yaku.yaku import Yaku


class Tanyao(Yaku):

    name_full = "tanyao"
    name_short = "tanyao"
    name_en = "all simples"
    value_open = 1
    value_closed = 1
    yakuman = False
    disables = {}
    enables = {}

    @staticmethod
    def applies(state, player):
        pass #TODO
