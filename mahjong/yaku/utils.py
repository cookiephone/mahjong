from mahjong.yaku.normalyaku import NORMAL_YAKU
from mahjong.yaku.yakuman import YAKUMAN
from graphlib import TopologicalSorter


ALL_YAKU = NORMAL_YAKU + YAKUMAN

YAKU_DISABLE_GRAPH = {yaku: yaku.disables for yaku in ALL_YAKU}
YAKU_CHECKING_ORDER = list(reversed(list(TopologicalSorter(graph=YAKU_DISABLE_GRAPH).static_order())))
