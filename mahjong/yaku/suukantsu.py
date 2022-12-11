from mahjong.yaku.yaku import Yaku
from mahjong.yaku.normalyaku import NORMAL_YAKU


class Suukantsu(Yaku):

    name_full = "suukantsu"
    name_short = "suukantsu"
    name_en = "four quads"
    value_open = None
    value_closed = None
    yakuman = True
    disables = NORMAL_YAKU
