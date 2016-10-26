# -*- coding:utf-8 -*-
import itertools as it
import re
import os.path
from .utils import noteng, notengline, iseng, isengline, ispureline


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
        return {k: v for k, v in self._normalize_items(target_items)}

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
        try:
            title, content = content_regex.findall(text)[0]
            return content
        except IndexError:
            return ''

    def _parse_content(self, content):
        # normalize content and split into lines
        content = self._normalize_content(content)
        lines = content.splitlines()

        # store indicies of lines that has been parsed 
        parsed = set()
        # store parsed english-translation tuples
        items = []

        for i, line in enumerate(lines):
            # jump the line if it has been parsed already
            if i in parsed:
                continue
            # start line reducing process if given line is mixed up with 
            # english and non-english
            elif not ispureline(line):
                while line:
                    # take english and reduce content
                    english = ''\
                        .join(it.takewhile(lambda c: iseng(c), line))\
                        .strip()
                    line = ''\
                        .join(it.dropwhile(lambda c: iseng(c), line))\
                        .strip()

                    print('============================')
                    print('english: {}'.format(english))

                    # take translation and reduce content
                    translation = ''\
                        .join(it.takewhile(lambda c: noteng(c), line))\
                        .strip()
                    line = ''\
                        .join(it.dropwhile(lambda c: noteng(c), line))\
                        .strip()

                    print('============================')
                    print('korean: {}'.format(translation))

                    # append items to the list and mark the line as parsed
                    items.append((english, translation))
                    parsed.add(i)
            # otherwise when the line is pure english or pure non-english
            else:
                reduced = it.dropwhile(lambda l: isengline(l), lines[i:])
                english_lines = it.takewhile(lambda l: isengline(l), lines[i:])
                english = '\n'.join(english_lines).strip()

                reduced = it.dropwhile(lambda l: notengline(l), reduced)
                translation_lines = it.takewhile(lambda l: notengline(l), reduced)
                translation = '\n'.join(translation_lines).strip()

                indicies = list(range(
                    i, i + len(english_lines) + len(translation_lines)
                ))

                # append items to the list and mark lines as parsed
                items.append((english, translation))
                parsed.union(indicies)

        return items

    def _normalize_content(self, content):
        norm_regex = re.compile(r'\n+')
        content = norm_regex.sub('\n', content)
        content = content.replace('\xa0', '')
        return content.strip()

    def _normalize_items(self, items):
        return [(k, v) for k, v in items if v]
