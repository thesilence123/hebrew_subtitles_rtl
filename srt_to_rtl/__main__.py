from bidi.algorithm import get_display
import sys
import unicodedata
from datetime import datetime as dt
import string
import logging
import random


logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(levelname)-s %(name)-2s %(funcName)20s() %(message)s',
                    datefmt='%m-%d %H:%M:%S:%M')
logger = logging.getLogger(__name__)


def is_all_punctutions(s):
    return all(map(lambda x: unicodedata.category(x).startswith('P'), s))


def count_punctuation_in_a_row_from_start(s):
    for i in xrange(len(s), 0, -1):
        if is_all_punctutions(s[: i]): return i
    return 0


def count_punctuation_in_a_row_from_end(s):
    for i in xrange(len(s)):
        if is_all_punctutions(s[i: len(s)]):
            return len(s) - i
    return 0


def fix(line):
    from_the_start = line[: count_punctuation_in_a_row_from_start(line)]
    from_the_middle = line[count_punctuation_in_a_row_from_start(line): len(line) - count_punctuation_in_a_row_from_end(
        line)]
    from_the_end = line[len(line) - count_punctuation_in_a_row_from_end(line): ]
    return u''.join(
        [u''.join(reversed(from_the_end)),
         from_the_middle,
         u''.join(reversed(from_the_start))
         ])


class Commenter(object):
    def __init__(self):

        self.things_to_do = {'': ['Randomizing numbers', 'Taking a shower', 'Looking nice', 'Playing poker',
                                  'Going to church', 'Playing with bananas'],
                             'Fixing the ': ['the dishwasher', 'my life', 'subtitles', 'sun', 'core', 'moon', 'belief']}
    def get_comment(self):
        return self.randomize() + '...'


    def randomize(self):
        action = random.choice(self.things_to_do.keys())
        while not self.things_to_do[action]:
            action = random.choice(self.things_to_do.keys())
        random.shuffle(self.things_to_do[action])
        thing = self.things_to_do[action].pop()
        return action + thing


def main(args):
    logger = logging.getLogger(__name__)
    logger.debug('In main')



    with open(args[0], 'r') as f:
        lines = (f.read()).decode('windows-1255').splitlines()

    logger.info('Fixing...')
    commenter = Commenter()
    for i, line in enumerate(lines[:]):
        if i % 500 == 499:
            print commenter.get_comment()
        lines[i] = fix(line)

    logger.debug('Finished fixing. First 10 lines: %s' % string.join(lines[100:200: 3], '\n'))
    print 'Writing file: %s' % args[1]
    with open(args[1], 'w') as f:
        for line in lines:
            f.write('%s\n' % line.encode('windows-1255'))
    print 'Done.'


if __name__ == '__main__':
    main(sys.argv[1:])
