import itertools
import json
import os.path
from collections import OrderedDict
from .parser import Parser
from .utils import available_notes


class Generator(object):
    DEFAULT_TARGETS=['단어', '문장']
    DEFAULT_BUILD_PATH = './.quiz.json'
    QUIZ_TITLE_KEY = 'title'

    def __init__(self, root='./'):
        self._root = root

    def generate_quiz(self, targets=None, to=''):
        to = to or self.DEFAULT_BUILD_PATH
        targets = targets or self.DEFAULT_TARGETS
        notes = available_notes()

        quiz = OrderedDict()
        for note in notes:
            for target in targets:
                # set parser and note name
                parser = Parser(root=self._root, target=target)
                name = os.path.basename(note)
                # fill in quiz data
                quiz[name] = quiz.get(name) or {}
                quiz[name][target] = parser.parse(note)
                quiz[name][self.QUIZ_TITLE_KEY] = parser.parse_title(note)

        sorted = OrderedDict(reversed(list(quiz.items())))
        with open(to, 'w', encoding='utf-8') as f:
            json.dump(sorted, f, indent=4)
