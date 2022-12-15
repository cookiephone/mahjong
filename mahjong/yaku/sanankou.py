from mahjong.yaku.yaku import Yaku


class Sanankou(Yaku):

    name_full = "sanankou"
    name_short = "sanankou"
    name_en = "three concealed triplets"
    value_open = 2
    value_closed = 2
    yakuman = False
    disables = {}
    enables = {}

    @staticmethod
    def applies(state, player):
        pass #TODO
