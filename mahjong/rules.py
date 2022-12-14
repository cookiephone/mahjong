from importlib import resources
import json
from types import SimpleNamespace


def get_ruleset_context(ruleset="default"):
    data = json.loads(resources.files("mahjong.resources.rulesets").joinpath(
        f"{ruleset}.json").read_text())
    return SimpleNamespace(**data)
