import mahjong.utils.parsing as parsing
import mahjong.dora as dora
import random


class Wall:

    def __init__(self, seed=None, akadora=True):
        self.seed = seed
        self.akadora = akadora
        random.seed(self.seed)

    def construct(self):
        self.get_tiles()
        self.shuffle_tiles()
        self.dora_indicators = [self.tiles[i] for i in [5, 7, 9, 11, 13]]
        self.uradora_indicators = [self.tiles[i] for i in [4, 6, 8, 10, 12]]
        self.ndora_revealed = 1
        self.remaining = len(self.tiles) - 14

    def dora(self):
        indicators = self.dora_indicators[:self.ndora_revealed]
        return dora.dora(indicators)

    def uradora(self):
        indicators = self.uradora_indicators[:self.ndora_revealed]
        return dora.dora(indicators)

    def draw(self, deadwall=False):
        if self.remaining == 0 and not deadwall:
            return None
        if deadwall:
            tile = self.tiles.pop(0)
        else:
            tile = self.tiles.pop()
        self.remaining -= 1
        return tile

    def reveal_kandora(self):
        if self.ndora_revealed < 5:
            self.ndora_revealed += 1

    def shuffle_tiles(self):
        random.shuffle(self.tiles)

    def get_tiles(self):
        if self.akadora:
            tilestring = parsing.ALL_TILES
        else:
            tilestring = parsing.ALL_TILES_NO_AKA
        tiles = parsing.tileset_from_string(tilestring)
        for i, tile in enumerate(tiles):
            tile.uid = i
        self.tiles = tiles
