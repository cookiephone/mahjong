from mahjong.yaku.yaku import Yaku


class Houtei(Yaku):

    name_full = "houtei raoyui"
    name_short = "houtei"
    name_en = "win by last discard"
    value_open = 1
    value_closed = 1
    yakuman = False
    disables = {}
    enables = {}

    def applies(self, state, player):
        pass #TODO
