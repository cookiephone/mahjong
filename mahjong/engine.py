from mahjong.game import GameState
from mahjong.commands import arbiter
from mahjong.commands.options import CommandOptions


class Engine:

    def __init__(self, seed=None, ruleset="default"):
        self.gamestate = GameState(seed=seed, ruleset=ruleset)
        self.options = CommandOptions(self.gamestate.rule_context)

    def commands(self):
        commands = []
        options = self.options.from_command_batch(self.gamestate.last_command_batch)
        for cmdtype, positions in options:
            commands.extend(cmdtype.build(self.gamestate, positions))
        return [cmd for cmd in commands if cmd.valid(self.gamestate)]

    def submit(self, batch):
        batch = arbiter.filter_command_batch(self.gamestate, batch)
        for command in batch:
            command(self.gamestate)
        self.gamestate.history.append(batch)
