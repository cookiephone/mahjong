from mahjong.commands.chii import CmdChii
from mahjong.commands.pon import CmdPon
from mahjong.commands.kan import CmdKan, CmdAddedKan
from mahjong.commands.ron import CmdRon
from mahjong.commands.endhand import CmdEndHand
from mahjong.utils import helpers


def _handle_multi_ron(state, ron_commands, rule):
    match rule:
        case "all":
            return ron_commands
        case "bump":
            target = ron_commands[0].called_player
            bump_order = state.current_hand.bump_order(target)
            for cmd in ron_commands:
                for player in bump_order:
                    if cmd.player == player:
                        return [cmd]
        case "cancel":
            return [CmdEndHand()]

def rule_ron_priority(state, batch):
    ron_commands = helpers.filter_commands_by_type(batch, CmdRon)
    other_commands = helpers.filter_commands_by_type(batch, CmdRon, negative=True)
    match len(ron_commands):
        case 0 | 1:
            return batch
        case 2:
            updated = _handle_multi_ron(state, ron_commands, state.rule_context.double_ron)
            return other_commands + updated
        case 3:
            updated = _handle_multi_ron(state, ron_commands, state.rule_context.triple_ron)
            return other_commands + updated

def rule_pon_kan_priority(_, batch):
    pon_kan_commands = helpers.filter_commands_by_type(
        batch, (CmdPon, CmdKan, CmdAddedKan))
    if not pon_kan_commands:
        return batch
    return helpers.filter_commands_by_type(batch, CmdChii, negative=True)

def filter_command_batch(state, batch):
    rules = [rule_ron_priority, rule_pon_kan_priority]
    for rule in rules:
        batch = rule(state, batch)
    return batch
