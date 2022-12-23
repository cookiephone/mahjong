import copy
import itertools
from dataclasses import dataclass
from typing import Any
from collections import defaultdict
from mahjong.utils import decorators
from mahjong.melds import Meld, Mentsu
from mahjong.tiles import Faces


@dataclass(frozen=True)
class Interpretation:

    unmelded_tiles: Any
    called_melds: Any
    implicit_melds: Any

    def make_with_meld(self, meld):
        return Interpretation(
            frozenset(self.unmelded_tiles - meld.tiles),
            self.called_melds,
            frozenset(self.implicit_melds | {meld}))


class HandExplorer:

    def __init__(self, player):
        self.unmelded_tiles = frozenset(copy.deepcopy(player.hand))
        self.called_melds = frozenset(copy.deepcopy(player.called_melds))
        self.children_builders = [self.attempt_anjun_fix, self.attempt_ankou_fix]

    def attempt_anjun_fix(self, root):
        tiles = [tile for tile in root.unmelded_tiles if not tile.is_honor()]
        tiles.sort(key=lambda tile: tile.face.key())
        children = set()
        for i, tile in enumerate(tiles[1:-1], 1):
            prv, nxt = tiles[i - 1], tiles[i + 1]
            if tile.face.pred() == prv.face and tile.face.succ() == nxt.face:
                meld = Meld(Mentsu.ANJUN, {prv, tile, nxt})
                child = root.make_with_meld(meld)
                children.add(child)
        return children

    def attempt_ankou_fix(self, root):
        buckets = defaultdict(set)
        for tile in root.unmelded_tiles:
            buckets[tile.face].add(tile)
        buckets[Faces.MAN5].update(buckets[Faces.MAN5_AKA])
        buckets[Faces.PIN5].update(buckets[Faces.PIN5_AKA])
        buckets[Faces.SOU5].update(buckets[Faces.SOU5_AKA])
        children = set()
        for tiles in buckets.values():
            if len(tiles) < 3:
                continue
            tiles = set(itertools.islice(tiles, 3))
            meld = Meld(Mentsu.ANKOU, tiles)
            child = root.make_with_meld(meld)
            children.add(child)
        return children

    @decorators.dedupe_generator
    def explore(self, root=None):
        if not root:
            root = Interpretation(self.unmelded_tiles, self.called_melds, frozenset())
        yield root
        for builder in self.children_builders:
            if children := builder(root):
                for child in children:
                    yield from self.explore(child)
