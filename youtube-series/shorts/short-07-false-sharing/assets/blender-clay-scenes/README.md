# Short 07 · False sharing · Numbered clay scenes

**Latest completed render:** [Revision 8](final-v8/README.md) uses the approved 2160 × 2300
clay composition, supplied safe-zone template, smaller inline-alignment code,
larger flowing clay pulses and faster resisted handoffs. Its source and new
exports live in `final-v8/`. All six new native clips and six matching previews
completed September 8, 2026 and passed export validation. The root MP4s
documented below remain revision 7.

Native Blender/Cycles scene package built from the September 7 canonical script,
after its numerical payoff was updated. Six independent silent scene clips are
the delivery format. No concatenated video is required to use them.

| Clip | Script scene | Source frames | Duration |
| --- | --- | --- | --- |
| [01-crowded-opening.mp4](01-crowded-opening.mp4) | Slower causal round trip | 1–192 | 8 s |
| [02-shared-cache-line.mp4](02-shared-cache-line.mp4) | Continued contention | 193–384 | 8 s |
| [03-write-ownership.mp4](03-write-ownership.mp4) | Continued ownership transfers | 385–576 | 8 s |
| [04-add-padding.mp4](04-add-padding.mp4) | Separate b inside the same struct | 577–720 | 6 s |
| [05-benchmark-result.mp4](05-benchmark-result.mp4) | Timings and 5.5× with continued updates | 721–816 | 4 s |
| [06-discussion-hold.mp4](06-discussion-hold.mp4) | Hold result text; counters keep updating | 817–1008 | 8 s |

These lengths provide readable, independently editable animation source. They
supersede the script's earlier shorter animation windows; they are not a new
narration-duration target. Each contention clip contains a four-second handoff
in each direction. Every file has zero-based playback timestamps and a complete
background. Scene 06 holds the result text while independent updates continue.
Native clips are 2360 × 2352 at 24 fps; matching previews are smaller copies.

## Current visual revision

Revision 7 follows the creator’s live feedback: turquoise-cyan (#008F88) joins cobalt and the orange ground, with no toon outlines. Flow paths are thick native clay; pulses
travel for one second and raised clay +1 bubbles rise for about 1.42 seconds. Visible numerals increment with a small pop and the counter presses. Ownership
colors the whole tray. The older gold-worker visual directions in the script
are superseded by this feedback; narration and measured numbers are unchanged.

All current production files, previews, intermediates and scene exports are
created directly in this Content HQ assets package. Earlier rejected revisions
are archived here. `_render/current/` contains native frame caches and `review/`
contains development motion checks; Revision 7 is complete. All six root MP4s and six numbered `previews/` viewing copies passed their export checks; `export-verification.json` records the dimensions, durations, frame counts, audio absence, zero start, full decode results and current file hashes. Previous exports are preserved in `archive/v6/`.

## Code and changed-line animation

A single native Menlo `struct Counters` appears in scenes 01–04, with syntax
colors and both atomic members enclosed by visible braces. During padding, the
same struct header and braces remain fixed while its member rows change to
`alignas(128) atomic<uint64_t> a{0};` and the equivalent declaration for b.
Staggered row transitions and mint underlines identify the new alignment.

This is a compact explanatory presentation of the benchmark layouts under one
struct name. The full benchmark uses Packed and Separated types, verifies initial
same-line placement, and checks actual cache-line boundaries. Headers, using
declarations and fixture alignment checks are omitted from the render. The
literal 128 is the test machine's measured cache-line size, not a universal
recommendation. Code clears for the result, which retains both times and 5.5×.

## Numerical source

The timing comparison is **244.52 ms → 44.19 ms**, both from benchmark run 04.
The script says **5.5 times faster in this test**. The result graphic keeps only
the two times, clean ivory arrow and **5.5× faster**. The measured multiple is essential result information.
See `../../benchmark-results.md` and `../../script.md` in the Content HQ package.
The script fingerprint used for the build is in `scene-manifest.json`.

## Animation semantics

- Turquoise-cyan (#008F88) identifies Core 0 / a; cobalt identifies Core 1 / b.
- The trays are schematic fixed cache-line address regions, not a model of one
  shared physical cache. Relative object widths are not byte measurements.
- A request pulse arrives before ownership color changes, and the tray moves only after that color change. Different counters initially occupy one region. The entire tray body, floor and rim change ownership color in bursts;
  a visible write follows the transfer, then its +1 bubble finishes independently of the next request.
- Padding is represented by an empty region as b moves into the second line.
  Relocation illustrates comparing layouts configured before timing; it does not
  depict safely relocating live atomic storage under active worker threads.
- Throughout all three contention scenes, the complete shared tray moves right and back left as a coherence-handoff metaphor; both members keep their relative offsets. a never changes address. Both trays keep identical geometry and scale. Counter
  tiles share their baseline meshes and scale; a 2% vertical press is a deliberate
  animation deformation tied to writes, not a change in counter storage size.
- Raised `+1` clay bubbles rise above each variable. Visible numerals count illustrative writes, not benchmark totals or a measured hardware trace. Letter labels stay visible. The two illustrative totals match when the benchmark result appears.
- No software lock, guaranteed strict alternation, perfect parallelism or core
  pinning is claimed. The schematic pulse rhythm is not a measured speed ratio.
- Scene 06 holds the result text while both separate counters keep updating. The final-totals experiment is not illustrated as
  completed, and no outcome for it is claimed.

## Appearance and placement

The approved native Short 06 materials, camera and studio lights supply the
Retro Sunset look. Native sculpted shells and duplicated tray assemblies replace
all image-generation pixels. The generated Short 07 concept is a look reference.

Timing center is y=590, retaining the additional 100 px downward correction from
the old y=490 result. A single common foreground root positions physical objects.
See `scene-verification.json` for actual bounds. The full gradient is continuous;
its warm highlight stays below the result text. This new scene honors the latest
clearance instruction; it does not retroactively change Short 06's old render.

These are lower-screen animation sources, not a finished 2160 × 3840 social
master. Real platform-interface clearance still needs checking in the complete
presenter/caption composite. Editorial captions, red pointers, narration and
sound are intentionally separate from these silent Blender scenes.

## Source and verification

- `false-sharing-clay.blend`: packed editable native scene, timeline markers.
- `build.py`: parameterized source path and work directory; no render unless
  `--preview` is supplied. Default source is the prior Content HQ native scene.
- `render_motion.py`: render unique native clay poses and full-scene numeral patches;
  `compose_model.py` combines the native images. `render.py` remains the conventional renderer.
- `finish.py`: encode six numbered clips and previews,
  export first/last stills, and fully decode-check every output.
- `verify_geometry.py`: checks shared mesh data, fixed member offsets during handoffs, fixed tray
  scales, counter scale limits, crossing clearance and result values.
- `scene-manifest.json`: source ranges, durations and source script fingerprint.
- `scene-verification.json`, `geometry-verification.json`,
  `cue-geometry-verification.json`, and
  `export-verification.json`: measured checks. The final revision report is written only after all six native clips and six previews pass frame-count, duration, dimensions, zero-start, audio absence and full decode verification.

Moving poses are authored on twos for tactile clay motion inside a 24 fps stream.
Only identical native clay poses reuse base frames. `native-padding-reuse-verification.json` records 41 unchanged padding poses reused from the previous native render after pose/material matching, glyph-coverage checks and a comparison against a fresh native crossing render (mean channel difference 0.045/255; 99th percentile 1/255). Existing numeral pixels in those bases are fully replaced by the current native patches. Changing numerals are rendered
with the full scene present as small native patches, including their face background,
lighting and occlusion. `native-composite-qa.json` compares against conventional
full native renders at a settled frame and a crossing frame (mean channel error
0.009 and 0.043 of 255; 99th-percentile error 0 and 1). There are no generated
in-between frames. The transparent result layer and native background are combined
above y=930; the model pass includes the complete lower studio region. The editable
scene can also render conventionally as a full frame.

Native export: H.264 CRF 16, yuv420p, BT.709, fast-start, no audio.
Previews: 1180 × 1176, Lanczos, CRF 18.
