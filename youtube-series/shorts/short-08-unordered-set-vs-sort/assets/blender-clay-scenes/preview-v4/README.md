# Short 08 — source-only contour previews

216×230 / 24 fps / silent, rendered directly at 10% dimensions.

Thin 10-native-pixel white strokes follow the projected rounded clay shell
contour with zero padding. No bounding-box frames or destination highlights.
At most one input/working-array source is highlighted at a time. Code, clay,
choreography, data, timings and the bucket-well redesign otherwise stay intact.

Clips 01, 03, 04 and 06 are rerendered. Unchanged clips 02, 05 and 07 are
byte-identical copies from preview-v3, recorded in preview-verification.json.
No full-resolution render or image-review loop. Previous packages preserved.

build.py loads preview-v3, removes its two selection frames and projects the
evaluated canonical shell's outer contour for each active source pose.
audit.py checks text and geometry; highlight-verification.json records sources
and the one-highlight limit. render_preview.py delivers seven numbered previews.
