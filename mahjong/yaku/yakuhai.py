from mahjong.yaku.yaku import Yaku


class Yakuhai(Yaku):

    name_full = "yakuhai"
    name_short = "yakuhai"
    name_en = "value tiles"
    value_open = 1
    value_closed = 1
    yakuman = False
    disables = []

    def applies(self, state, player):
        pass #TODO
