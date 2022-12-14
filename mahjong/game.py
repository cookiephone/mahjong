from random import Random
from types import SimpleNamespace
from mahjong import rules


def gamestate(seed=None, ruleset="default"):
    return SimpleNamespace(
        seed=seed,
        rng=Random(seed),
        rule_context=rules.get_ruleset_context(ruleset),
        hands=[],
        history=[],
        current_hand=None)
