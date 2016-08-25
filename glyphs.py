import urllib2
import os
import shutil
import unicodedata
from random import choice, randint
from PIL import Image
from unikovcode import MarkovData

image_file = 'unifont-9.0.01.bmp'
image_url = 'http://unifoundry.com/pub/unifont-9.0.01/unifont-9.0.01.bmp'

origin = (32, 64)
width, height = (16, 16)
cols = 0x100


def iterorigins():
    for i in xrange(0xffff + 1):
        if should_skip(i):
            continue
        row = i / cols
        col = i % cols
        x = origin[0] + width * col
        y = origin[1] + height * row
        yield (x, y)


def iterrects():
    for x, y in iterorigins():
        yield (x, y, x + width, y + height)


def should_skip(cp):
    return unicodedata.category(unichr(cp)).startswith('C')


class GlyphGenerator(object):
    def __init__(self, mdata, mode):
        self._mdata = mdata
        self._mode = mode

    def generate(self):
        result = choice(self._mdata.seeds)
        order = len(result)
        while len(result) < 256:
            values = self._mdata.chains.get(str(result[-order:]))
            value = choice([v for v in values if v is not None]) \
                    if values else None
            if value is None:
                value = choice([0, 0xff])
            result.append(value)
        glyph = Image.new(self._mode, (width, height))
        glyph.putdata(result)
        return glyph


def get_image():
    if not os.path.isfile(image_file):
        data = urllib2.urlopen(image_url)
        with open(image_file, 'wb') as out:
            shutil.copyfileobj(data, out)
    return Image.open(image_file)


def get_raw_data(image):
    return [list(image.crop(r).getdata()) for r in iterrects()]


def get_generator():
    uimage = get_image()
    raw_data = get_raw_data(uimage)
    mdata = MarkovData(raw_data, order=width)
    return GlyphGenerator(mdata, uimage.mode)


def main():
    generator = get_generator()
    for _ in xrange(10):
        result = generator.generate()
        size = tuple([d * 3 for d in result.size])
        result.resize(size).show()


if __name__ == '__main__':
    main()
