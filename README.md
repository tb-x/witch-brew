# Witchy Brew

A friendly little witch flies her broom over meadows, forests and snowy hills, catching the
ingredients for a magic potion. At the end of each level she lands at her cottage, you drop
everything into the cauldron, stir it, and out of the potion jumps a new friend who rides the broom
with her from then on: a black cat, a frog with a crown, a pumpkin lantern, a snowy owl, a trail of
stars, and finally a rainbow and a unicorn.

It plays like Flappy Bird, but nothing can go wrong: bumping into a tree only makes her spin and
say "Oops!", and the level goes on until the potion is complete.

Everything you see is pixel art made with PixelLab, and everything you hear was made with
ElevenLabs: a friendly voice that tells you what to find and counts with you, sound effects, and
cheerful music. The witch and the cat are animated (she bobs and blinks on her broom; the cat
swishes its tail). The world is drawn on a small pixel canvas, 2 pixels to every game unit, and blown
up by whole pixels, so the bits drawn in code (sparkles, the potion, fire, fireworks, the rainbow)
match the pictures.

## How it plays

- Pick a level (the next one opens when you finish one). A voice says what to find: "Find two
  mushrooms and two blueberries!" The recipe is shown as pictures at the top of the screen.
- Tap anywhere (or press space) and the witch swoops up; let go and she glides gently down. If she
  touches the ground she just bounces back up.
- Fly into an ingredient to catch it: it flies up into the recipe and the voice counts it in a
  little sentence ("First snowflake!", "Second snowflake!"). Extra ones you don't need just sparkle.
- Trees, clouds and rocks stand in the way with wide gaps between them, and the witch is gently
  pulled towards the middle of the next gap. A bump makes her spin round, she drifts back, and for
  a moment she can fly straight through things.
- From level 3 a smelly sock or an old shoe floats about too. Catch one and she bats it away:
  "A smelly sock? No thanks!"
- Missed an ingredient? More keep coming until the recipe is complete. Then "That's everything!
  Fly home!" and she glides down to her cottage.
- At the cauldron: tap to throw the ingredients in one by one (the voice counts them again, "First
  snowflake!"), then stir by rubbing round and round on the screen (tapping works too; a finger
  circling the pot shows how). Five stars arch over the pot and light up one by one with a chime;
  when the last one lights, the potion is ready.
  Abracadabra! The level's friend jumps out of the pot, somersaults onto the broom ("A black cat!
  She wants to fly with you!"), and the end card shows 🗺️ (levels), 🔄 (again) and ▶️ (next level).
- The broom always carries every friend earned so far, on every level and on the title screen.

### The six levels

| Level | Where | Recipe | New friend | Also | New |
| --- | --- | --- | --- | --- | --- |
| 1 | sunny meadow: oak trees, fluffy clouds | 3 flowers | a black cat, behind her | flowers grow all over the meadow | learn to tap; slow, very wide gaps |
| 2 | forest: fir trees, hanging moss | 2 mushrooms, 2 blueberries | a frog with a crown, on the handle | | two kinds to collect |
| 3 | pumpkin patch at sunset: stacked hay bales, autumn branches, a red barn | 2 leaves, 2 apples, 1 feather | a pumpkin lantern, hanging from the handle | | three kinds; socks and shoes to avoid |
| 4 | snowy hills: snow-capped rock pillars, snow clouds with icicles | 3 snowflakes, 2 blueberries | a snowy owl, on her hat | snow falls | a little faster |
| 5 | starry night: fairy-tale towers, dark clouds, a village with lit windows | 3 stars, 1 moon, 2 water drops | a trail of stars from the broom | fireworks | dark sky |
| 6 | rainbow clouds: pink cloud piles, a flower field, a fairy castle | 2 stars, 2 flowers, 2 drops, 1 feather | a rainbow trail, and a unicorn flying alongside | a rainbow | four kinds, fastest |

## Running it

Serve the folder, e.g. `python -m http.server 5215`, and open http://localhost:5215.
Add `?all` to the address to open every level, and `?friends=6` to put all six friends on the broom
(for testing; `?friends=0` takes them all off). It fits phones and tablets either way round: the
short side of the screen always shows about the same amount of the world, so on a phone held upright
the sky is taller and you see less ahead. Opened straight from disk the pictures still show, but the
browser won't load the sounds, so the effects are made in the browser and the device's own voice talks.

## Tuning knobs

At the top of the script in `index.html`:

| Knob | What it does |
| --- | --- |
| `VIEW_MIN` | At least this many game units across the short side of the screen (smaller = bigger witch). Each picture pixel is a whole number of screen pixels, so the real view is a little bigger on some screens |
| `RES` | Picture pixels per game unit (the PixelLab pictures are made for 2) |
| `ASSET_V` | Bump after changing any picture or sound in `assets/`, so browsers fetch the new one |
| `WITCH_FPS` | Speed of the witch's flying animation (the cat's is three quarters of it) |
| `GRAVITY`, `FLAP`, `MAX_FALL` | How fast she drops, how high a tap lifts her, and her slowest-possible glide |
| `SPEED` | Flying speed (each level multiplies it by its `speed`) |
| `PILLAR_EVERY`, `PILLAR_W` | Distance between obstacles, and how wide they are |
| `MAX_SHIFT` | Most the gap moves up or down from one obstacle to the next |
| `ASSIST`, `ASSIST_RANGE` | The gentle pull towards the middle of the next gap (0 = off) and how far ahead it starts |
| `HIT_R`, `PICK_R` | How close she must get to bump something (small = forgiving), and to catch an ingredient (big = easy) |
| `OOPS_TIME`, `SAFE_TIME` | How long she spins after a bump, and how long she can then fly through things |
| `ITEM_CHANCE`, `DECOY_CHANCE` | How often an ingredient appears between obstacles, and how often a sock or shoe does instead |
| `STIR_NEEDED`, `STIR_TAP`, `STIR_STARS` | How much stirring finishes the potion, how much one tap counts, and how many stars light up on the way |
| `MAGIC_TIME` | How long the potion's magic plays before the end card |
| `SFX_VOL`, `VOICE_VOL`, `MUSIC_VOL` | Loudness of the effects, the voice (every line is evened out first) and the music |
| `MUSIC_DUCK`, `MUSIC_XFADE` | How far the music dips while the voice talks; seconds of the track's end blended into its start so it loops without a seam |
| `ING`, `DECOYS` | The ingredients (emoji, picture, words, potion colour) and the things to avoid |
| `FRIENDS` | The friend each level adds, its picture and where it sits on the broom (in pixels of the witch's picture) |
| `RIDER` | Where the witch's body is in her picture, and how high the broom is in each animation frame, so the friends bob with it |
| `LEVELS` | Per level: sky colours, recipe, `speed`, `gap` (height of the gaps), `decoys`, the extra `magic`, and `art`: its background strips (`far`, `near`, and `soil`, the colour under them) and its obstacles: a `cap` at the gap, a `body` stacked down to the ground (`bodyStep` makes it a wobbly pile), and a `top` piled up into the sky (`topStep` apart). The other colours are only used while the pictures load |
| `LINES` | Every spoken line (its clip is `assets/say-<key>.mp3`; the text is for the device's voice if the clip can't load) |

## The plan from here

1. **Play-test** with a five-year-old on a phone and tune `FLAP`, `GRAVITY`, `SPEED`, `gap` and
   `ASSIST` until it's easy and fun.
2. **Finish**: offline support (manifest, `sw.js`, icons), list it on the landing page, publish to
   `tb-x/witch-brew`.
3. Maybe: one shared palette (like Nut Run's `art-src/palette.py`) so all the pictures match even
   more closely.

## Credits

Pictures: made with [PixelLab](https://pixellab.ai). Voices and sounds: [elevenlabs.io](https://elevenlabs.io).
Music: Eleven Music. Sparkles, the potion, fire, fireworks and the rainbow are drawn in code.

### Picture credits

All made on 2026-10-18 with PixelLab (trial account, paid credits; PixelLab's terms let us use and
share them freely, with no attribution needed): every picture with `create_image_pixflux`, and the
two animations with `animate_image`. They were all made at twice the size of an earlier first try,
which is no longer in the game. The untouched originals are in `art-src/`; `python art-src/prep.py`
(run from this folder) cuts them out, crops and trims them into `assets/` (then bump `ASSET_V`).

- `assets/witch-fly.png`: the witch in a green dress and purple hat on a long broom, 8 frames of
  her flying (she bobs and blinks), side by side. Made from `art-src/witch-a.png` (one of two tries;
  `witch-b.png` isn't used) with `animate_image`; the frames are in `art-src/frames/`.
- Her friends: `assets/cat.png` (8 frames of the cat swishing its tail and blinking, also made with
  `animate_image`), `frog-crown.png`, `lantern.png`, `owl.png` and `unicorn.png` (mirrored by the
  script, as it faced left). The script shrinks them all to 65% (`FRIEND_SIZE`) so they don't crowd
  the witch, snapping every pixel back to the picture's own colours so they stay crisp.
- `assets/cottage.png`, `assets/cauldron.png`: the witch's cottage (the chimney smoke is drawn in
  code) and an empty cauldron (the potion inside, the fire under it and the spoon are drawn in code).
- Ingredients, `assets/ing-<name>.png`: flower, mushroom, berry (blueberries), leaf (maple), apple,
  feather, snow (snowflake), star, moon and drop (water drop); one picture each. The flower also
  grows all over the meadow at the end of level 1.
- Things to avoid: `assets/sock.png` and `shoe.png`.
- Level 1: `assets/bg-meadow-far.png` (distant hills) and `bg-meadow-near.png` (grass and flowers
  along the bottom), each shown next to its mirror image so it repeats without a seam;
  `crown-meadow.png` (the leaves cropped off a whole tree), `bark-oak.png` (stacked up each trunk)
  and `cloud.png` (piled up for the hanging obstacles, and small and see-through far away).
- Level 2: `bg-forest-far.png` (a fir forest) and `bg-forest-near.png` (ferns and mushrooms);
  `fir.png` (without its stump) on `bark-dark.png`, and `vines.png` (hanging moss).
- Level 3: `bg-autumn-far.png` (sunset fields with a red barn; its stripy sky stays, the sun is
  painted over with its band's colour, and the level's sky matches its top) and `bg-autumn-near.png`
  (a pumpkin patch); `hay-top.png` (a round hay bale with a pumpkin) on a wobbly pile of
  `hay-bale.png` (the same bale without the pumpkin, cut out by the script), and `leaves-autumn.png`.
- Level 4: `bg-snow-far.png` (snowy mountains) and `bg-snow-near.png`; `rock-top.png` (a snow-capped
  rock) on `rock.png` (a stone column), and `cloud-snow.png` (snow clouds with icicles).
- Level 5: `bg-night-far.png` (a valley village with lit windows; its starry sky stays) and
  `bg-night-near.png` (grass with glowing flowers; a second try, as the first came with a stripy sky
  that couldn't be cut out); `tower-roof.png` (the roof cut off a little tower) on `tower.png` (stone
  bricks with a lit window, a second try), and `cloud-night.png`. The extra stars and moon are drawn in code.
- Level 6: `bg-rainbow-far.png` (pastel cloud hills with a fairy castle; its sky stays) and
  `bg-rainbow-near.png` (the band of flowers along the bottom of its picture); `cloud-pink.png` piled
  up from the ground and down from the sky.
- PixelLab paints a sky behind most landscape strips even when asked not to; the script flood-fills
  it away from the top. Every near strip is cropped so its grass line is 80 pixels (40 game units)
  down, which the game lines up with the ground, and the colour under it (`soil`) fills the rest.

### Audio credits

All made on **2026-10-18** with the ElevenLabs **Starter** (paid) plan. Starter-plan audio may be
used commercially; we credit "elevenlabs.io" and "Eleven Music" anyway. No real person's voice was
used. The audio is here only as this game's own sounds: it is not licensed for anyone else to reuse,
and it is not covered by any licence that may later be put on this game's code.

- **Voice**, `assets/say-*.mp3`, 43 clips: stock voice "Jessica - Playful, Bright, Warm", model
  Eleven Multilingual v2, speed 0.85, stability 0.6 (the same voice and settings as Nut Run). The
  lines are in `LINES` in `index.html`: the six "Find …!" recipes, "Tap to fly!", the counting
  lines (`say-c-<ingredient>-<n>.mp3`: "First flower!", "Second flower!", "Third flower!" and so on for
  every ingredient, or "A feather!" and "A moon!" where a level only needs one), "Oops!", "Whoops!", "Bump!", the sock and shoe lines, "That's everything! Fly home!",
  "Tap to put them in the pot!", "Now stir! Round and round!", a line for each friend ("Abracadabra!
  A black cat! She wants to fly with you!" and so on) and "Hooray!".
- **Sound effects**, `assets/sfx-*.mp3`, 11 clips made with the ElevenLabs sound effects model, each
  from a short description: flap (a broom whoosh), pick (a sparkly chime), bump (a soft cartoon bonk),
  boing (bouncing off the ground), nope (the sock and shoe), splash (into the cauldron), bubble,
  poof (the potion is ready), pop (a firework), home (arriving at the cottage) and jump (a friend
  leaping out of the pot). Each has a stand-in made in the browser while it loads.
- **Music**, `assets/music.mp3`: one 60-second instrumental track made with Eleven Music (music_v2),
  "gentle, whimsical, magical … celesta, pizzicato strings, flute, glockenspiel …". The game loops it
  by blending its last 2 seconds into its start, and dips it while the voice talks.
