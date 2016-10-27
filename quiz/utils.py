# -*- coding:utf-8 -*-
import string
import os
import os.path
import re


def noteng(c):
    return c in ['—', ',', '[', ']', '(', ')', '\n', "'", '"', ' '] or \
        c not in string.ascii_letters


def iseng(c):
    return c in ''.join(
        string.ascii_letters + 
        string.whitespace.replace('\n', '') +
        string.punctuation.replace('~', '') + '—'
    )


def notengline(l):
    words = l.split(sep=' ')
    try:
        return (
            all([noteng(c) for c in words[0]]) and
            all([noteng(c) for c in words[len(words) - 1]])
        ) or maybe_notengline(l)
    except IndexError:
        return True


def isengline(l):
    words = l.split(sep=' ')
    try:
        return (
            all([iseng(c) for c in words[0]]) and
            all([iseng(c) for c in words[len(words) - 1]])
        ) or maybe_engline(l)
    except IndexError:
        return True


def maybe_engline(l, p=0.7):
    eng_count = sum([1 for c in l if iseng(c)])
    total_count = len(l)
    return (eng_count / total_count) >= p


def maybe_notengline(l, p=0.7):
    noeng_count = sum([1 for c in l if noteng(c)])
    total_count = len(l)
    return (noeng_count / total_count) >= p


def ispureline(l):
    return notengline(l) or isengline(l)


def available_notes(root='./'):
    note_regex = re.compile(r'\d+\.\d+.md')
    return [os.path.join(root, f) for f in os.listdir(root) 
            if os.path.isfile(f) and note_regex.findall(f)]
