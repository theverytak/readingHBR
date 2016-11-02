# -*- coding:utf-8 -*-
import itertools as it
import string
import os
import os.path
from .presets import (
    PURITY_HEURISTIC_PROBS,
    PURITY_HEURISTIC_DEFAULT_PROB
)


def noteng(c):
    return c in ['—', ',', '[', ']', '(', ')', '\n', "'", '"', ' ', '’'] or \
        c not in string.ascii_letters


def iseng(c):
    return c in ''.join(
        string.ascii_letters + 
        string.whitespace.replace('\n', '') +
        string.punctuation.replace('~', '') + '—' + '’'
    )


def notengline(l, t=None):
    words = l.split(sep=' ')
    try:
        return (
            all([noteng(c) for c in words[0]]) and
            all([noteng(c) for c in words[len(words) - 1]])
        ) or maybe_notengline(l, target=t)
    except IndexError:
        return True


def isengline(l, t=None):
    words = l.split(sep=' ')
    try:
        return (
            all([iseng(c) for c in words[0]]) and
            all([iseng(c) for c in words[len(words) - 1]])
        ) or maybe_engline(l, target=t)
    except IndexError:
        return True


def maybe_engline(l, target=None):
    p = PURITY_HEURISTIC_PROBS.get(target) or \
        PURITY_HEURISTIC_DEFAULT_PROB

    eng_count = sum([1 for c in l if iseng(c)])
    total_count = len(l)
    return (eng_count / total_count) >= p


def maybe_notengline(l, target=None):
    p = PURITY_HEURISTIC_PROBS.get(target) or \
        PURITY_HEURISTIC_DEFAULT_PROB

    noeng_count = sum([1 for c in l if noteng(c)])
    total_count = len(l)
    return (noeng_count / total_count) >= p


def ispureline(l, t=None):
    return notengline(l, t=t) or isengline(l, t=t)


def ltakewhile(*args, **kwargs):
    return list(it.takewhile(*args, **kwargs))


def ldropwhile(*args, **kwargs):
    return list(it.dropwhile(*args, **kwargs))


def stakewhile(*args, **kwargs):
    return ''.join(it.takewhile(*args, **kwargs))


def sdropwhile(*args, **kwargs):
    return ''.join(it.dropwhile(*args, **kwargs))
