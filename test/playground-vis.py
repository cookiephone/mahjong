# pylint: skip-file

import make
make.build_and_install(deps=False, extras=["dev"])

from mahjong.seats import Seat
from mahjong.melds import Meld, Mentsu
from mahjong.engine import Engine
from mahjong.commands.starthand import CmdStartHand
from mahjong.utils.debug import gamestate_vis_string

import visualizer

visual_context = visualizer.run()

seed = 0

engine = Engine(seed=seed)
engine.submit([CmdStartHand()])
wall = engine.gamestate.current_hand.wall
ndiscards = [15, 17, 14, 14]
for idx, p in enumerate(engine.gamestate.hands[-1].players):
    p.hand = [wall.draw() for _ in range(13)]
    p.discards = [wall.draw() for _ in range(ndiscards[idx])]
engine.gamestate.hands[-1].players[0].hand.append(wall.draw())
def nfromhand(hand, amount):
    return [hand.pop() for _ in range(amount)]
ts = nfromhand(engine.gamestate.hands[-1].players[0].hand, 3)
meld = Meld(variant=Mentsu.MINJUN, tiles=ts, called_tile=ts[0],
    called_player=engine.gamestate.hands[-1].get_player(Seat.WEST))
engine.gamestate.hands[-1].players[0].called_melds.append(meld)
ts = nfromhand(engine.gamestate.hands[-1].players[0].hand, 3)
meld = Meld(variant=Mentsu.MINKOU, tiles=ts, called_tile=ts[1],
    called_player=engine.gamestate.hands[-1].get_player(Seat.NORTH))
engine.gamestate.hands[-1].players[0].called_melds.append(meld)
ts = nfromhand(engine.gamestate.hands[-1].players[2].hand, 4)
meld = Meld(variant=Mentsu.MINKAN, tiles=ts, called_tile=ts[2],
    called_player=engine.gamestate.hands[-1].get_player(Seat.SOUTH))
engine.gamestate.hands[-1].players[2].called_melds.append(meld)
ts = nfromhand(engine.gamestate.hands[-1].players[1].hand, 3)
meld = Meld(variant=Mentsu.MINJUN, tiles=ts, called_tile=ts[0],
    called_player=engine.gamestate.hands[-1].get_player(Seat.WEST))
engine.gamestate.hands[-1].players[1].called_melds.append(meld)
ts = nfromhand(engine.gamestate.hands[-1].players[3].hand, 4)
meld = Meld(variant=Mentsu.SHOUMINKAN, tiles=ts, called_tile=ts[3],
    called_player=engine.gamestate.hands[-1].get_player(Seat.WEST))
engine.gamestate.hands[-1].players[3].called_melds.append(meld)
ts = nfromhand(engine.gamestate.hands[-1].players[3].hand, 4)
meld = Meld(variant=Mentsu.ANKAN, tiles=ts)
engine.gamestate.hands[-1].players[3].called_melds.append(meld)
visual_context.set_gamestate(engine.gamestate)
# mock riichi
visual_context.state.bottom.riichi = 0
visual_context.state.right.riichi = 1
visual_context.state.top.riichi = 8
visual_context.state.left.riichi = 12
visual_context.need_update = True

"""
import time
time.sleep(15)
print("continue!")

engine.submit([CmdStartHand()])
visual_context.set_gamestate(engine.gamestate)
"""
