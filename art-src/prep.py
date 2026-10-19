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
TREE_SIZE = 0.6     # the whole trees are shrunk to this size
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


def frames(name, count, k=1, flip=False):
    """An animation's frames from art-src/frames (frame 0 is the picture it was made from)."""
    out = []
    for i in range(count):
        f = Image.open(SRC / 'frames' / f'{name}-{i}.png').convert('RGBA')
        if k != 1:
            f = shrink(f, k)
        if flip:
            f = f.transpose(Image.FLIP_LEFT_RIGHT)
        out.append(f)
    return out


def cut_white(im, tol=20):
    """Clear a plain white background, flood-filling in from the edges."""
    w, h = im.size
    px = im.load()
    todo = deque([(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)] + [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)])
    seen = set()
    while todo:
        x, y = todo.popleft()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h):
            continue
        seen.add((x, y))
        if min(px[x, y][:3]) < 255 - tol:
            continue
        px[x, y] = (0, 0, 0, 0)
        todo.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    for y in range(h):   # and the bits of background showing through between branches
        for x in range(w):
            if min(px[x, y][:3]) > 245:
                px[x, y] = (0, 0, 0, 0)
    return im


def tree(im, k, cap_end, body_end, name):
    """Cut a whole tree into its top (crown and the top of the trunk), a slice of trunk that the game stacks
    down to the ground, and its foot (the roots). All three keep the full width, so they line up."""
    im = shrink(im, k)
    w, h = im.size
    top = im.getchannel('A').getbbox()[1]
    a, b = round(cap_end * k), round(body_end * k)
    save(im.crop((0, top, w, a)), f'{name}-top')
    save(im.crop((0, a, w, b)), f'{name}-trunk')
    save(trim_bottom(im.crop((0, b, w, h))), f'{name}-foot')


def trim_bottom(im):
    box = im.getchannel('A').getbbox()
    return im.crop((0, 0, im.width, box[3]))


def centre(im, width):
    x = (im.width - width) // 2
    return im.crop((x, 0, x + width, im.height))


def save(im, name):
    OUT.mkdir(exist_ok=True)
    im.save(OUT / f'{name}.png', optimize=True)
    print(f'{name}.png', im.size)


# the witch and her friends
# The witch's animations all share one crop box, so her body, broom and friends stay put whichever plays:
# flying (8 frames, a loop), and swoop, cheer, wave and bonk (frames 1-6 of each; frame 0 is the flying pose).
WITCH_ANIMS = {'fly': [f'witch-{i}' for i in range(8)]}
for n in ('swoop', 'cheer', 'wave', 'bonk'):
    if (SRC / 'frames' / f'witch-{n}-1.png').exists():
        WITCH_ANIMS[n] = [f'witch-{n}-{i}' for i in range(1, 7)]
wf = {n: [Image.open(SRC / 'frames' / f'{f}.png').convert('RGBA') for f in fs] for n, fs in WITCH_ANIMS.items()}
boxes = [f.getchannel('A').getbbox() for fs in wf.values() for f in fs]
WBOX = (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))
print('   witch crop box', WBOX)
for n, fs in wf.items():
    w, h = WBOX[2] - WBOX[0], WBOX[3] - WBOX[1]
    out = Image.new('RGBA', (w * len(fs), h), (0, 0, 0, 0))
    broom = []
    for i, f in enumerate(fs):
        c = f.crop(WBOX)
        out.alpha_composite(c, (i * w, 0))
        px = c.load(); x = 85 + 11 - WBOX[0]   # the broom handle in front of her
        col = [y for y in range(h) if px[x, y][3] and px[x, y][0] > 80 and px[x, y][0] > px[x, y][2] + 30 and px[x, y][1] < px[x, y][0]]
        broom.append(min(col) if col else None)
    save(out, f'witch-{n}')
    print(f'   witch-{n} broom tops', broom)
save(sheet(frames('cat', 8, FRIEND_SIZE)), 'cat')
save(sheet(frames('frog', 7, FRIEND_SIZE)), 'frog-crown')                     # frame 0 sits still; 1-6 flick the tongue
save(sheet(frames('unicorn', 8, FRIEND_SIZE, flip=True)), 'unicorn')        # it faced left; it flies to the right
save(sheet(frames('bird', 6)), 'bird')
save(sheet(frames('bat', 6, flip=True)), 'bat')                             # it faced right; the flocks fly left
save(sheet(frames('cauldron', 8)), 'cauldron')
for n in ('lantern', 'owl'):
    save(shrink(trim(load(n)), FRIEND_SIZE), n)
save(trim(load('cottage2-b')), 'cottage')

# ingredients and the things to avoid
for n in ('flower', 'mushroom', 'berry', 'leaf', 'apple', 'feather', 'snow', 'star', 'moon', 'drop'):
    save(trim(load(n)), f'ing-{n}')
for n in ('sock', 'shoe', 'fish', 'snail', 'comet'):
    save(trim(load(n)), n)

# obstacles: a cap at the gap, a body stacked down to the ground, and a pile hanging from the sky
tree(cut_white(load('tree-oak')), TREE_SIZE, 184, 208, 'oak')
save(trim(load('cloud')), 'cloud')
tree(load('tree-fir'), TREE_SIZE, 200, 232, 'fir')
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
# more obstacles, so a level isn't the same thing over and over: things that stand on the ground, picked by
# how much room there is under the gap (ob-*), and more pieces for the piles hanging from the sky
for n in ('bush-meadow', 'apple-tree', 'fern', 'toadstool', 'pumpkins', 'scarecrow', 'snowman2', 'snowy-fir',
          'glow-mushrooms', 'night-shrub', 'spellbooks', 'cupcake', 'lollipop'):
    save(trim(load(n)), f'ob-{n}')
for n in ('cloud2', 'leaves-gold', 'cloud-rainbow', 'beehive', 'icicles', 'lanterns-hanging'):
    save(trim(load(n)), n)

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
