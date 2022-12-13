from mahjong.commands.command import Command
from mahjong.hand import Hand


class CmdStartHand(Command):

    def __init__(self):
        super().__init__("start hand")

    def execute(self, state):
        hand = Hand(state)
        state.hands.append(hand)
        state.current_hand = hand

    def valid(self, state):
        return True  # TODO
