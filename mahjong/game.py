from random import Random
from dataclasses import dataclass
from typing import Any
from mahjong import rules


@dataclass(init=False)
class GameState:

    seed: Any
    rng: Any
    rule_context: Any
    hands: Any
    history: Any
    current_hand: Any

    def __init__(self, seed=None, ruleset="default"):
        self.seed=seed
        self.rng=Random(seed)
        self.rule_context=rules.get_ruleset_context(ruleset)
        self.hands=[]
        self.history=[]
        self.current_hand=None

    @property
    def last_command_batch(self):
        try:
            return self.history[-1]
        except IndexError:
            return None

    @property
    def round(self):
        n_non_renchan = len([hand for hand in self.hands if hand.honba == 0])
        return 1 + (n_non_renchan - 1) % 4

    @property
    def last_active_seat(self):
        try:
            return self.history[-1][0].player.seat
        except (IndexError, AttributeError):
            return None
