"""Turn the PixelLab originals in art-src/ into the game's pictures in assets/.

Every picture is drawn at 2 pixels per game unit (the game's ART_RES).
Run from the game folder:  python art-src/prep.py
Then bump ASSET_V in index.html.
"""
from collections import deque
from pathlib import Path
from PIL import Image

SRC = Path(__file__).resolve().parent
OUT = SRC.parent / 'assets'
FRIEND_SIZE = 0.65   # the broom friends are shrunk to this size, so they don't crowd the witch
NEAR_SOLID = 80   # the near strips are cropped so their first solid row (the grass line) is this far down


def load(name):
    return Image.open(SRC / f'{name}.png').convert('RGBA')


def trim(im):
    return im.crop(im.getchannel('A').getbbox())


def rows(im):
    w, h = im.size
    a = im.getchannel('A').load()
    return [sum(1 for x in range(w) if a[x, y]) for y in range(h)]


def cut_sky(im, tol=12):
    """PixelLab paints a sky behind landscape strips. Flood-fill it away from the top row, stepping only
    to neighbours of a similar colour (so gradient skies go too), then drop anything left floating
    that doesn't reach the bottom."""
    w, h = im.size
    src = im.load()
    out = im.copy()
    px = out.load()
    seen = [[False] * h for _ in range(w)]
    todo = deque()
    for x in range(w):
        seen[x][0] = True
        todo.append((x, 0))
    while todo:
        x, y = todo.popleft()
        px[x, y] = (0, 0, 0, 0)
        r, g, b, _ = src[x, y]
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[nx][ny]:
                r2, g2, b2, a2 = src[nx, ny]
                if a2 == 0 or max(abs(r - r2), abs(g - g2), abs(b - b2)) <= tol:
                    seen[nx][ny] = True
                    todo.append((nx, ny))
    keep = [[False] * h for _ in range(w)]
    todo = deque((x, h - 1) for x in range(w) if px[x, h - 1][3])
    for x, y in todo:
        keep[x][y] = True
    while todo:
        x, y = todo.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not keep[nx][ny] and px[nx, ny][3]:
                keep[nx][ny] = True
                todo.append((nx, ny))
    for x in range(w):
        for y in range(h):
            if not keep[x][y]:
                px[x, y] = (0, 0, 0, 0)
    return out


def near(im, solid=None):
    """Crop a ground strip so its grass line sits NEAR_SOLID rows down (the game lines that up with the ground)."""
    w, h = im.size
    if solid is None:
        solid = next(y for y, n in enumerate(rows(im)) if n >= w * 0.98)
    top = solid - NEAR_SOLID
    out = Image.new('RGBA', (w, h - top), (0, 0, 0, 0))
    out.alpha_composite(im.crop((0, max(0, top), w, h)), (0, max(0, -top)))
    return out


def no_sun(im, rows_down):
    """Paint a (pale yellow) sun over with the colour of its sky band, or the mirrored repeat would show two suns."""
    px = im.load()
    for y in range(rows_down):
        for x in range(im.width):
            r, g, b, _ = px[x, y]
            if r > 235 and g > 225:
                px[x, y] = px[0, y]
    return im


def mean_rgb(im):
    n = s0 = s1 = s2 = 0
    for r, g, b, a in im.getdata():
        if a:
            n += 1; s0 += r; s1 += g; s2 += b
    return (s0 / n, s1 / n, s2 / n)


def bottom_colour(im):
    w = im.width
    y = max(y for y, n in enumerate(rows(im)) if n >= w * 0.9)
    return '#%02x%02x%02x' % tuple(int(c) for c in mean_rgb(im.crop((0, y - 3, w, y + 1))))


def sheet(frames):
    """Frames side by side, all cropped to the box that holds every frame, so they line up."""
    boxes = [f.getchannel('A').getbbox() for f in frames]
    box = (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))
    w, h = box[2] - box[0], box[3] - box[1]
    out = Image.new('RGBA', (w * len(frames), h), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        out.alpha_composite(f.crop(box), (i * w, 0))
    print(f'   {len(frames)} frames of {w}x{h}, crop box {box}')
    return out


def shrink(im, k):
    """Make a picture smaller and keep it crisp: resample it smoothly, then make every pixel either
    see-through or solid and snap its colour to the nearest colour of the original."""
    pal = sorted({px[:3] for px in im.getdata() if px[3] > 128})
    small = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    out = small.load()
    cache = {}
    for y in range(small.height):
        for x in range(small.width):
            r, g, b, a = out[x, y]
            if a < 110:
                out[x, y] = (0, 0, 0, 0)
                continue
            if (r, g, b) not in cache:
                cache[(r, g, b)] = min(pal, key=lambda c: (c[0] - r) ** 2 + (c[1] - g) ** 2 + (c[2] - b) ** 2)
            out[x, y] = cache[(r, g, b)] + (255,)
    return small


def centre(im, width):
    x = (im.width - width) // 2
    return im.crop((x, 0, x + width, im.height))


def save(im, name):
    OUT.mkdir(exist_ok=True)
    im.save(OUT / f'{name}.png', optimize=True)
    print(f'{name}.png', im.size)


# the witch and her friends
save(sheet([Image.open(SRC / 'frames' / f'witch-{i}.png').convert('RGBA') for i in range(8)]), 'witch-fly')
save(sheet([shrink(Image.open(SRC / 'frames' / f'cat-{i}.png').convert('RGBA'), FRIEND_SIZE) for i in range(8)]), 'cat')
for n in ('frog-crown', 'lantern', 'owl'):
    save(shrink(trim(load(n)), FRIEND_SIZE), n)
save(shrink(trim(load('unicorn')), FRIEND_SIZE).transpose(Image.FLIP_LEFT_RIGHT), 'unicorn')   # it faced left; it flies to the right
save(trim(load('cottage')), 'cottage')
save(trim(load('cauldron')), 'cauldron')

# ingredients and the things to avoid
for n in ('flower', 'mushroom', 'berry', 'leaf', 'apple', 'feather', 'snow', 'star', 'moon', 'drop'):
    save(trim(load(n)), f'ing-{n}')
for n in ('sock', 'shoe', 'fish', 'snail', 'comet'):
    save(trim(load(n)), n)

# obstacles: a cap at the gap, a body stacked down to the ground, and a pile hanging from the sky
save(trim(load('crown').crop((0, 0, 160, 86))), 'crown-meadow')      # leaves only, off a whole tree
save(trim(load('bark')), 'bark-oak')
save(trim(load('cloud')), 'cloud')
save(trim(load('fir').crop((0, 0, 128, 112))), 'fir')                 # without its stump
save(trim(load('bark-dark')), 'bark-dark')
save(trim(load('vines')), 'vines')
save(trim(load('hay-top')), 'hay-top')
save(trim(load('hay-top').crop((0, 30, 96, 85))), 'hay-bale')         # the bale without its pumpkin
save(trim(load('leaves-autumn')), 'leaves-autumn')
save(trim(load('rock-top')), 'rock-top')
save(centre(trim(load('rock')), 48), 'rock')                          # a little narrower than the snowy top
save(trim(load('cloud-snow')), 'cloud-snow')
save(trim(load('tower-roof').crop((0, 0, 96, 68))), 'tower-roof')     # the roof off a little tower
save(centre(load('tower'), 44), 'tower')                              # a little narrower than the roof
save(trim(load('cloud-night')), 'cloud-night')
save(trim(load('cloud-pink')), 'cloud-pink')

# background strips: far hills and the ground along the bottom
for lvl in ('meadow', 'forest', 'autumn', 'snow', 'night', 'rainbow'):
    far = load(f'hills-{lvl}-far')
    if lvl in ('autumn', 'night', 'rainbow'):
        # stripy or starry skies don't cut out cleanly: they stay, and the level's sky matches their top row
        if lvl == 'autumn':
            no_sun(far, 160)
        save(far, f'bg-{lvl}-far')
        print('   sky top', '#%02x%02x%02x' % far.getpixel((0, 0))[:3])
    else:
        save(trim(cut_sky(far)), f'bg-{lvl}-far')
    nr = load(f'hills-{lvl}-near')
    if lvl == 'rainbow':
        strip = near(nr.crop((0, 112, 400, 160)), solid=8)              # just the band of flowers
    else:
        strip = near(cut_sky(nr))
    save(strip, f'bg-{lvl}-near')
    print('   ground colour', bottom_colour(strip))
