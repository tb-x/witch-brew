# Witchy Brew

A friendly little witch flies her broom over meadows, forests and snowy hills, catching the
ingredients for a magic potion. At the end of each level she lands at her cottage, you drop
everything into the cauldron, stir it, and the potion does something magic.

It plays like Flappy Bird, but nothing can go wrong: bumping into a tree only makes her spin and
say "Oops!", and the level goes on until the potion is complete.

**This is the grey-box prototype**: everything is drawn with simple shapes and emoji so the flying
can be tried out on a phone before any pixel art is made. The PixelLab pictures come next (see the
plan below).

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
| 1 | sunny meadow | 3 flowers | flowers grow all over the meadow | learn to tap; slow, very wide gaps |
| 2 | forest | 2 mushrooms, 2 blueberries | a frog gets a crown | two kinds to collect |
| 3 | pumpkin patch at sunset | 2 leaves, 2 apples, 1 feather | the pumpkin grows huge | three kinds; socks and shoes to avoid |
| 4 | snowy hills | 3 snowflakes, 2 blueberries | the snowman dances, snow falls | a little faster |
| 5 | starry night | 3 stars, 1 moon, 2 water drops | fireworks | dark sky |
| 6 | rainbow clouds | 2 stars, 2 flowers, 2 drops, 1 feather | a rainbow and a unicorn | four kinds, fastest |

## Running it

Serve the folder, e.g. `python -m http.server 5215`, and open http://localhost:5215.
Add `?all` to the address to open every level (for testing). It fits phones and tablets either way
round: the short side of the screen always shows the same amount of the world, so on a phone held
upright the sky is taller and you see less ahead.

## Tuning knobs

At the top of the script in `index.html`:

| Knob | What it does |
| --- | --- |
| `VIEW_MIN` | Game units across the short side of the screen (smaller = bigger witch) |
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
| `ING`, `DECOYS` | The ingredients (picture, words for the voice, potion colour) and the things to avoid |
| `LEVELS` | Per level: colours, recipe, `speed`, `gap` (height of the gaps), `decoys`, and the magic |

## The plan from here

1. **Grey box** (this): try the flying with a five-year-old on a phone and tune `FLAP`, `GRAVITY`,
   `SPEED`, `gap` and `ASSIST` until it's easy and fun.
2. **Pixel art with PixelLab** (ask before each batch, with the cost):
   - The witch on her broom, seen from the side (`create_character`), with flying, swoop (tap),
     dizzy (bump) and happy animations, plus standing-and-stirring for the cauldron.
   - The ingredients and the sock and shoe: one small `create_image_pixflux` picture each.
   - The obstacles for each level (tree trunks with crowns, hanging branches, clouds, rocks and
     icicles, mushrooms) and the cottage, cauldron, frog, pumpkin and snowman.
   - Parallax background strips per level, cut out and mirrored like Nut Run's, and one shared
     palette (Nut Run's `art-src/palette.py`) so everything matches the witch.
3. **Sound**: synthesized effects and speech for now. Recorded ElevenLabs lines (counting, "Find
   three flowers!") or Eleven Music only if asked for.
4. **Finish**: offline support (manifest, `sw.js`, icons), list it on the landing page, publish to
   `tb-x/witch-brew`.

## Credits

Everything is drawn in code for now (the ingredients are emoji); the sounds and the voice are made
by the browser.
