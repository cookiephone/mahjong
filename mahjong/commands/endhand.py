from mahjong.commands.command import Command


class CmdEndHand(Command):

    def __init__(self):
        super().__init__("end hand")
    
    def execute(self, state):
        pass #TODO

    def valid(self, state):
        return True #TODO
