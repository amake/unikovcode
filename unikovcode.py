from __future__ import print_function
import os
import urllib2
import logging
from collections import defaultdict
from random import choice, randint
from string import hexdigits, ascii_lowercase, ascii_uppercase

data_url = 'http://unicode.org/Public/UNIDATA/UnicodeData.txt'
data_file = 'UnicodeData.txt'
hex_chars = ''.join(set(hexdigits) - set(ascii_lowercase))
non_hex_chars = ''.join(set(ascii_uppercase) - set(hex_chars))


def iterslice(items, size):
    for i in xrange(0, len(items) - size + 1):
        slse = items[i:i + size]
        trailing =  items[i + size] if i + size < len(items) else None
        yield slse, trailing


class MarkovData(object):
    def __init__(self, raw_data, order=5):
        self.raw_data = raw_data
        self.order = order
        self.chains = self._train()
        self.seeds = self._get_seeds()
        logging.debug('Seeds: %d' % len(self.seeds))
        logging.debug('Chain keys: %d' % len(self.chains))
        logging.debug('Random key: %s' % choice(self.chains.keys()))
        
    def _train(self):
        result = defaultdict(list)
        for item in self.raw_data:
            for key, value in iterslice(item, self.order):
                result[str(key)].append(value)
        return dict(result)

    def _get_seeds(self):
        return [item[:self.order] for item in self.raw_data]


class UnicodeGenerator(object):
    def __init__(self, mdata):
        self._mdata = mdata

    def _gen_hex(self):
        plane_max = choice([0xFFFF, 0x10FFFF])
        codepoint = '%04X' % randint(0, plane_max)
        chars = list(codepoint)
        replace_at = randint(0, len(chars) - 1)
        chars[replace_at] = choice(non_hex_chars)  # for lulz
        return ''.join(chars)

    def _gen_desc(self):
        result = choice(self._mdata.seeds)
        order = len(result)
        while True:
            values = self._mdata.chains.get(str(result[-order:]))
            if not values:
                break
            value = choice(values)
            if not value:
                break
            result += value
        return self._gen_desc() if result in self._mdata.raw_data else result

    def generate(self):
        return u'\uFFFD U+%s %s' % (self._gen_hex(), self._gen_desc())


def get_raw_data():
    if not os.path.isfile(data_file):
        data = urllib2.urlopen(data_url)
        with open(data_file, 'w') as out:
            out.write(data.read())
    return open(data_file)


def get_names(record):
    '''See http://www.unicode.org/reports/tr44/#UnicodeData.txt'''
    split = record.split(';')
    character_name = split[1]
    unicode10name = split[10]
    result = [character_name]
    if unicode10name:
        result.append(unicode10name)
    return result

def get_codepoint_names():
    with get_raw_data() as in_data:
        cp_names = [name for line in in_data for name in get_names(line)]
    return [name for name in cp_names if not name.startswith('<')]


generator = None


def get_generator():
    global generator
    if generator is None:
        data = MarkovData(get_codepoint_names(), order=5)
        generator = UnicodeGenerator(data)
    return generator


def main():
    generator = get_generator()
    for _ in xrange(10):
        print(generator.generate())


if __name__ == '__main__':
    main()
