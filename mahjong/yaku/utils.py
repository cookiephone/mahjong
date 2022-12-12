from mahjong.yaku.allyaku import ALL_YAKU
from graphlib import TopologicalSorter
from collections import defaultdict


YAKU_DISABLE_GRAPH = defaultdict(list)
for yaku in ALL_YAKU:
    YAKU_DISABLE_GRAPH[yaku].extend(yaku.enables)
    for disabled in yaku.disables:
        YAKU_DISABLE_GRAPH[disabled].append(yaku)

YAKU_CHECKING_ORDER = list(TopologicalSorter(graph=YAKU_DISABLE_GRAPH).static_order())
