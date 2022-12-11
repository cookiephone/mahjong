def filter_commands_by_type(commands, types, negative=False):
    return [cmd for cmd in commands if isinstance(cmd, types) ^ negative]
