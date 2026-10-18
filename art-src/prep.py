"""Turn the PixelLab originals in art-src/ into the game's pictures in assets/.

Run from the game folder:  python art-src/prep.py
Then bump ASSET_V in index.html.
"""
import sys
from collections import deque
from pathlib import Path
from PIL import Image

SRC = Path(__file__).resolve().parent
OUT = SRC.parent / 'assets'


def load(name):
    return Image.open(SRC / f'{name}.png').convert('RGBA')


def trim(im):
    return im.crop(im.getchannel('A').getbbox())


def cut_sky(im, tol=18):
    """PixelLab paints a sky behind landscape strips: flood-fill it away from the top row."""
    orig = im.load()
    im = im.copy()
    w, h = im.size
    px = im.load()
    seen = set()
    todo = deque((x, 0) for x in range(w))
    while todo:
        x, y = todo.popleft()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h):
            continue
        seen.add((x, y))
        r, g, b, a = orig[x, y]
        ref = orig[x, 0]
        if a and max(abs(r - ref[0]), abs(g - ref[1]), abs(b - ref[2])) > tol:
            continue
        px[x, y] = (0, 0, 0, 0)
        todo.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return im


def save(im, name):
    OUT.mkdir(exist_ok=True)
    im.save(OUT / f'{name}.png', optimize=True)
    print(f'{name}.png', im.size)


save(trim(load('witch-c')), 'witch')
save(trim(load('cottage')), 'cottage')
save(trim(load('cauldron')), 'cauldron')
save(trim(load('cloud')), 'cloud')
save(trim(load('flower')), 'ing-flower')
# the crown came with its own trunk and a tuft of grass: keep the leaves only
save(trim(load('crown').crop((0, 0, 80, 45))), 'crown-meadow')
# bark is stacked up each trunk, so keep its full height
bark = load('bark')
save(bark.crop((5, 0, 29, 128)), 'bark-oak')
save(trim(cut_sky(load('hills-far'))), 'bg-meadow-far')
save(load('hills-near').crop((0, 30, 400, 80)), 'bg-meadow-near')
