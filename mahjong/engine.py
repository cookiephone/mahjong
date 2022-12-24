from mahjong.game import GameState
from mahjong.commands import arbiter


class Engine:

    def __init__(self, seed=None, ruleset="default"):
        self.gamestate = GameState(seed=seed, ruleset=ruleset)

    def commands(self):
        commands = []  # TODO build all potentially valid commands using CommandOptions
        return [cmd for cmd in commands if cmd.valid(self.gamestate)]

    def submit(self, batch):
        winning_command = arbiter.filter_command_batch(self.gamestate, batch)
        winning_command(self.gamestate)
        self.gamestate.history.append(batch)
