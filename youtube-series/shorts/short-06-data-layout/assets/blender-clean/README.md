# Short 06: simplified Blender animation

This revision replaces the earlier presentation-heavy render. It contains
syntax-highlighted C++, physical `score` and `history` labels, score values,
and a minimal result: **4.36 ms → 0.35 ms**, **12.5x faster**.

There are no titles, captions, banners, narration, sound, selection outlines,
query-subset highlights, or explanatory metadata in the video. All three
players receive the same visual treatment. Models are larger and occupy more
of the vertical composition. White score text sits on dark matte navy insets
whose color does not change under the stage lights.

## Files

- `cpp-data-layout-clean.blend`: editable Blender 5.1.2 scene, packed fonts,
  named model parents, syntax materials, and timing markers.
- `cpp-data-layout-clean.mp4`: silent native 2160 x 2352 animation, 24 fps,
  exactly 19 seconds.
- `preview.mp4`: smaller 720 x 784 viewing copy.
- `stills/`: native key frames and the render manifest.
- `storyboard.jpg`: overview of the revised composition.
- `build_scene.py`, `render_animation.py`, `audit_scene.py`: source and checks.
- `scene-audit.json`, `export-verification.json`: recorded validation.

Place the lower-screen animation at x=0, y=1488 in the existing 2160 x 3840
composition. The upper 2160 x 1488 area remains the presenter region.

## Timing

- 0–6.92 s: player records and their score-only lookup.
- 6.92–10.04 s: scores lift, gather, and settle; histories remain stored.
- 10.04–12 s: split arrays and updated lookup.
- 12–15 s: only the two measured timings and speedup, above the models.
- 15–19 s: return to the split-array code and hold the model composition.

## Evidence retained outside the render

The comparison is the existing ordered active-ID score lookup: 1,048,576 IDs
among 4,194,304 players, with medians of 4.355233 and 0.347342 milliseconds.
Both compiled kernels are scalar under normal -O3. Allocation, layout
conversion, sorting, and validation are outside the timing. See
`/Users/keremkazan/code/data-layout/LOOKUP-RESULTS.md` for the recorded protocol.
The approximately 12.5x ratio is specific to that workload, not a general
application speedup. No new benchmark was run for this animation revision.

Three schematic players retain scores 7, 2, and 9 and all fifteen history
plates each. Every score moves and every history remains. The geometry is
schematic rather than a literal byte scale. Uniform presentation of all three
objects illustrates field layout; it does not change the benchmark's query set.
No winner is implied for a future score-plus-history experiment.

## Rendering

Built with EEVEE at 32 samples. Every moving frame is rendered at native
resolution. Identical static holds reuse verified identical scene states.
There is no frame interpolation or upscaling in the native export.

```sh
blender -b --python build_scene.py -- --out /absolute/output/directory
blender -b /absolute/output/directory/cpp-data-layout-clean.blend \
  --python render_animation.py -- --frames /absolute/work/frames \
  --stills /absolute/output/directory/stills
```

The builder uses macOS Arial and Menlo paths; the saved blend packs the fonts.
Retiming an animation requires revising the static-hold mapping or rendering
all frames directly in Blender.
