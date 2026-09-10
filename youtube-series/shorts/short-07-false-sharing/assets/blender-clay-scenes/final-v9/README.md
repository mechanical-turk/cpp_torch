# Short 07 — sculpted clay revision 9

The creator approved the hand-sculpted `extreme-clay-study-v2` aesthetic for the
entire animation on September 9, 2026. This package applies its actual rolled
rims, broad thumb presses, softened folds, nonperiodic clay shaders and studio
lighting to the complete approved revision-8 timeline.

**Rendered and verified 2026-09-09 19:28:13 EDT.** All six native videos and six previews are complete. `_render/pipeline-status.json` records the current
render state. Only files listed with successful checks in
`export-verification.json` are completed exports.

| Numbered scene | Duration | Action |
| --- | --- | --- |
| `01-crowded-opening.mp4` | 6 s | Packed counters and round-trip ownership handoff |
| `02-shared-cache-line.mp4` | 6 s | Continued independent writes within one line |
| `03-write-ownership.mp4` | 6 s | Whole-line color changes and weighted tray transfers |
| `04-add-padding.mp4` | 6 s | Inline `alignas(128)` and b crossing into a second line |
| `05-benchmark-result.mp4` | 4 s | 244.52 ms → 44.19 ms; 5.5× faster |
| `06-discussion-hold.mp4` | 8 s | Result remains while separate updates continue |

Native assets: **2160 × 2300**, 24 fps, opaque, silent H.264 CRF 16, BT.709.
Place at **(0, 0)** in a **2160 × 3840** vertical master; recording goes below.
Matching 1080 × 1150 previews are in `previews/`. Each scene is a separate file;
there is no combined video. Source durations remain editable by the creator.

## Preserved explanation and composition

The four-row struct, inline alignment, syntax colors, code size, gradient
placement, measured result and all choreography retain revision 8's values.
The request arrives before ownership changes, then the shared tray transfers
with anticipation, acceleration, bank, overshoot and settle. Contention
continues through the first three scenes. Padding ends the handoff. Enlarged
packets consume and release neighboring clay dashes. Each +1 has its own
40-frame rise; numeral changes and counter compression continue after padding
and through the final result hold. Poses remain authored on twos, with no
synthesized in-betweens. Counts are illustrative, not benchmark measurements.

## Sculpted treatment and native checks

One canonical sculpted shell serves the two counters and cores; both trays
share another shell; all dashes share their pinched pill master. Repeated
geometry and modifiers stay identical. Physical lettering gains soft bevels
and shallow raised depth. Native code and result outlines remain unchanged.

Both pigment-ramp endpoints follow the original ownership color animation.
This prevents the new procedural shader from masking the tray's color changes.
The ground retains its continuous Retro Sunset gradient. There are no radial
fingerprint shaders. Clay detail is anchored in local/object coordinates.

`build.py` loads the approved revision-8 animation, applies the approved native
sculpture and materials, retains animation and saves `false-sharing-final.blend`.
It audits all 864 frames. `verify_motion.py` checks layout and semantic offsets.
The first audit reports zero violations, minimum code/core gap 66.95 px and
minimum code-row gap 50.80 px. Essential text is checked against the supplied
platform template; outer geometry can use nonessential side margins.
`safe-zone-proofs/` places the actual template over the full vertical master,
with the animation at its intended scale and position. No guide is baked in.

`render.py`, `pipeline.py`, `compose.py`, and `finish.py` handle resumable native
rendering, compositing, per-scene encoding and full export validation. Native
FONTs remain editable in the saved source and are converted to meshes only
inside the render session to avoid the known animated tessellation defect.
Metal binary archives are disabled for the renderer process to avoid the
previous Blender crash. Persistent render data and motion blur remain off.

All outputs and intermediates stay directly in this episode's assets package.
Revision 8 and both still studies remain intact. Generated media and caches are
Git-ignored. This is production media for editing, not a published master or a
claim that a final posting-interface review has been completed.

## Production profile

The native 48-sample clay plate was compared with the approved 96-sample still:
mean channel difference 0.280/255, with the sculpture and surface grain retained
on native and phone-size visual review. Numeral-patch composition versus the
full native plate differed by 0.171/255 on average. `production-quality-comparison.json`
and `native-composite-verification.json` retain these measurements.

The unchanged 52 native code/result states are reused from revision 8 after
confirming all 864 typography state mappings match and the newly rendered
frame-551 glyph layer is pixel-identical. `hud-reuse-verification.json` records
all reused layer hashes. Every clay pose and the new-lighting background are
rendered anew, with 48 clay samples and eight ground-AO samples. Text remains
64 samples; the static upper background uses 128 samples. Caches only reuse
identical authored states, with changing numerals rendered against the complete
scene to retain their shading and contact.

`postflight.py` checks all twelve final hashes and the source-script fingerprint,
creates a compact final contact sheet, updates this package status and appends
an automated completion entry to the episode log. The supervisor retries an
incomplete render up to three times and reports failures rather than marking
missing clips complete.
