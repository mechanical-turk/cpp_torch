# Animations Playbook

**Current production standard: Retro Sunset, strongly hand-sculpted studio clay.**
Consolidated September 10, 2026 from the creator's September 5–9 decisions and
the completed Short 07 revision 9. This is the authoritative reusable animation
playbook linked from `AGENTS.md`. Keep animation detail here, not in `AGENTS.md`.

Use this system for a completely different subject: retain the visual language,
canonical components and production discipline; replace the code, data,
relationships and choreography with those required by the new script.

## Start here and reference precedence

1. Read this playbook, [Visual Asset Guidelines](visual-asset-guidelines.md) and
   [Video Resolution Standard](video-resolution-standard.md), then the target
   episode's current script, benchmark evidence and latest production log.
2. Open the [completed Short 07 revision 9 package](../shorts/short-07-false-sharing/assets/blender-clay-scenes/final-v9/README.md)
   and its [editable native scene](../shorts/short-07-false-sharing/assets/blender-clay-scenes/final-v9/false-sharing-final.blend).
   These are the current reusable animation reference, not the older root MP4s.
3. For exact appearance, inspect the [approved hand-sculpted still](../shorts/short-07-false-sharing/assets/blender-clay-scenes/extreme-clay-study-v2/hand-sculpted-clay-sample-2160x2300.png)
   and its [native builder](../shorts/short-07-false-sharing/assets/blender-clay-scenes/extreme-clay-study-v2/build_sample.py).
   Reuse actual meshes, nodes and lights; do not reconstruct the look from adjectives.
4. Create the new package directly inside the target episode's `assets/` folder.
   Define semantic roles, exact labels/counts, code changes, measured results,
   scene boundaries, destination rectangle and end state before animating.
5. Preserve the established aesthetic unless the creator changes it. New topics
   do not need another theme-selection round. Honor an explicit still-review
   pause; continue already authorized work without repeating approval requests.
6. Check native stills, phone-size readability, the real safe-zone template and
   all-frame geometry before the expensive batch. Deliver N numbered scene files.

The latest explicit creator decision and its approved native reference outrank
older package notes. This document's current settings replace contradictory
historical defaults. The full [earlier playbook](animations-playbook-history-2026-09-09.md)
is preserved for exact older recipes and decision history. Episode logs remain
append-only. Do not restore an older “pending” change to an already approved layout.

## The selected aesthetic

Retro Sunset remains the theme. The final choice is pronounced, tactile,
hand-sculpted plasticine: thick rolled rims, broad irregular thumb compression,
soft local folds, shallow smears, restrained fine grain, rich color and physical
depth. This supersedes the smoother toy/plastic appearance and the first extreme
study's glitch-like fingerprint rings.

The geometry must carry the clay look. Rounded silhouettes alone and a generic
noise bump on an otherwise smooth box are insufficient. Use fuller rolled crowns,
recessed faces, visibly sculpted edges and grounded contact shadows. Avoid sharp
accidental creases, faceting, intersecting shells and decorative clutter.

Lighting remains crisp, vibrant and directional, with soft-edged shadows. Strong
form definition and dark recesses coexist with matte clay. Reject washed-out
labels, broad milky reflections, flat illumination and a cheap glossy toy look.
Toon shading, black outline fixes and switching one worker to a different
material style were rejected. Solve contrast with color, geometry and lighting.

Do not use concentric/radial-wave shader marks to imitate fingerprints. They
looked like bottom-surface glitches. Use irregular physical presses and
nonperiodic smears. The smooth elliptical **background gradient** is still wanted;
its rejection must not be confused with the rejected repeating surface rings.

### Palette and background

The current three-color arrangement is orange/peach ground, turquoise-teal
`#008F88`, and cobalt `#2558BE`, with burgundy/plum behind the code. The yellow
worker lacked contrast against orange and was replaced. Carry each worker's
color through its core, variable, path, packet and owned region. Keep its identity
stable when another region changes ownership. Use dark recessed faces and ivory
physical lettering. Judge the lit colors together at phone size.

The Short 07 dark worker faces use teal `#073E3F` and blue `#132958` where those
ownership materials apply. The older gold/amber scalar and navy history cradle
remain available as subject-specific Short 06 components, not the default
replacement for the approved two-worker palette.

Retain the native continuous, opaque, edge-to-edge Retro Sunset ground and its
contact shadows. The original gradient recipe uses peach `#C67653`, warm orange
`#B35C45`, burgundy `#572536`, and plum `#2D1223`. Copy the current native nodes
and camera mapping to reproduce their lit appearance. Keep the orange hotspot
near the objects and away from white code. Expose background-highlight position
separately from foreground placement; moving one does not automatically fix the other.
No black bars, transparent edges, rounded outer canvas or visible composite seams.

### Actual sculpted material and geometry recipe

Use the [revision 9 builder](../shorts/short-07-false-sharing/assets/blender-clay-scenes/final-v9/build.py)
for exact rings, press locations, linked geometry and node construction. These
are scene-scale settings, not universal constants for an unrelated model scale.

| Element | Current native treatment |
| --- | --- |
| Counter/core shell | Shared rounded-rectangle loft; 128 evenly spaced perimeter vertices per ring; fuller rolled crown, broad irregular compression and local folds |
| Tray shell | A separate shared loft with thick rolled rim, recessed interior and softened folds |
| Surface subdivision | Identical level 2 / render level 2 on sculpted shell peers |
| Path pills | One shared, subtly pinched dash mesh |
| Physical lettering | Raised native curves; extrusion .009, bevel .005, bevel resolution 4; apply consistently to hidden alternate numerals and bubbles too |
| Pigment | Noise scale 3.8, detail 2; restrained darker/lighter variation around the semantic base color |
| Roughness | Noise-driven .68–.84 |
| Highlights | Coat 0; specular IOR level .27; sheen .08 |
| Subsurface | Weight .035, scale .08, radius (.7, .38, .2) |
| Worked-clay smears | Object-space vector stretch (1.2, 4.5, 1.5); noise scale 4, detail 2.4, roughness .45; bump strength .28, distance .019 |
| Fine grain | Object-space noise scale 95, detail 2; bump strength .17, distance .008 |

Keep sculptural displacement and texture coordinates local to the object so
copies and moving objects do not acquire different contours or swimming detail.
No randomized surface changes between frames. Preserve object-linked worker
materials when replacing shared mesh data.

If ownership drives a material with a pigment ramp, animate **both ramp endpoint
colors** with the owner, preserving their tint variation. Animating only the
Principled Base Color after connecting a ramp leaves the visible color frozen.
Include animated material state in render-cache keys.

### Camera and light rig

Reuse the current packed camera, studio and color-management settings with their
scene scale. Preserve the perspective view; the earlier orthographic treatment
was superseded. Keep depth of field and motion blur off for the legible technical
scene. Use native outlines for text rather than trying to recover sharpness by
upscaling or post sharpening.

The native perspective camera is at (0, -22, 22), with 80 mm lens, 36 mm sensor
and horizontal sensor fit. Color management is `Khronos PBR Neutral`, look `None`,
exposure 0. The packed rig contains the exact rotations and parent relationships.

| Light | Position | Energy | Shape and size | RGB color |
| --- | --- | --- | --- | --- |
| Warm key | (-5, -4, 7) | 1650 W | Rectangle 2.2 × 4.5 | (1, .92, .82) |
| Cool edge strip | (3.5, 1, 6) | 780 W | Rectangle 1.1 × 4.5 | (.69, .82, 1) |
| Restrained front fill | (1, -12, 5) | 140 W | Disk, size 6 | (.88, .93, 1) |

The inherited arrow softbox is disabled at 0 W in this scene; the result arrow
uses the unlit typography treatment. Do not accidentally restore the older
95 W arrow light or 1600/720/170 W main rig. Do not blindly transfer wattages to
new scene units or flatten shadows to make the surface look softer.

## Composition, resolution and safe zone

For continuing this mobile animation layout, use the approved rectangle below.
The full vertical master and the animation asset are different deliverables.
Render only pixels the edit uses; do not spend GPU time rendering an unused
presenter region or an oversized asset that is immediately downscaled.

| Setting | Approved current value |
| --- | --- |
| Vertical master | 2160 × 3840 |
| Native animation source | **2160 × 2300** |
| Placement in master | **(0, 0)**, full width, no scaling |
| Recording region below | Remaining 2160 × 1540 |
| Frame rate | 24 fps |
| Viewing preview | 1080 × 1150 |
| Background | Fully opaque, continuous gradient |

The requests for 106% height, then +6%, then 95% of that sample were iterative
composition adjustments. The accepted result is 2160 × 2300; **do not apply those
percentages again**. The prior 2360 × 2352 source and lower-screen 2160 × 2352
layout are not this composition. A different destination must declare its own
rectangle and pass the same checks; it does not change the 4K master standard.

Use the actual [1080 × 1920 safe-zone template](../assets/all-platforms-safe-zone-template-1080x1920.png).
Scale it 2× over a complete 2160 × 3840 master with the animation at its intended
placement. Do not stretch the guide onto the shorter animation source. Keep
proofs separate; never bake the overlay into media.

- Template safe rectangle at 4K: x=120–1872, y=440–2840. Intersect with the
  animation rectangle; its bottom is y=2300. Add inner padding for text.
- Revision 9's internal code/result audit uses x=180–1812, y=480–1180;
  physical-label audit uses x=120–1872, y=440–2260. These are this layout's
  production guards, not platform specifications.
- Check opening, changed-code entry and underlines, airborne crossing, landing,
  result reveal and final activity. Audit essential labels and rising +1 bubbles
  across all frames, including overshoot. Nonessential outer rims may extend
  into side margins; never claim every object pixel clears the interface.
- Review native size and phone size. Actual TikTok header coverage outranks an
  old geometric calculation. Before release, follow the real posting-interface
  checks in [Visual Asset Guidelines](visual-asset-guidelines.md) and the
  [Short Upload Gate](../../docs/operations/short-upload-gate.md).
- If foreground placement changes, move code, underlines, models, labels,
  result and arrow coherently. Camera changes alone can leave camera-parented
  text behind. Recheck the background hotspot, pixel partition and all bounds.

**Historical Short 06 exception:** its last 15-second render still had a noted,
unrendered additional +100 px whole-foreground correction for TikTok headers.
That instruction belongs to that file. It does not require shifting approved
Short 07 revision 9 again. The exact old offsets and measurements are retained
in the [history snapshot](animations-playbook-history-2026-09-09.md).

## Content, typography and minimal results

The Blender render is a visual aid. Omit titles, captions, banners, narration,
explanatory paragraphs and nonessential benchmark detail. Keep necessary code,
field labels, values and relationships. Recompose the usable canvas after
removing overlays rather than leaving empty heading slots. Presenter narration
and editorial captions are separate from these silent scene assets.

Every needed physical field must be labeled: `score` and `history` in Short 06,
`a` and `b` in Short 07. Equivalent objects get equivalent emphasis. The earlier
left/right-only score highlighting with an untouched center was rejected.
Object counts, order and values must match the current subject, including while
moving. Never reuse another episode's numbers as new evidence.

### Code

For a code-driven experiment, show the actual meaningful before/after edit in
readable syntax-highlighted code. A diagram does not replace that code. Preserve
struct grouping when colocation is the point. In Short 07 both layouts contain
one four-row `struct Counters` with its braces. After the edit:

```cpp
struct Counters {
  alignas(128) atomic<uint64_t> a{0};
  alignas(128) atomic<uint64_t> b{0};
};
```

`alignas(128)` must stay on the same line as its atomic declaration. The creator
explicitly rejected splitting it onto a new line and requested a smaller font
to fit. This is the benchmark's chosen alignment; it is not a universal cache-line
size or a default for unrelated experiments. Keep future snippets faithful to
the code actually tested.

Use packed Menlo native glyphs with unlit/emission syntax materials. The current
font is **100 font units**, consistently sized for both layouts. The earlier
1.5× enlargement and 150-unit sample do not override the approved inline fit.
Remove irrelevant boilerplate before shrinking; then size the longest complete
required declaration to fit safely. Never let “bigger” mean cropped or obscured.

The current camera-local text plane uses z=-7 and
`unit = (7 * camera.sensor_width / camera.lens) / 2160`; font size is `100 * unit`.
These units are not visible glyph pixels. Short 07 row origins are x=200, with
baselines y=590, 715, 840 and 965. Copy the actual font geometry and verify bounds.

| Syntax role | Current code color |
| --- | --- |
| Plain text / punctuation | `#FFF8EB` |
| Keywords | `#EDC7FF` |
| Types | `#B8F2EB` |
| Numeric literals | `#FFE0A3` |
| Changed-expression underline | `#7AF5C4` |

Physical labels retain raised ivory clay; use the packed label/numeral faces from
the native scene. Result numbers use Arial Black and units use Arial Bold.
Light-independent code and results must not become washed out by the studio rig.

Make the code edit noticeable: keep header/braces stable, stagger changed rows,
slide/flatten old rows, unfold/slide replacements and briefly underline the new
expression. Short 07's two rows start eight frames apart; old-row exit takes
8 frames, replacement starts at +9 and unfolds over 18. Underlines travel with
the code and retract before results. Inspect moving bounds and row clearance.

### Results and arrow

Every benchmark result includes the two measured timings **and the speedup
multiple**, computed from the same matched measurements and rounded defensibly.
Short 07 uses `244.52 ms → 44.19 ms` and `5.5× faster`. Necessary scope belongs
in narration/notes: “in this test.” No machine specs, prose panel or invented ratio.

Use coral `#FF8D6C` for the first timing, mint `#7AF5C4` for the improved timing
and ratio, and a clean ivory arrow. Align the visible optical centers of arrow
and values, not their baseline origins. Keep units smaller and numbers prominent.
Current timing glyph heights are 120 px, units 46 px, ratio 126 px; timings center
around y=640 and the ratio around y=880. Values enter with restrained settling,
the arrow draws on, then the ratio appears and stays readable.

Build the arrow as one continuous filled, rounded outline with depth and bevel.
Intersecting tubes/shaft/head parts produced corrupted geometry. Inspect its
silhouette and partial reveal. Use an Object/local-X reveal mask normalized to
the actual shape; Generated coordinates previously caused an all-or-nothing
reveal. The current arrow uses 2-unit extrusion and 6-unit bevel in the same
pixel-to-camera unit system; reuse its native construction.

End on the final meaningful result. No return-to-code outro, redundant recap or
forced 19-second duration. A separately numbered discussion scene may hold the
result while meaningful background activity continues. The creator controls the
final cut; neither Short 06's 15 seconds nor Short 07's 36 seconds is a universal
length requirement.

## Reusable structure and consistent objects

Keep explicit collections for `01 • Clay models`, `02 • Code and results`, and
`03 • Studio`. Group compound objects under named assembly roots so shell, inset,
label and value travel together. Keep studio, semantic data, typography and
motion controls separate. Expose configuration for labels/counts, palette,
spacing, placement, background highlight, camera, events, frame ranges, quality
and output paths. Existing episode scripts are references, not a claimed generic
factory; replace their episode-specific constants deliberately.

- Build one complete canonical assembly per family and make linked mesh copies.
  Duplicate the entire assembly, including inset, modifiers, labels and local
  transforms. Copy font data when displayed text differs.
- Repeated trays share mesh and scale. Peers have identical baseline dimensions,
  modifier settings, depth placement and deformation recipe. Do not fit each
  peer independently to a projected width or compensate for perspective by resizing.
- Check evaluated world dimensions and family scale rules as well as shared data.
  Copying mesh pointers alone did not prevent the original inconsistent boxes.
- Use the same press/deformation recipe for peers. A counter can visibly compress
  when it writes; event-specific compression does not justify different baseline sizes.
- Preserve actual members and counts through motion. For Short 06 the historical
  invariants are scores 7/2/9, three labels per field, fifteen history cards per
  player and forty-five total. Those are not contents of every future animation.
- Lift far enough to clear intermediate geometry, including the thicker new rims.
  Check the crossing, not just opening/landing. A larger clear lift arc fixed the
  earlier score/history intersections.

## Motion: causality, weight and continuous activity

Animate the explanation, not arbitrary decoration. Relate each script line to
one observable action. Show the request before its consequence and preserve
what remains logically unchanged. Schematic motion and illustrative counts must
not be described as measured processor traces or literal hardware travel.

Use anticipation, resisted launch, acceleration, modest banking, overshoot and
settling to give the clay mass. Avoid a massless constant-speed glide or an
excessively slow tray that stalls the explanation. Use controlled squash/press,
clear lift arcs and small landing compression without changing peer baselines.
The current native poses are authored **on twos** in a 24 fps stream: two-frame
holds produce deliberate stop motion. Do not smooth them with optical flow or
invent extra interpolated frames. The shapes, material and motion must all read
as clay; a still's surface treatment alone is not a demonstration of physics.

### Short 07 ownership recipe

Two cores update different counters within one cache line. The shared tray,
both members and its label move left-to-right and back during contention.
Color the whole owned region, not only a thin rim. Counters retain worker colors.
The transfer represents coherence ownership, not a change in memory address;
the later padding move changes b's relative placement.

The final three-second handoff cycle supersedes the older four-second version:

| Relative frame at 24 fps | Action |
| --- | --- |
| 0–20 | Substantial request packet travels toward the counter/line |
| 24 | Whole line takes the requester's color, after arrival |
| 30–48 | Tray transfers with anticipation, acceleration, bank, overshoot and settle |
| 50 and 66 | Two illustrative writes after landing |
| 72 | Next handoff cycle |

Continue transfers throughout all three contention scenes. Do not stop the tray
while cores are still competing. Padding ends the handoff. Preserve the packed
member spacing during transfers and the location of a within its own tray during
the later common reframe. Show b lifting, crossing into the second equally sized
tray and settling. Extra unused space makes the layout change visible.

Packets must be large enough to follow. The selected continuous clay packet
consumes nearby dashes; adjoining pinched pills swell and release as it passes.
Avoid a tiny sphere racing over a thin dashed line without interacting with it.
Paths must remain high-contrast against the orange ground.

After each write, change the visible numeral and give the counter a small
press/settle. A raised `+1` bubble rises into open vertical space; flat tiny +1
text on the face was rejected. Each bubble has its own **40-frame lifetime**,
independent of the next pulse, ownership change or scene boundary. Keep the
variable label fixed. Do not cut off bubbles in later scenes. After padding,
independent pulses, numeral changes and bubbles continue under the benchmark
and final discussion hold.

For the current timeline, padding starts at frame 433, lift at 467, crossing at
485, landing at 529, and results at 577. These are reference choreography values,
not mandatory timings for a new script. The next proposed final-totals experiment
is not depicted as already performed.

## Production and delivery

### Work directly in Content HQ

Create the package under
`youtube-series/<episode-or-shorts-path>/<episode>/assets/blender-<package>/`.
All source scripts, editable `.blend` files, first previews, intermediate PNGs,
logs, numbered videos, stills, proofs and reports belong there from the start.
Keep intermediate frames and logs in `_render/`. Do not render into a separate
Codex workspace, Downloads or temporary directory and copy only the final output
back later. A copy is not the requested production location.

Resolve paths from the package. Preserve previous revisions before replacing
canonical outputs. Point feedback and handoffs to the actual newest render,
not an older root MP4. Do not rename an older file to imply a new render.

### One file per scene

Deliver **N self-contained clips numbered 01 through N**, not one long movie.
Map the script to an ordered manifest with filename, purpose, source frame range,
frame count and duration. One native timeline with scene markers is acceptable.
Each output must contain its full background and all necessary objects/text,
start at timestamp zero and decode independently. Keep consistent camera, color,
resolution and safe placement across the set; no added title cards or black frames.
Meaningful motion can continue across scene boundaries without truncating its
lifetime. Do not bake a cross-scene transition that prevents independent editing.

Revision 9 reference scene map (24 fps, 864 total frames):

| File | Source frames | Duration |
| --- | --- | --- |
| `01-crowded-opening.mp4` | 1–144 | 6 s |
| `02-shared-cache-line.mp4` | 145–288 | 6 s |
| `03-write-ownership.mp4` | 289–432 | 6 s |
| `04-add-padding.mp4` | 433–576 | 6 s |
| `05-benchmark-result.mp4` | 577–672 | 4 s |
| `06-discussion-hold.mp4` | 673–864 | 8 s |

Deliver matching smaller previews. Produce a concatenated viewing copy only
when requested. Do not force new scripts into six scenes or these durations.
For Resolve/mobile assembly, retain a 2160 × 3840 timeline and place this source
at (0, 0) with no resampling. The obsolete `short-07-4k-vertical.fcpxml` described
an older layout and was deleted; it is not a dependency of the clips. An exchange
file is not proof that a Resolve project has been assembled successfully.

### Build, preview and render

1. Match current script and benchmark evidence; establish the semantic invariants.
2. Reuse approved native assets. For a new material, lighting or shape direction,
   test stills first and establish a faithful native Blender still before video.
   Generated images are appearance targets, not production geometry or evidence.
3. Render inexpensive previews of opening, transfer, code change, crossing,
   landing and result; review native detail and actual phone-size legibility.
4. Audit every authored pose, duplicates, intermediate clearance, ownership
   colors, bubble lifetimes, arrow reveal and actual template placement.
5. Verify the production sample level and any layered/cached rendering against
   a conventional native reference before spending the full batch.
6. Render all authorized scenes, automatically encode/validate each as it finishes,
   and preserve resumable checkpoints. Inspect final key frames and endings.
7. Record completion only after the files exist and verification passes. A
   started process or an old file is not a completed animation. Report progress,
   failures and remaining work honestly; keep earlier start entries in the log.

### Tested renderer and recovery

Use native Blender/Cycles. The tested local environment is Blender 5.1.2 on Apple
M1 Pro Metal. Use GPU enabled, kernel optimization `OFF`, MetalRT `OFF`, with
process-local `CYCLES_METAL_DISABLE_BINARY_ARCHIVES=1`. This bypasses the observed
Metal `path_cache_get` invalid-free crash. Do not change global preferences or
assume this workaround is needed on every machine.

An animated FONT tessellation bug dropped glyph fragments in consecutive CPU
and GPU renders. Convert native FONT outlines to meshes once **inside the render
session**, preserving transform animation. Keep native text editable and fonts
packed in the saved scene. Clay uses Metal; transparent typography uses CPU.
Persistent render data is off. Fixed seed 0, animated seed off, denoising on,
reconstruction filter .8, depth of field off and motion blur off preserve stable
surface detail and sharp glyphs.

| Pass | Current verified profile |
| --- | --- |
| Moving clay / model patches | 48 samples, adaptive threshold .012, ground AO 8 samples |
| Native approved hero still | 96 samples; the approved study used threshold .007 |
| Transparent code/results | 64 samples; revision 9 renderer threshold .012 |
| Static upper background | 128 samples, threshold .008 |
| Saved editable scene | 96 samples, threshold .007 |

These settings supersede the old 32-sample/four-AO motion recipe for this
sculpted revision. They were compared against the approved 96-sample still:
mean channel difference about .280/255, with native and phone-size visual review.
The numeral-patch composite differed from a conventional full native plate by
about .171/255. These are reference evidence, not guaranteed quality thresholds
for a new material. Increase quality if noise, crawling texture or edge damage appears.

Cache only identical native states: transforms, visibility, geometry, modifiers,
font shapes, metaball elements, reveal parameters and animated materials matter.
Invalidate affected caches when any of those, the light, camera, gradient,
placement or sampling changes. Reuse static code only after checking that its
geometry, colors, all-frame state mappings and rendered glyphs are unchanged.
Never synthesize moving frames or upscale a smaller render as the native output.

The current optimization splits at **y=990**: upper background 2160 × 990,
lower model region 2160 × 1310, full-size transparent text 2160 × 2300. Verify
content and shadows obey that partition; any reframe can invalidate it. Render
numeral patches with the entire scene present for correct shading. Put numerals
in a non-animated hidden collection for blank base renders: animated object hide
flags were re-evaluated at render time and previously spoiled the cache. Check
patches, seams and full-frame differences before reuse. Keep the editable scene
capable of conventional full-frame rendering.

The supervisor should checkpoint progress, retry interrupted/missing states,
check actual required files even when Blender exits with code 0, and surface
failure. The current implementation permits three resumable attempts. Do not
leave an encoder waiting forever after a renderer silently failed. Avoid stopping
a working render merely because shader compilation or a GPU frame has quiet logs.

### Encoding, verification and source control

Encode native dimensions without resizing: H.264, CRF 16, medium preset,
`yuv420p`, BT.709 metadata, fast-start and no audio. Viewing previews use Lanczos
1080 × 1150 and CRF 18 for this source size. Use actual frame ranges for duration.

Before delivery, check every native and preview file with `ffprobe` and a full
decode: width/height, 24 fps, expected frame count, duration, zero start, no audio,
and intended final state. Verify current hashes, script/benchmark consistency,
all-frame text bounds, peer dimensions, continuous background, correct labels,
clear crossing, ownership order and continuing final activity. Local template
proof is distinct from final platform-interface clearance.

Package native clips, previews, packed editable source, builders/render/encode
scripts, manifest, key stills, separate guide proofs, README, status and meaningful
verification reports. Append episode production events without rewriting prior
log entries. Record approved reusable choices here; keep episode measurements
and execution detail in its package/log. Parameterize or replace source paths
and frame constants when starting another episode. Inspect script side effects:
revision 9 `build.py` builds/audits without rendering, while older builders may
start previews automatically. Reading this playbook is not a render request.

Keep reproducible source and decision documents in Git. Keep generated Blender
PNGs/JPEGs/EXRs, `.blend` and numbered backups, MP4/MOV/WAV, generated JSON,
logs, temporary/partial files, `_render/` caches and archived iteration outputs
covered by the scoped `.gitignore` rules. Look-development images, review contact
sheets, copied source snapshots and Resolve hang diagnostics also contributed
noise and have scoped exclusions. Check the **whole git diff and untracked
files**, not only the index, when the creator asks about artifact clutter.
Ignoring files does not delete the working renders. Do not blanket-ignore source
scripts or unrelated assets. When a commit is requested, include only authorized
animation work and preserve unrelated edits; no unsolicited commits or pushes.

## Historical decisions retained and current source map

The [full history snapshot](animations-playbook-history-2026-09-09.md) retains
all prior numerical recipes, Short 06 timings, early theme/object alternatives,
width changes, vertical corrections, light tables and source references.
The latest choices above supersede those recipes where they conflict. In particular:

- Retro Sunset won the theme exploration; clay won the object-style exploration.
  The native image had to match the generated reference before video was approved.
- Missing score labels, arbitrary unequal highlights, small fonts, washed-out
  white text, a malformed arrow and busy overlays were explicitly rejected.
- Independent box fitting caused unequal scores/history; canonical duplicates
  and common family scale replaced it.
- Early +200 px and successive +100 px placement changes belong to their source
  revisions. The orange hotspot moved with the readability correction. Do not
  accumulate old offsets on the final approved composition.
- The 19-second code-return ending was removed. Useful result holds remain allowed.
- Yellow-on-orange, toon contrast fixes, tiny fast pulses, flat +1 text,
  color-only ownership and stopping tray/bubble activity were rejected.
- A slower causal opening was followed by a request for stronger momentum and
  resistance. Preserve the final sequential but weighted three-second handoff.
- Code must show packed members together, then inline alignment in the same
  struct. Larger fonts were reduced to fit the actual supplied safe zone.
- The first extreme study's radial artifacts were removed before the final
  hand-sculpted study was approved and applied to all six scenes.

| Reference | Purpose |
| --- | --- |
| [Final-v9 package and scene sources](../shorts/short-07-false-sharing/assets/blender-clay-scenes/final-v9/README.md) | Current reusable animation, completed six clips, checks and native asset recipe |
| [Final-v9 builder](../shorts/short-07-false-sharing/assets/blender-clay-scenes/final-v9/build.py) | Exact sculpted geometry/material application; loads the previous animated scene |
| [Final-v8 builder](../shorts/short-07-false-sharing/assets/blender-clay-scenes/final-v8/build.py) | Underlying code layout, semantic invariants and authored choreography preserved by v9 |
| [Approved sculpted still package](../shorts/short-07-false-sharing/assets/blender-clay-scenes/extreme-clay-study-v2/README.md) | Selected surface, silhouette, gradient and lighting reference |
| [Short 07 script](../shorts/short-07-false-sharing/script.md), [benchmark evidence](../shorts/short-07-false-sharing/benchmark-results.md), [log](../shorts/short-07-false-sharing/log.md) | Episode-specific facts; later creator-approved animation decisions supersede outdated visual directions in the script |
| [Short 06 package](../shorts/short-06-data-layout/assets/blender-clay-animation/README.md) and [log](../shorts/short-06-data-layout/log.md) | Original scalar/history component family and historical placement caveat |
| [Historical playbook snapshot](animations-playbook-history-2026-09-09.md) | Preserved earlier decisions; never the active default |

When another choice changes, update its authoritative section and append the
supporting episode-log entry. Keep the reusable playbook, historical evidence
and actual production files connected so the next session can reproduce the
system without relying on conversation memory.
