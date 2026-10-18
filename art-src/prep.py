"""Turn the PixelLab originals in art-src/ into the game's pictures in assets/.

Run from the game folder:  python art-src/prep.py
Then bump ASSET_V in index.html.
"""
from collections import deque
from pathlib import Path
from PIL import Image

SRC = Path(__file__).resolve().parent
OUT = SRC.parent / 'assets'
NEAR_SOLID = 40   # the near strips are cropped so their first solid row (the grass line) is this far down


def load(name):
    return Image.open(SRC / f'{name}.png').convert('RGBA')


def trim(im):
    return im.crop(im.getchannel('A').getbbox())


def rows(im):
    w, h = im.size
    a = im.getchannel('A').load()
    return [sum(1 for x in range(w) if a[x, y]) for y in range(h)]


def cut_sky(im, tol=14):
    """PixelLab paints a sky behind landscape strips. Flood-fill it away from the top row, stepping only
    to neighbours of a similar colour (so banded skies go too), then drop anything left floating
    (a sun, stray stars) that doesn't reach the bottom."""
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
    # keep only what is joined to the bottom row
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


def scale_rgb(im, k):
    out = im.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            px[x, y] = (min(255, int(r * k[0])), min(255, int(g * k[1])), min(255, int(b * k[2])), a)
    return out


def mean_rgb(im):
    n = s0 = s1 = s2 = 0
    for r, g, b, a in im.getdata():
        if a:
            n += 1; s0 += r; s1 += g; s2 += b
    return (s0 / n, s1 / n, s2 / n)


def bottom_colour(im):
    w, h = im.size
    y = max(y for y, n in enumerate(rows(im)) if n >= w * 0.9)
    return '#%02x%02x%02x' % tuple(int(c) for c in mean_rgb(im.crop((0, y - 3, w, y + 1))))


def save(im, name):
    OUT.mkdir(exist_ok=True)
    im.save(OUT / f'{name}.png', optimize=True)
    print(f'{name}.png', im.size)


# characters, props and ingredients
save(trim(load('witch-c')), 'witch')
save(trim(load('cottage')), 'cottage')
save(trim(load('cauldron')), 'cauldron')
for n in ('flower', 'mushroom', 'berry', 'leaf', 'apple', 'feather', 'snow', 'star', 'moon', 'drop'):
    save(trim(load(n)), f'ing-{n}')
for n in ('sock', 'shoe', 'frog', 'pumpkin', 'snowman', 'unicorn'):
    save(trim(load(n)), n)
save(trim(load('crown-gold')), 'gold-crown')

# obstacles: a cap at the gap, a body stacked down to the ground, and a pile hanging from the sky
save(trim(load('crown').crop((0, 0, 80, 45))), 'crown-meadow')       # leaves only, off a whole tree
save(load('bark').crop((5, 0, 29, 128)), 'bark-oak')
save(trim(load('cloud')), 'cloud')
save(trim(load('crown-forest').crop((0, 0, 64, 55))), 'fir')          # without the patch of earth
save(trim(load('bark-dark').crop((0, 0, 32, 116))), 'bark-dark')      # without the roots
save(trim(load('leaves-forest')), 'vines')
save(trim(load('hay-top')), 'hay-top')
save(trim(load('hay-top').crop((0, 17, 48, 43))), 'hay-bale')        # the bale without its pumpkin
save(trim(load('leaves-autumn')), 'leaves-autumn')
rock_top = trim(load('rock-top').crop((0, 0, 48, 41)))                # without the snow at its foot
save(rock_top, 'rock-top')
rock = load('rock')
want, have = mean_rgb(rock_top.crop((0, rock_top.height // 2, rock_top.width, rock_top.height))), mean_rgb(rock)
save(scale_rgb(rock, [w / h for w, h in zip(want, have)]), 'rock')  # matched to the snowy top's darker grey
save(trim(load('cloud-snow')), 'cloud-snow')
save(trim(load('tower-top').crop((0, 0, 48, 29))), 'tower-roof')      # the roof off a little tower
save(trim(load('tower').crop((0, 0, 32, 87))), 'tower')
save(trim(load('cloud-night')), 'cloud-night')
save(trim(load('cloud-pink')), 'cloud-pink')

# background strips: far hills (sky cut away) and the ground along the bottom
for lvl in ('meadow', 'forest', 'autumn', 'snow', 'night'):
    far = 'hills-far' if lvl == 'meadow' else f'hills-{lvl}-far'
    nr = 'hills-near' if lvl == 'meadow' else f'hills-{lvl}-near'
    if lvl == 'autumn':
        # its banded sunset sky is too stripy to cut out, so it stays (the level's sky matches its top row);
        # the sun is painted over with its band's colour, or the mirrored repeat would show two suns
        im = load(far)
        px = im.load()
        for y in range(60):
            for x in range(im.width):
                if min(px[x, y][:3]) > 225:
                    px[x, y] = px[0, y]
        save(im, f'bg-{lvl}-far')
        print('   autumn sky top', '#%02x%02x%02x' % px[0, 0][:3])
    else:
        save(trim(cut_sky(load(far))), f'bg-{lvl}-far')
    strip = near(load(nr))
    save(strip, f'bg-{lvl}-near')
    print('   ground colour', bottom_colour(strip))
# the rainbow hills are clouds on a pastel sky: keep their sky (the level's sky matches its top row)
rb = load('hills-rainbow-far')
save(rb, 'bg-rainbow-far')
print('   rainbow sky top', '#%02x%02x%02x' % rb.getpixel((0, 0))[:3], 'bottom', '#%02x%02x%02x' % rb.getpixel((0, 119))[:3])
# the rainbow ground has a hole in the middle: use its left part (the game mirrors it)
save(near(load('hills-rainbow-near').crop((0, 0, 172, 80)), solid=72), 'bg-rainbow-near')
