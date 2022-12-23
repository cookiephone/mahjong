# pylint: skip-file

import make
make.build_and_install(deps=False, extras=["dev"])

from mahjong.engine import Engine
from mahjong.commands.starthand import CmdStartHand


engine = Engine(seed=0)

engine.submit([CmdStartHand()])
