import mahjong.rules as rules
from mahjong.hand import Hand
from random import Random


class GameState:

    def __init__(self, seed=None, ruleset="default"):
        self.seed = seed
        self.rng = Random(self.seed)
        self.rule_context = rules.get_ruleset_context(ruleset)
        self.command_history = []
        self.hands = []

    #TODO turn this into starthand command effect later
    def init_hand(self):
        self.hands.append(Hand(self))
