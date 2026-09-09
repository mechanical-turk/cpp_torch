# Short 07 — final clay revision 8

Native animation source and render destination for the creator-approved clay
look, 2160 × 2300 canvas, and supplied platform safe-zone template. The animation
sits at (0, 0) in the 2160 × 3840 master, with the recording region below.

Completed September 8, 2026 at 19:20 EDT. All six numbered native MP4s and six
matching previews are rendered and verified here. `export-verification.json`
records their successful checks and current hashes; `_render/pipeline-status.json`
records completion. Previous revision 7 clips remain in the parent package.
There is no combined viewing video.

| File | Duration | Action |
| --- | --- | --- |
| [01-crowded-opening.mp4](01-crowded-opening.mp4) | 6 s | Packed counters; ordered round-trip ownership handoff |
| [02-shared-cache-line.mp4](02-shared-cache-line.mp4) | 6 s | Continued writes to different counters inside one line |
| [03-write-ownership.mp4](03-write-ownership.mp4) | 6 s | Whole-line ownership changes and resisted tray transfers |
| [04-add-padding.mp4](04-add-padding.mp4) | 6 s | Inline alignment change and b moving to a second line |
| [05-benchmark-result.mp4](05-benchmark-result.mp4) | 4 s | 244.52 ms → 44.19 ms, then 5.5× faster |
| [06-discussion-hold.mp4](06-discussion-hold.mp4) | 8 s | Result remains; independent counters keep updating |

These are editable source durations. The creator controls narration timing and
the final cut. No captions, title cards, narration, sound, or code-return outro
are baked into the clips. Illustrative counter values are not benchmark totals.

## Composition and code

The actual 1080 × 1920 RGBA template is doubled over the full 4K master. Essential
text fits x=120–1872, y=440–2840; code/results have additional inner padding.
The complete native timeline is checked, including row entry, underlines,
ownership movement and rising +1 bubbles. Separate template proofs are saved
for review, never included in the MP4s.

The creator rejected `alignas(128)` on its own line. Both code layouts therefore
retain one four-row `struct Counters`; the two changed rows read
`alignas(128) atomic<uint64_t> a{0};` and the equivalent for b. Menlo is reduced
consistently from 150 to 100 font units to fit those complete declarations.
The syntax colors and sharp unlit glyph treatment remain. The header and braces
stay stable while member rows change with a staggered slide/unfold and brief
underlines beneath the inserted alignment expressions.

## Motion and native assets

The approved still supplies the original model geometry, clay material nodes,
studio lights, camera and foreground scale. Trays share canonical mesh data and
scale. A modest common horizontal reframe makes room for the second tray; it
does not depict a changing offset for a within its original line.

Each three-second handoff contains 20 frames of pulse travel, an ownership color
change at frame 24, and a resisted transfer from frame 30 through frame 48.
Anticipation, acceleration, banking, overshoot and settling convey weight. Two
illustrative writes follow each landing, avoiding the implication that every
increment necessarily causes a handoff. Every +1 bubble has its own 40-frame
lifetime and continues across scene boundaries. The final scene keeps updates
active rather than illustrating the proposed final-totals experiment as done.

The larger continuous clay packet consumes nearby dashes; adjoining pills swell
and release as it passes. Stable object-space texture and geometry are used.
All moving poses are native Blender renders authored on twos in a 24 fps stream.
No optical flow, synthesized frames or image-generation pixels are used.

## Render recovery and source

The initial Blender 5.1.2 GPU preview crashed in Metal shader compilation,
specifically `path_cache_get` with an invalid free. The process-local
`CYCLES_METAL_DISABLE_BINARY_ARCHIVES=1` workaround completed the retry previews.
It bypasses the path identified in the crash; it does not disable GPU rendering
or change global Blender preferences. The option is implemented in Blender's
[Metal kernel source](https://raw.githubusercontent.com/blender/blender/main/intern/cycles/device/metal/kernel.mm).

A separate animated FONT tessellation issue caused missing glyph fragments in
consecutive frames on both GPU and CPU. The renderer converts native font
outlines to meshes once per process, preserving transform animation; the saved
source retains editable native text. Identical packed-code states at frames 37
and 77 then rendered with identical pixels. Typography uses a separate native
CPU pass; clay models use Metal/Cycles. Persistent scene data is disabled.

Cached model bases exclude numerals through a non-animated child collection,
because Blender re-evaluates animated object hide flags at render time. Numeral
patches render with the complete scene present. The corrected blank-base
composition was checked against a full native frame: mean channel difference
0.178/255, 99th percentile 1/255. Base imagery was visually checked for absent
numerals before resuming the model batch.

The motion pass uses 32 Cycles samples and four ground ambient-occlusion samples,
matching the playbook's production settings. A native comparison against the
48-sample/16-AO reference gave mean channel difference 0.392/255 and 99th
percentile 3/255, with the clay detail retained on visual review. Completed full
frames from the higher-sample pass are retained; partial-pass caches were
invalidated when changing this profile. The text pass remains 64 samples and
the static upper background 128. `production-quality-comparison.json` records
the comparison.

`build.py` creates `false-sharing-final.blend` and audits placement. Run
`verify_motion.py` with Blender for row clearance and structural checks.
`render.py --preview` produces layered native proofs. `pipeline.py` supervises
the resumable production render and `finish.py` encodes/validates each scene.
All work, caches and logs stay under this episode asset directory; generated
artifacts are ignored by Git.

Native output is 2160 × 2300, 24 fps, silent H.264 CRF 16 with BT.709 metadata
and fast-start. Smaller editing previews are 1080 × 1150. Exports are checked
for dimensions, frame count, duration, zero start, absence of audio, and full
decode. Template clearance is separate from an actual posting-interface review.

Final review covered the ordered handoff, changing code, lifted crossing,
landing, benchmark reveal, and continued final activity. Encoded opening,
padding, benchmark and last-frame samples were visually inspected. The final
illustrative values are 11 / 11 with both +1 bubbles still active. All twelve
export hashes and the canonical script fingerprint match their reports.
