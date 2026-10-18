# Witchy Brew

A friendly little witch flies her broom over meadows, forests and snowy hills, catching the
ingredients for a magic potion. At the end of each level she lands at her cottage, you drop
everything into the cauldron, stir it, and the potion does something magic.

It plays like Flappy Bird, but nothing can go wrong: bumping into a tree only makes her spin and
say "Oops!", and the level goes on until the potion is complete.

Everything you see is pixel art made with PixelLab: the witch (with her black cat), every
ingredient, the trees, rocks, towers and clouds in the way, the hills and ground of each level, and
the cottage, cauldron and the creatures the potions change. The world is drawn on a small pixel
canvas and blown up by whole pixels, so the bits drawn in code (sparkles, the potion, the fire,
fireworks and the rainbow) look pixelated too and match the pictures.

## How it plays

- Pick a level (the next one opens when you finish one). A voice says what to find: "Find two
  mushrooms and two blueberries!" The recipe is shown as pictures at the top of the screen.
- Tap anywhere (or press space) and the witch swoops up; let go and she glides gently down. If she
  touches the ground she just bounces back up.
- Fly into an ingredient to catch it: it flies up into the recipe and the voice counts ("One!",
  "Two!"). Extra ones you don't need just sparkle.
- Trees, clouds and rocks stand in the way with wide gaps between them, and the witch is gently
  pulled towards the middle of the next gap. A bump makes her spin round, she drifts back, and for
  a moment she can fly straight through things.
- From level 3 a smelly sock or an old shoe floats about too. Catch one and she bats it away:
  "A smelly sock? No thanks!"
- Missed an ingredient? More keep coming until the recipe is complete. Then "That's everything!
  Fly home!" and she glides down to her cottage.
- At the cauldron: tap to throw the ingredients in one by one (the voice counts them), then stir
  by rubbing round and round on the screen (tapping works too) until the bar is full.
  Abracadabra! The potion does its magic, then the end card shows 🗺️ (levels), 🔄 (again) and
  ▶️ (next level).

### The six levels

| Level | Where | Recipe | Magic | New |
| --- | --- | --- | --- | --- |
| 1 | sunny meadow: oak trees, fluffy clouds | 3 flowers | flowers grow all over the meadow | learn to tap; slow, very wide gaps |
| 2 | forest: fir trees, hanging moss | 2 mushrooms, 2 blueberries | a frog gets a crown | two kinds to collect |
| 3 | pumpkin patch at sunset: stacked hay bales, autumn branches, a red barn | 2 leaves, 2 apples, 1 feather | the pumpkin grows huge | three kinds; socks and shoes to avoid |
| 4 | snowy hills: snow-capped rock pillars, snow clouds with icicles | 3 snowflakes, 2 blueberries | the snowman dances, snow falls | a little faster |
| 5 | starry night: fairy-tale towers, dark clouds, a village with lit windows | 3 stars, 1 moon, 2 water drops | fireworks | dark sky |
| 6 | rainbow clouds: pink cloud piles, a flower field, a fairy castle | 2 stars, 2 flowers, 2 drops, 1 feather | a rainbow and a unicorn | four kinds, fastest |

## Running it

Serve the folder, e.g. `python -m http.server 5215`, and open http://localhost:5215.
Add `?all` to the address to open every level (for testing). It fits phones and tablets either way
round: the short side of the screen always shows the same amount of the world, so on a phone held
upright the sky is taller and you see less ahead.

## Tuning knobs

At the top of the script in `index.html`:

| Knob | What it does |
| --- | --- |
| `VIEW_MIN` | At least this many game pixels across the short side of the screen (smaller = bigger witch). Each game pixel is a whole number of screen pixels, so the real view is a little bigger on some screens |
| `ASSET_V` | Bump after changing any picture in `assets/`, so browsers fetch the new one |
| `GRAVITY`, `FLAP`, `MAX_FALL` | How fast she drops, how high a tap lifts her, and her slowest-possible glide |
| `SPEED` | Flying speed (each level multiplies it by its `speed`) |
| `PILLAR_EVERY`, `PILLAR_W` | Distance between obstacles, and how wide they are |
| `MAX_SHIFT` | Most the gap moves up or down from one obstacle to the next |
| `ASSIST`, `ASSIST_RANGE` | The gentle pull towards the middle of the next gap (0 = off) and how far ahead it starts |
| `HIT_R`, `PICK_R` | How close she must get to bump something (small = forgiving), and to catch an ingredient (big = easy) |
| `OOPS_TIME`, `SAFE_TIME` | How long she spins after a bump, and how long she can then fly through things |
| `ITEM_CHANCE`, `DECOY_CHANCE` | How often an ingredient appears between obstacles, and how often a sock or shoe does instead |
| `STIR_NEEDED`, `STIR_TAP` | How much stirring finishes the potion, and how much one tap counts |
| `MAGIC_TIME` | How long the potion's magic plays before the end card |
| `ING`, `DECOYS` | The ingredients (emoji, PixelLab picture if there is one, words for the voice, potion colour) and the things to avoid |
| `LEVELS` | Per level: sky colours, recipe, `speed`, `gap` (height of the gaps), `decoys`, the magic, and `art`: its background strips (`far`, `near`, and `soil`, the colour under them) and its obstacles: a `cap` at the gap (`capScale` times bigger), a `body` stacked down to the ground (`bodyStep` makes it a wobbly pile), and a `top` piled up into the sky (`topStep` apart). The other colours are only used while the pictures load |

## The plan from here

1. **Grey box**: try the flying with a five-year-old on a phone and tune `FLAP`, `GRAVITY`,
   `SPEED`, `gap` and `ASSIST` until it's easy and fun.
2. **Pixel art with PixelLab** (ask before each batch, with the cost):
   - Done (2026-10-18, about $0.35 of credits for 50 pictures): everything in the game.
   - Maybe: a flying animation for the witch (cape and hair fluttering), and one shared palette
     (like Nut Run's `art-src/palette.py`) so all the pictures match even more closely.
3. **Sound**: synthesized effects and speech for now. Recorded ElevenLabs lines (counting, "Find
   three flowers!") or Eleven Music only if asked for.
4. **Finish**: offline support (manifest, `sw.js`, icons), list it on the landing page, publish to
   `tb-x/witch-brew`.

## Credits

Pictures: made with [PixelLab](https://pixellab.ai) (listed below). Sparkles, the potion, fire,
fireworks and the rainbow are drawn in code; the recipe and level buttons use emoji until their
pictures load. The sounds and the voice are made by the browser.

### Picture credits

All made on 2026-10-18 with PixelLab's `create_image_pixflux` (trial account, paid credits; PixelLab's
terms let us use and share them freely, with no attribution needed). The untouched originals are in
`art-src/`; `python art-src/prep.py` (run from this folder) cuts them out and trims them into
`assets/` (then bump `ASSET_V`).

- `assets/witch.png`: a little witch in a green dress with a black cat, flying a broom to the right
  (one of three tries; the other two, `art-src/witch-a.png` and `witch-b.png`, aren't used).
  The game tilts her with how she's flying and spins her when she bumps into something.
- `assets/cottage.png`, `assets/cauldron.png`: the witch's cottage (the chimney smoke is drawn in
  code) and an empty cauldron (the potion inside, the fire under it and the spoon are drawn in code).
- Ingredients, `assets/ing-<name>.png`: flower, mushroom, berry (blueberries), leaf (maple), apple,
  feather, snow (snowflake), star, moon and drop (water drop); one picture each. The flower also
  grows all over the meadow for level 1's magic.
- Things to avoid: `assets/sock.png` and `shoe.png`.
- The potions' magic: `assets/frog.png` and `gold-crown.png` (level 2), `pumpkin.png` (level 3,
  doubles in size), `snowman.png` (level 4, dances) and `unicorn.png` (level 6, flies under the
  rainbow).
- Level 1: `assets/bg-meadow-far.png` (distant hills; PixelLab painted a sky behind them, which the
  script cuts out) and `bg-meadow-near.png` (the grass and flowers along the bottom), each shown next
  to its mirror image so it repeats without a seam; `crown-meadow.png` (cropped off a whole tree),
  `bark-oak.png` (stacked up each trunk) and `cloud.png` (piled up for the hanging obstacles, and
  small and see-through far away on every daytime level).
- Level 2: `bg-forest-far.png` (a misty fir forest) and `bg-forest-near.png` (ferns and moss);
  `fir.png` (a whole fir with the patch of earth under it cropped off) on `bark-dark.png`, and
  `vines.png` (hanging moss) piled down from the sky.
- Level 3: `bg-autumn-far.png` (sunset hills with a red barn: its stripy sky was too hard to cut out,
  so it stays, the sun is painted over with its band's colour, and the level's sky matches its top)
  and `bg-autumn-near.png` (a pumpkin patch); `hay-top.png` (a round hay bale with a pumpkin) on a
  wobbly pile of `hay-bale.png` (the same bale without the pumpkin, cut out by the script), and
  `leaves-autumn.png` (autumn branches) hanging down.
- Level 4: `bg-snow-far.png` (snowy mountains) and `bg-snow-near.png`; `rock-top.png` (a snow-capped
  rock) on `rock.png` (a stone column, darkened by the script to match), and `cloud-snow.png` (snow
  clouds with icicles).
- Level 5: `bg-night-far.png` (a hill village with lit windows) and `bg-night-near.png` (night grass
  with fireflies); `tower-roof.png` (the roof cut off a little tower, shown twice its size) on
  `tower.png` (a stone tower with a lit window), and `cloud-night.png`. The stars and moon are
  drawn in code.
- Level 6: `bg-rainbow-far.png` (pastel cloud hills with a fairy castle; its sky stays, and the
  level's sky matches it) and `bg-rainbow-near.png` (a flower field in the clouds: the left part of a
  strip that had a hole in the middle, mirrored by the game); `cloud-pink.png` piled up from the
  ground and down from the sky.
- Every near strip is cropped so its grass line is 40 rows down, which the game lines up with the
  ground, and the colour under it (`soil`) fills the rest of the screen.
