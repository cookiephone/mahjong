from mahjong.game import GameState
from mahjong.commands import arbiter


class Engine:

    def __init__(self, seed=None, ruleset="default"):
        self.gamestate = GameState(seed=seed, ruleset=ruleset)

    def commands(self):
        commands = [] #TODO build all potentially valid commands
        return [cmd for cmd in commands if cmd.valid(self.gamestate)]

    def submit(self, batch):
        batch = arbiter.filter_command_batch(batch)
        for cmd in batch:
            cmd.execute(self.gamestate)
