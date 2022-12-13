from importlib import resources
import json
from mahjong.utils.attrdict import AttrDict


def get_ruleset_context(ruleset="default"):
    context = AttrDict()
    data = json.loads(resources.files("mahjong.resources.rulesets").joinpath(
        f"{ruleset}.json").read_text())
    context.update(data)
    return context
