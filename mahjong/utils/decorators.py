from functools import wraps
from collections import defaultdict


def dedupe_generator(generator):
    observed = defaultdict(lambda: False)
    @wraps(generator)
    def wrapper(*args, **kwargs):
        for elem in generator(*args, **kwargs):
            if not observed[elem]:
                yield elem
                observed[elem] = True
    return wrapper
