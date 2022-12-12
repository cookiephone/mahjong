from mahjong.yaku.yaku import Yaku


class Chiitoi(Yaku):

    name_full = "chiitoitsu"
    name_short = "chiitoi"
    name_en = "seven pairs"
    value_open = 0
    value_closed = 2
    yakuman = False
    disables = {}
    enables = {}

    def applies(self, state, player):
        pass #TODO
