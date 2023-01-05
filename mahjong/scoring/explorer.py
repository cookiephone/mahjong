import copy
import itertools
from dataclasses import dataclass
from typing import Any
from collections import defaultdict
from functools import wraps
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
        self.children_builders = [
            self._attempt_anjun_fix,
            self._attempt_ankou_fix,
            self._attempt_pair_fix,
        ]

    def _attempt_anjun_fix(self, root):
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

    def _attempt_ankou_fix(self, root):
        buckets = defaultdict(set)
        for tile in root.unmelded_tiles:
            buckets[tile.face].add(tile)
        buckets[Faces.MAN5].update(buckets[Faces.MAN5_AKA])
        buckets[Faces.PIN5].update(buckets[Faces.PIN5_AKA])
        buckets[Faces.SOU5].update(buckets[Faces.SOU5_AKA])
        for tiles in buckets.values():
            if len(tiles) < 3:
                continue
            tiles = set(itertools.islice(tiles, 3))
            meld = Meld(Mentsu.ANKOU, tiles)
            yield root.make_with_meld(meld)

    def _attempt_pair_fix(self, root, multiple_pairs=False):
        if not multiple_pairs and any(meld.is_pair() for meld in root.implicit_melds):
            return
        buckets = defaultdict(set)
        for tile in root.unmelded_tiles:
            buckets[tile.face].add(tile)
        buckets[Faces.MAN5].update(buckets[Faces.MAN5_AKA])
        buckets[Faces.PIN5].update(buckets[Faces.PIN5_AKA])
        buckets[Faces.SOU5].update(buckets[Faces.SOU5_AKA])
        for tiles in buckets.values():
            if len(tiles) < 2:
                continue
            tiles = set(itertools.islice(tiles, 2))
            meld = Meld(Mentsu.PAIR, tiles)
            yield root.make_with_meld(meld)

    def _explore_melds(self, root):
        yield root
        for builder in self.children_builders:
            if children := builder(root):
                for child in children:
                    yield from self._explore_melds(child)

    @_chiitoi_checker
    def _chiitoi_exploration(self, root):
        if child := next(self._attempt_pair_fix(root, multiple_pairs=True), None):
            yield from self._chiitoi_exploration(child)
        yield root

    def _kokushi_musou_exploration(self, root, fixed_pair=None):
        if not fixed_pair and (children := self._attempt_pair_fix(root)):
            for child in children:
                pair = next(iter(child.implicit_melds))  # pair is guaranteed to exist | pylint: disable=R1708
                pair_tile = next(iter(pair.tiles))  # tile is guaranteed to exist | pylint: disable=R1708
                if pair_tile.is_terminal() or pair_tile.is_honor():
                    yield from self._kokushi_musou_exploration(child, fixed_pair=pair)
        tiles = {}
        for tile in root.unmelded_tiles:
            if ((tile.is_honor() or tile.is_terminal()) and not tile.face in tiles and fixed_pair
              and not tile.face == next(iter(fixed_pair.tiles)).face):  # tile is guaranteed to exist | pylint: disable=R1708
                tiles[tile.face] = tile
        if tiles.values():
            meld = Meld(Mentsu.KOKUSHI, set(tiles.values()))
            child = root.make_with_meld(meld)
            yield child

    def _explore_special_hands(self, root):
        yield from self._chiitoi_exploration(root)
        yield from self._kokushi_musou_exploration(root)

    @decorators.dedupe_generator
    def explore(self):
        root = Interpretation(self.unmelded_tiles, self.called_melds, frozenset())
        yield from self._explore_melds(root)
        yield from self._explore_special_hands(root)

    @staticmethod
    def _chiitoi_checker(chiitoi_explorer):
        @wraps(chiitoi_explorer)
        def wrapper(*args, **kwargs):
            for child in chiitoi_explorer(*args, **kwargs):
                n_unique_faces = len(set(next(iter(pair.tiles)) for pair in child.implicit_melds))  # tile is guaranteed to exist | pylint: disable=R1708
                if len(child.implicit_melds) == n_unique_faces:
                    yield child
        return wrapper
