import string
import os
import os.path
import re


def noteng(c):
    return c in ['—', ',', '[', ']', '(', ')', '\n', "'", '"'] or \
        c not in [*string.ascii_letters,]


def iseng(c):
    return c in [
        *string.ascii_letters,
        *string.whitespace.replace('\n', ''),
        *string.punctuation.replace('~', ''),
        '—'
    ]


def notengline(l):
    words = l.split(sep=' ')
    try:
        return all([noteng(c) for c in words[0]]) and \
            all([noteng(c) for c in words[len(words) - 1]])
    except IndexError:
        return True


def isengline(l):
    words = l.split(sep=' ')
    try:
        return all([iseng(c) for c in words[0]]) and \
            all([noteng(c) for c in words[len(words) - 1]])
    except IndexError:
        return True


def available_notes(root='./'):
    note_regex = re.compile(r'\d+\.\d+.md')
    return [os.path.join(root, f) for f in os.listdir(root) 
            if os.path.isfile(f) and note_regex.findall(f)]
