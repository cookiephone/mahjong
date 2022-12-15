from mahjong.yaku.yaku import Yaku
from mahjong.yaku.riichi import Riichi


class Ippatsu(Yaku):

    name_full = "ippatsu"
    name_short = "ippatsu"
    name_en = "ready hand"
    value_open = 0
    value_closed = 1
    yakuman = False
    disables = {}
    enables = {Riichi}

    @staticmethod
    def applies(state, player):
        pass #TODO
