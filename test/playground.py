# pylint: skip-file

import make
make.build_and_install(deps=False, extras=["dev"])

from mahjong import Engine, GameState, Player, Meld, Mentsu
from mahjong.commands import CmdStartHand, CommandOptions, CmdKan
from mahjong.scoring import HandExplorer
from mahjong.utils.parsing import tileset_from_string, tileset_to_string


engine = Engine(seed=0)
cmds = engine.commands()
engine.submit(cmds)

#options = CommandOptions(engine.gamestate.rule_context)
#print(options(CmdKan))

"""
player = Player(None, 0)
player.hand = tileset_from_string("6667899mWWWW", unique_uids=True)
player.called_melds = [Meld(Mentsu.MINJUN, tileset_from_string("123p"))]

explorer = HandExplorer(player)
outcomes = set(explorer.explore())

print("===================")
print("hand: 6667899mWWWW")
print("===================")
print("exploration yields...")
for outcome in outcomes:
    meldstr = " + ".join(f"[{meld.variant}:{tileset_to_string(meld.tiles)}]" for meld in outcome.implicit_melds)
    print(f"interpretation: {tileset_to_string(outcome.unmelded_tiles):<15} | {meldstr}")
"""
