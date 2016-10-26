# -*- coding:utf-8 -*-
import itertools as it
import re
import os.path
from . import utils


class Parser(object):
    TITLE_UNDER_REGEX_FORMAT = r'\s*([^\n=]+)\n=+'
    TITLE_BOLD_REGEX_FORMAT = r'\*\*(.+?)\*\*'
    CONTENT_REGEX_FORMAT = r'(\*\*{}\*\*)\s+(?P<lines>[^*]+)'

    def __init__(self, root='./', target='단어'):
        self._root = root
        self._target = target

    def parse(self, path):
        target_content = self._parse_text(self._read_text(path))
        target_items = self._parse_content(target_content)
        return {k: v for k, v in self._normalize(target_items)}

    def parse_title(self, path):
        text = self._read_text(path)
        under_regex = re.compile(self.TITLE_UNDER_REGEX_FORMAT)
        bold_regex = re.compile(self.TITLE_BOLD_REGEX_FORMAT)

        try:
            return under_regex.findall(text)[0]
        except IndexError:
            return bold_regex.findall(text)[0]

    def _read_text(self, path):
        path = os.path.join(self._root, path)
        with open(path, 'r', encoding='UTF-8') as f:
            return f.read()

    def _parse_text(self, text):
        content_regex = self.CONTENT_REGEX_FORMAT.format(self._target)
        content_regex = re.compile(content_regex)
        title, content = content_regex.findall(text)[0]
        return content

    def _parse_content(self, content):
        # first normalize unicode
        content = content.replace('\xa0', '')

        # start reducing process
        items = []
        while content:
            # take english and reduce content
            english = ''.join(it.takewhile(lambda c: utils.iseng(c), content)).strip()
            content = ''.join(it.dropwhile(lambda c: utils.iseng(c), content)).strip()
            # take translation and reduce content
            translation = ''.join(it.takewhile(lambda c: utils.noteng(c), content)).strip()
            content = ''.join(it.dropwhile(lambda c: utils.noteng(c), content)).strip()
            # append items to the list
            items.append((english, translation))
        return items

    def _normalize(self, items):
        return [(k, v) for k, v in items if v]
