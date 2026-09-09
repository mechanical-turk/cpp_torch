# Short 06: wider clean animation

Regenerated at **2360 × 2352**, with exactly **100 extra pixels on each side**.
The original content keeps its pixel size and vertical position. The original
Blender stage, lighting and materials extend the background gradient naturally.
All code, labels, objects, animation, timing and colors are retained.

- `cpp-data-layout-clean-wide.mp4`: native video, 24 fps, 456 frames, 19 seconds, silent.
- `preview.mp4`: half-size 1180 × 1176 viewing copy.
- `cpp-data-layout-clean-wide.blend`: editable widened Blender scene with packed fonts.
- `stills/`: six native frames and the animation render manifest.
- `camera-verification.json`: checks that scene points shift right exactly 100 pixels with no resizing.
- `export-verification.json`: video dimensions, duration, decoding and crop comparisons.
- `widen_scene.py`, `render_animation.py`, `finish.py`: reproduction scripts.

To preserve the previous alignment in a 2160-pixel-wide composition, place this
asset at x = -100 rather than scaling it to fit. Height and vertical placement
remain unchanged. The wider asset is a requested derivative, not a change to
the series master resolution standard.

The original clean version remains in `../blender-clean/`. Every moving
frame is rendered natively; only verified static holds reuse frames. No new
benchmark was run, and the recorded 12.5× result still refers to the existing
ordered score-only lookup experiment.
