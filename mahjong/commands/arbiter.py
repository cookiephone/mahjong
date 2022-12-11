from mahjong.commands.chii import CmdChii
from mahjong.commands.pon import CmdPon
from mahjong.commands.kan import CmdKan, CmdAddedKan
from mahjong.commands.ron import CmdRon
from mahjong.commands.endhand import CmdEndHand


def _filter_by_type(commands, types, negative=False):
    return [cmd for cmd in commands if isinstance(cmd, types) ^ negative]

def _handle_multi_ron(state, batch):
    rule = state.rule_context.double_ron if len(batch) == 2 else state.rule_context.triple_ron
    match rule:
        case "all":
            return batch
        case "bump":
            target = batch[0].called_player
            bump_order = state.current_hand.bump_order(target)
            return next(cmd for player in bump_order for cmd in batch if cmd.player == player)
        case "cancel":
            return [CmdEndHand()]

def rule_ron_priority(state, batch):
    ron_commands = _filter_by_type(batch, CmdRon)
    match len(ron_commands):
        case 0:
            pass
        case 1:
            return ron_commands
        case 2 | 3:
            return _handle_multi_ron(state, ron_commands)

def rule_pon_kan_priority(state, batch):
    pon_kan_commands = _filter_by_type(batch, (CmdPon, CmdKan, CmdAddedKan))
    if not pon_kan_commands:
        return batch
    return _filter_by_type(batch, CmdChii, negative=True)

def filter_command_batch(state, batch):
    rules = [rule_ron_priority, rule_pon_kan_priority]
    for rule in rules:
        batch = rule(state, batch)
    return batch
