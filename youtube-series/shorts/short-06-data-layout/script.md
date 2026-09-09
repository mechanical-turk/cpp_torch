# Short 06: This struct wrecks performance

Canonical spoken script, synchronized to the simplified Blender animation.
Updated September 5, 2026. This supersedes the rejected Round 10 script;
the earlier [iteration record](iterations-2026-09-05/README.md) remains at 9/20.

Animation: [cpp-data-layout-clean.mp4](assets/blender-clean/cpp-data-layout-clean.mp4)
at 24 fps, exactly 19.000 seconds. [Editable scene](assets/blender-clean/cpp-data-layout-clean.blend).
Working composite filename: `cpp-data-layout-related-fields-performance-short-06.mp4`.
The presenter-and-voice composite has not yet been recorded or timed.

## Creative decision

- **Claim and position:** this player-record layout hurts the score-only loop;
  pull the scores into their own array.
- **Challenged belief:** a player's related fields should sit together in memory.
- **Reaction:** surprise and the urge to defend a familiar, readable struct.
- **Expected objection:** "That's a normal player struct. What if you need
  the histories too?" The ending makes that tradeoff the next experiment.
- **Intentional omissions:** cache internals, AoS/SoA terminology, compiler
  discussion, and whole-application design advice. The displayed SplitPlayers
  is still a struct; the target is field placement for this loop.
- **Evidence:** the existing ordered-ID lookup comparison, with the same data,
  IDs, order, additions, and result. Full conditions are retained below.

## Script and animation cues

### 0.00-1.40 | The opening

> This pattern destroys performance.

Start speaking immediately. Point toward the visible Player definition and
assembled records. The histories lift slightly in the existing opening.
Hit **struct** and **wrecks**; flow straight into the next sentence.

### 1.40-6.92 | The spacing

> We only need the scores. Look how far apart they are.

Point to the labeled score faces, then spread your hands across their spacing.
All three records receive the same treatment. No query-subset highlights or
new annotations are needed.

### 6.92-10.04 | The extraction

> Pull the scores out. Pack them together.

Lift your hand as all three score blocks rise, then bring your hands together
as they gather. The code changes to SplitPlayers and `scores[id]` at 6.92 s.
Land **together** as the blocks settle near 10 s.

### 10.04-12.00 | The retained data

> The histories stay here.

Point to the separate history row. Every history remains visible.

### 12.00-15.00 | The payoff

> The same lookups ran over twelve times faster.

The render shows `4.36 ms` to `0.35 ms` and `12.5x faster` together at 12 s.
Point toward the lower time. Deliver the result directly; there is no further
reveal to delay and no need to speak both decimal timings.

### 15.00-19.00 | The next experiment

> Need the histories too? That's what I'm testing next.

The timing text disappears and the split-array code returns at 15 s.
Gesture toward the histories and scores. The animation holds all fields
without selective outlines. Cut immediately after **next**.

## Recording and composition

- Use the existing clean render: syntax-highlighted code, labeled models,
  and the minimal numerical result. Preserve the creator's explicit removal
  of titles, captions, banners, callouts, selection highlights, and render audio.
- Record the presenter and spoken delivery separately. Place the opaque
  2160 x 2352 animation at x=0, y=1488 in the 2160 x 3840 composition.
- These speech boundaries are recording cues. The animation's extraction,
  result, and final hold begin at frames 167, 289, and 361 respectively.
  Record against those transitions; verify the actual combined export is
  strictly below 20 seconds. Do not append silence or an end card after the read.

## Evidence retained outside the render

[Recorded benchmark](../../../aliases/01-screen-short-form/data-layout/LOOKUP-RESULTS.md):
1,048,576 ordered active IDs among 4,194,304 players; repeat medians
4.355233 ms and 0.347342 ms, a 12.54x ratio. Both kernels are scalar under
normal -O3. Allocation, conversion, sorting, and validation are outside timing.
Histories remain stored. The animation and narration refer to this measured
score-only workload, not every layout, lookup order, or whole application.

The shapes are schematic. Three scores and all 45 history plates are retained;
their uniform presentation illustrates field placement, not the actual query
subset. Setup and the `scores` binding are outside the code viewport.
No hardware counters isolate cache misses, and the score-plus-complete-history
lookup for the same selected IDs has not been measured. That is the proposed
next test, not a known result or release commitment.

The [previous canonical script](script-before-blender-sync-2026-09-05.md) is
preserved. Animation and benchmark files were not changed by this script update.
Platform copy and the final combined-video review remain separate tasks.
