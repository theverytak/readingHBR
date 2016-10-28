# -*- coding:utf-8 -*-
import itertools as it
import re
import os.path
from .utils import (
    noteng, notengline, 
    iseng, isengline, 
    ispureline,
    ltakewhile,
    ldropwhile,
    stakewhile,
    sdropwhile,
)


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
        # Alias
        t = self._target

        # Normalize content and split into lines
        content = self._normalize_content(content)
        lines = content.splitlines()

        # store indicies of lines that has been parsed 
        parsed = set()

        # store parsed english-translation tuples
        items = []

        for i, line in enumerate(lines):
            # Jump the line if it has been parsed already
            if i in parsed:
                continue
            # Start line reducing process if given line is mixed up with 
            # english and non-english
            elif not ispureline(line):
                while line:
                    # Take english and reduce content
                    english = stakewhile(lambda c: iseng(c), line).strip()
                    line = sdropwhile(lambda c: iseng(c), line).strip()

                    # Take translation and reduce content
                    translation = stakewhile(lambda c: noteng(c), line).strip()
                    line = sdropwhile(lambda c: noteng(c), line).strip()

                    # Append items to the list and mark the line as parsed
                    items.append((english, translation))
                    parsed.add(i)
            # Otherwise when the line is pure english or pure non-english
            else:
                # Take english lines and reduce lines
                english_lines = ltakewhile(lambda l: isengline(l, t=t), lines[i:])
                english = '\n'.join(english_lines).strip()
                reduced = it.dropwhile(lambda l: isengline(l, t=t), lines[i:])

                # Take translation and reduce lines
                translation_lines = ltakewhile(lambda l: notengline(l, t=t), reduced)
                translation = '\n'.join(translation_lines).strip()
                reduced = it.dropwhile(lambda l: notengline(l, t=t), reduced)

                # Calculate how far we have parsed through the lines
                distance = len(english_lines + translation_lines)
                indicies = list(range(i, i + distance))

                # Append items to the list and mark lines as parsed
                items.append((english, translation))
                parsed.update(indicies)

        return items

    def _normalize_content(self, content):
        norm_regex = re.compile(r'\n+')
        content = norm_regex.sub('\n', content)
        content = content.replace('\xa0', '')
        return content.strip()

    def _normalize_items(self, items):
        return [(k, [*v.splitlines()]) for k, v in items if v]
