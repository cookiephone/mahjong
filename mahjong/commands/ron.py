from mahjong.commands.command import Command


class CmdRon(Command):

    def __init__(self, player):
        super().__init__("ron")
        self.player = player
    
    def execute(self, state):
        pass

    def valid(self, state):
        return True #TODO
