# Short 06: lower placement and animated code/results

The canvas remains **2360 × 2352**. A camera shift moves the existing content
down exactly **200 pixels**, preserving model size, lighting and animation.
The original gradient continues above the composition.

Changed code lines now slide and flip into place in a stagger at approximately
6.6–8.1 seconds. Brief mint underlines mark the changed declarations and lookup,
then disappear. Syntax highlighting remains, and unchanged lines stay still.

The result uses bold coral and mint numbers with smaller units. The arrow and
both values share an optical center at y = 510 pixels. The arrow draws across,
a mint accent travels along it, the faster value settles into place, and the
ratio rises in. The result contains only `4.36 ms`, `0.35 ms` and `12.5× faster`.
There are no new captions, banners, narration or sound.

## Files

- `cpp-data-layout-motion.mp4`: native 2360 × 2352, 24 fps, 19 seconds, silent.
- `preview.mp4`: 1180 × 1176 viewing copy.
- `cpp-data-layout-motion.blend`: editable complete scene with packed fonts.
- `stills/`: opening, code transition, settled code, arrow draw, result and final hold.
- `scene-verification.json`: all-frame foreground bounds, alignment and frame mapping.
- `export-verification.json`: video metadata, decoding and rendering comparisons.
- `revise_scene.py`, `render_upper.py`, `finish.py`: reproduction scripts.

All foreground fits between approximately y = 391 and y = 2102. This verifies
the requested pixel placement; the final Reel composer has not been inspected.
All three scores and all 45 history plates remain. No benchmark was rerun.

## Rendering

The changed upper 1100 pixels are rendered natively in Blender. The unchanged
lower models reuse the previous native frames, translated exactly 200 pixels
without resizing. Their appearance is checked against full-scene reference
renders. This preserves model pixels while avoiding redundant 3D rendering.
Identical full-scene states reuse frames; moving frames are not interpolated.
The saved Blender file also supports a conventional complete-frame rerender.
The reproduction scripts refer to the existing native source frame cache in
the local workspace. Earlier clean and wide versions remain preserved.
