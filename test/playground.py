from mahjong import rules
from mahjong.tiles import Faces, Tile
from mahjong.seats import Seat
from mahjong.melds import Meld, Mentsu
from mahjong.wall import Wall
from mahjong.utils.parsing import tileset_from_string, tileset_to_string


tiles = tileset_from_string("213mW9651p4501mWesnGGR")
for tile in tiles:
    print(tile)

s = tileset_to_string(tiles)
print(s)

print(Seat.TOIMEN.apply(Seat.TOIMEN))

meld = Meld(type=Mentsu.ANKAN)

print(repr(meld))

wall = Wall(seed=0)
wall.reveal_kandora()
print([str(f) for f in wall.dora()])
print([str(f) for f in wall.uradora()])

rctx = rules.get_ruleset_context()
print(rctx)
