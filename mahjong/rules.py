import importlib.resources as resources
import json


def get_ruleset_context(ruleset="default"):
    return json.loads(resources.files("mahjong.resources.rulesets").joinpath(f"{ruleset}.json").read_text())
