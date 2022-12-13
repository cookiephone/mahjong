import make
make.build_and_install()

from mahjong import rules
from mahjong.tiles import Faces, Tile
from mahjong.seats import Seat
from mahjong.melds import Meld, Mentsu
from mahjong.wall import Wall
from mahjong.game import GameState
from mahjong.engine import Engine
from mahjong.commands.ron import CmdRon
from mahjong.commands.starthand import CmdStartHand
from mahjong.utils.parsing import tileset_from_string, tileset_to_string
from mahjong.utils.debug import gamestate_vis_string

import visualizer.visualizer as vis


vis.run()
exit()

seed = 0

engine = Engine(seed=seed)
CmdStartHand().execute(engine.gamestate)
wall = Wall()
wall.construct()
ndiscards = [15, 17, 14, 14]
for i, player in enumerate(engine.gamestate.hands[-1].players):
    player.hand = [wall.draw() for _ in range(13)]
    player.discards = [wall.draw() for _ in range(ndiscards[i])]
engine.gamestate.hands[-1].players[0].hand.append(wall.draw())
nfromhand = lambda hand, n: [hand.pop() for _ in range(n)]
tiles = nfromhand(engine.gamestate.hands[-1].players[0].hand, 3)
meld = Meld(type=Mentsu.MINJUN, tiles=tiles, called_tile=tiles[0], called_player=engine.gamestate.hands[-1].get_player(Seat.EAST))
engine.gamestate.hands[-1].players[0].called_melds.append(meld)
tiles = nfromhand(engine.gamestate.hands[-1].players[0].hand, 3)
meld = Meld(type=Mentsu.MINKOU, tiles=tiles, called_tile=tiles[1], called_player=engine.gamestate.hands[-1].get_player(Seat.SOUTH))
engine.gamestate.hands[-1].players[0].called_melds.append(meld)
tiles = nfromhand(engine.gamestate.hands[-1].players[2].hand, 4)
meld = Meld(type=Mentsu.MINKAN, tiles=tiles, called_tile=tiles[2], called_player=engine.gamestate.hands[-1].get_player(Seat.WEST))
engine.gamestate.hands[-1].players[2].called_melds.append(meld)
tiles = nfromhand(engine.gamestate.hands[-1].players[3].hand, 4)
meld = Meld(type=Mentsu.SHOUMINKAN, tiles=tiles, called_tile=tiles[3], called_player=engine.gamestate.hands[-1].get_player(Seat.NORTH))
engine.gamestate.hands[-1].players[3].called_melds.append(meld)
tiles = nfromhand(engine.gamestate.hands[-1].players[3].hand, 4)
meld = Meld(type=Mentsu.ANKAN, tiles=tiles)
engine.gamestate.hands[-1].players[3].called_melds.append(meld)

print(gamestate_vis_string(engine.gamestate))
