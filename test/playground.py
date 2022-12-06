import make
make.build_and_install()

from mahjong import rules
from mahjong.tiles import Faces, Tile
from mahjong.seats import Seat
from mahjong.melds import Meld, Mentsu
from mahjong.wall import Wall
from mahjong.game import GameState
from mahjong.utils.parsing import tileset_from_string, tileset_to_string
from mahjong.utils.debug import gamestate_vis_string


seed = 0

game = GameState(seed=seed)
game.wall.construct()
wall = Wall(seed=seed)
wall.construct()
ndiscards = [15, 17, 14, 14]
for i, player in enumerate(game.players):
    player.hand = [wall.draw() for _ in range(13)]
    player.discards = [wall.draw() for _ in range(ndiscards[i])]
game.players[0].hand.append(wall.draw())

print(gamestate_vis_string(game))
