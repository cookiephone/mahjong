import mahjong.rules as rules
from mahjong.hand import Hand
from random import Random


class GameState:

    def __init__(self, seed=None, ruleset="default"):
        self.seed = seed
        self.rng = Random(self.seed)
        self.rule_context = rules.get_ruleset_context(ruleset)
        self.hands = []
        self.history = []
        self.current_hand = None
