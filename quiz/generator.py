# -*- coding:utf-8 -*-
import re
import itertools as it
import json
import os
import os.path
from collections import OrderedDict
from .parser import Parser


class Generator(object):
    DEFAULT_TARGETS=['단어', '문장']
    DEFAULT_BUILD_PATH = './.quiz.json'

    QUIZ_TITLE_KEY = 'title'
    QUIZ_NAME_SEPARATOR = ' - '

    NOTE_EXTNAME = '.md'
    NOTE_REGEX = r'(\d+\.)?\d+\.\d+{}'.format(NOTE_EXTNAME)

    def __init__(self, root='./articles'):
        self._root = os.path.normpath(root)

    def generate_quiz(self, targets=None, to=None):
        quiz = OrderedDict()
        for note in self._available_notes():
            for target in targets or self.DEFAULT_TARGETS:
                # set parser and note name
                parser = Parser(target=target)
                name = self._note_name(note)
                # fill in quiz data
                quiz[name] = quiz.get(name) or {}
                quiz[name][target] = parser.parse(note)
                quiz[name][self.QUIZ_TITLE_KEY] = parser.parse_title(note)

        # reverse the order and dump into the target json file.
        sorted = OrderedDict(reversed(list(quiz.items())))
        with open(to or self.DEFAULT_BUILD_PATH, 'w', encoding='UTF-8') as f:
            json.dump(sorted, f, indent=4)

    def _available_notes(self):
        # recursively find notes from the root directory
        notes = []
        regex = re.compile(self.NOTE_REGEX)
        for root, subfolders, files in os.walk(self._root):
            notes += [os.path.join(root, f) for f in files if regex.findall(f)]
        return notes

    def _note_name(self, path):
        # split the path into segments and find name segments
        root_segments_len = len(self._root.split(os.path.sep))
        path_segments = path.split(os.path.sep)
        name_segments = path_segments[root_segments_len:]

        # truncate file extension from the note name
        *rest, basename = name_segments
        return self.QUIZ_NAME_SEPARATOR.join([
            *rest, basename.replace(self.NOTE_EXTNAME, '')
        ])
