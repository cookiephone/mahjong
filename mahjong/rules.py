from mahjong.utils.attrdict import AttrDict
import importlib.resources as resources
import json


def get_ruleset_context(ruleset="default"):
    context = AttrDict()
    data = json.loads(resources.files("mahjong.resources.rulesets").joinpath(f"{ruleset}.json").read_text())
    context.update(data)
    return context
