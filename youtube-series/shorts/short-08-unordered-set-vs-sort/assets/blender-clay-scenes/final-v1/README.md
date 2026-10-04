# Short 08 — Sculpted clay animation

Status: STOPPED BY CREATOR. This revision is rejected and must not be resumed.
The review-only replacement is ../keyframes-v2/. Video approval is revoked.

The creator authorized production of the pitched seven scenes on September 16,
2026. Spoken words remain unchanged in the [canonical episode script](../../../script.md).
Use that current file rather than an old copied script.

## Native appearance and layout

Directly reuses Short 07 final-v9 meshes, sculpted materials, lights, camera and
Retro Sunset ground. The approved thumb-pressed shells, nonperiodic smears,
matte pigment and grazing studio light are actual native assets. New linked
tile, bucket and tray assemblies replace the previous episode's counters.

2160 × 2300, opaque and silent, 24 fps with poses held on twos. Place at (0,0)
in a 2160 × 3840 master; the lower 1540 pixels remain for the presenter.
Code uses native unlit Menlo at 96 units, consistently sized across both
viewports to include entrance motion within the safe guards. Result type and
the single-piece optically centered arrow retain the approved treatment.

No baked captions, callouts, red editorial annotations, titles, narration or
research-table banner. These silent scene assets are separate from final edit
caption/presenter layers described in the script.

## Scene files

| File | Frames | Seconds |
| --- | --- | ---: |
| 01-big-o-opening.mp4 | 1–72 | 3 |
| 02-speedup-tease.mp4 | 73–120 | 2 |
| 03-hash-insertions.mp4 | 121–288 | 7 |
| 04-sort-and-compact.mp4 | 289–408 | 5 |
| 05-benchmark-result.mp4 | 409–480 | 3 |
| 06-memory-layout.mp4 | 481–648 | 7 |
| 07-flat-table-tease.mp4 | 649–720 | 3 |

Seven self-contained native H.264 CRF16 files, each with a 1080 × 1150 CRF18
preview under previews/. No concatenated movie. Durations are editable visual
beat targets, not a timed recording of the creator's spoken script.

## Semantic invariants

- Original illustrative input 3,1,3,4,2 stays intact; the benchmark is 100M
  integers with 1% duplicates, not this pedagogical five-tile sample.
- Reserved standard unordered_set: a new 2 adds a node; repeated 3 does not.
- Copy before sort. Sorted order 1,2,3,3,4; unique retains 1,2,3,4.
- The logical-end divider does not shorten the allocated tray. Tail contents
  are not specified. Sequential contact after the result illustrates layout,
  not the whole sorting operation or a measured cache-miss trace.
- Sorting uses two readable lift/shift/land moves: 1 goes first, then 2. The duplicate
  clears before the surviving 4 slides into its slot.
- Supplied result 25.25 s → 2.61 s; 9.68× from the unrounded paired medians.
- Flat-table ending is an unmeasured next-test preview. Original timing labels
  stay with their methods; no result is assigned to the new flat table.

## Reproduction and verification

build.py loads the approved prior scene, constructs the new source and authors
native animation. It saves short-08-clay.blend without rendering. verify_scene.py
checks visible font bounds and builds exact-pose maps; check_motion.py checks
input/prefix invariants and conservative shell AABBs during sorting crossings.
render.py makes conventional full stills, proof.py places those beneath the
actual supplied platform guide on a full 4K master.

After production-preflight.json records a verified source hash and batch
approval, pipeline.py supervises produce.py with three resumable attempts.
CPU glyph passes are batched; moving clay uses native Metal/Cycles. Static
upper background reuse is checked against conventional native stills first.
All geometry/material/visibility/reveal state participates in cache mapping.
Typography is converted to mesh only in the render process, preserving native
editable FONTs in the packed source. No frame interpolation or native upscaling.

Every output is full-decoded and checked for native dimensions, fps, frame
count, duration, zero start, absence of audio and hash. Generated assets,
proofs, runtime reports, logs and caches stay in this directory and are ignored
by the project's existing Blender artifact rules. Sources and this README are
tracked candidates; no commit or push is implied.

## Batch preflight passed

All-frame text guards pass; unchanged input and final unique prefix verified;
sorting shell crossings have no conservative AABB overlap. Minimum clay
bound y=1217.11 leaves the static upper-background partition clear. Native
48-sample clay and layered composition were compared with a 96-sample native
reference; mean channel differences are below 0.45/255 with native-detail
and template inspection. Model 48 / typography 64 / background 128 samples.

Production started with resumable per-state rendering and automatic per-scene
encoding/validation. Check _render/pipeline-status.json for current state.
