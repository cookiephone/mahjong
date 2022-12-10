from mahjong.commands.command import Command


class CmdStartHand(Command):

    def __init__(self):
        super().__init__("start hand")
    
    def execute(self, state):
        pass #TODO

    def valid(self, state):
        return True #TODO
