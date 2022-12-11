from mahjong.yaku.yaku import Yaku
from mahjong.yaku.normalyaku import NORMAL_YAKU


class KokushiMusou(Yaku):

    name_full = "kokushi musou"
    name_short = "kokushi musou"
    name_en = "thirteen orphans"
    value_open = None
    value_closed = None
    yakuman = True
    disables = NORMAL_YAKU

    def applies(self, state, player):
        pass #TODO
