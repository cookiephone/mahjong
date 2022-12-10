from mahjong.game import GameState
from mahjong.commands import arbiter


class Engine:

    def __init__(self, seed=None, ruleset="default"):
        self.gamestate = GameState(seed=seed, ruleset=ruleset)

    def commands(self):
        commands = [] #TODO build all potentially valid commands
        return [cmd for cmd in commands if cmd.valid(self.gamestate)]

    def submit(self, commands):
        commands = arbiter.filter_commands(commands)
        for cmd in commands:
            cmd.execute(self.gamestate)
