# Animations Playbook

Reusable Blender production system for **Retro Sunset studio clay**. Established
from the creator's September 5–6, 2026 animation decisions and revisions.
Use this for a new subject, with new data and choreography, while retaining the
same visual family, scene structure, reusable objects and production discipline.

## Start here next time

1. Read this playbook, [Visual Asset Guidelines](visual-asset-guidelines.md) and
   [Video Resolution Standard](video-resolution-standard.md). Those documents
   own general semantic consistency, overlay format and master-resolution rules;
   this document supplies the Blender implementation and selected art direction.
2. Read the **pending placement correction below before copying any scene**.
3. For the latest approved surface and sculpture treatment, open the
   [hand-sculpted clay reference](../shorts/short-07-false-sharing/assets/blender-clay-scenes/extreme-clay-study-v2/README.md).
   Its native Blender scene establishes the stronger clay aesthetic selected on
   September 9. Preserve the target episode's approved composition and motion.
   For the original component system, open the [current editable animation](../shorts/short-06-data-layout/assets/blender-clay-animation/cpp-data-layout-clay-animation.blend)
   and inspect its [result still](../shorts/short-06-data-layout/assets/blender-clay-animation/stills/06-final-result.png).
   These contain the corrected repeated geometry, actual materials, camera and
   light rig. Reuse the native assets; do not reconstruct their appearance from
   adjectives or a remembered screenshot.
4. Copy the scene into the new subject's asset directory. Keep the style and
   components; replace the old labels, values, code, measured results and motion.
5. Specify the new conceptual action and data invariants before animating.
   Adapt the timeline to that action. Neither 15 nor 19 seconds is a required
   duration for future animations.
6. Deliver one numbered, self-contained video per scene, following the scene
   export contract below. A single long animation is no longer the default.
7. Build and render directly inside the subject's Content HQ `assets/` folder.
   Use the production-location rule below; do not stage renders elsewhere.

Suggested invocation: “Use the animations playbook to build an animation about
[subject], using the Retro Sunset clay elements. The action to show is [action].”

## Pending placement correction — applies before the next render

**The creator reports that TikTok headers cover the current content. Move the
entire foreground down another 100 px relative to the latest 15-second render.**
This is the latest instruction. It supersedes earlier claims that the local
composition audit alone established safe placement.

This means code, code-change underlines, models, their field labels, benchmark
values, arrow and result text together. It is not another code-only adjustment.
Keep the canvas size and object/font scale unchanged. Preserve the continuous,
full-bleed gradient and keep its orange highlight away from white code.

**Status: noted, not implemented or rendered.** The creator explicitly requested
documentation only. The current `.blend`, scripts, PNGs and MP4 still contain
the previous placement. Do not describe them as containing this new correction.

| Measurement at 2360 × 2352 | Current rendered value | Arithmetic target after +100 px |
| --- | --- | --- |
| Visible code/result vertical bounds over the sequence | y=348.25–1036.85 | y=448.25–1136.85 |
| Model vertical bounds over the sequence | y=1063.77–2129.08 | y=1163.77–2229.08 |
| Code first-row baseline origin | y=415 | y=515 |

These targets are a placement specification, not proof of platform clearance.
The shifted models would leave about 123 px at the bottom of this source asset;
recheck the complete edited vertical video, including its scale/placement and
platform controls. The creator's observed header overlap outranks the old
geometric audit. Do not invent a universal TikTok-header pixel height.

For the next implementation, use one explicit foreground vertical-offset control
so all components move together. A camera-only change can leave camera-parented
text unmoved relative to the frame; verify projected positions for both 3D and
camera-parented content. Recalculate render partitions and invalidate affected
caches. Do not shift a finished rectangular image into black or transparent bars.
Keep a separate background-highlight position control and check contrast after
the content moves. No second exact gradient displacement was specified in this
latest instruction; its prior implemented displacement was +100 px.

## Visual identity

**Theme: Retro Sunset. Object treatment: sculpted, tactile clay. Lighting:
crisp, vibrant, directional studio lighting with soft-edged shadows.**

The selected appearance combines deep burgundy/plum, warm peach/orange ground,
golden pillow-like objects with recessed amber faces, saturated cobalt inserts,
navy cradles and ivory lettering. Surfaces should look deliberately sculpted:
rounded contours, visible thickness, recesses, subtle grain and clear contact
shadows. Preserve the reference's depth and silhouette as well as its colors.

Soft clay shapes do not imply flat, uniformly soft lighting. The creator rejected
a washed-out, cheap toy/plastic appearance and requested sharper definition,
stronger contrast, richer color and more interesting studio illumination.
Keep tactile matte surfaces while using controlled highlights to describe form.
Avoid blown-out labels, broad milky reflections and arbitrary decorative clutter.

The generated clay hero established the direction. The native studio still
established the approved lighting and material execution. The current animation
adds corrected uniform geometry and larger code. Each reference has a different
role; none overrides the pending placement correction.

## Content and composition

- The animation is a visual aid. Omit title cards, captions, banners, narration
  and explanatory paragraphs from the render unless a later brief asks for them.
- Keep useful code, object/field labels, necessary values, connecting arrows and
  a minimal measured result. Do not remove information needed to identify a field.
- For a code-driven experiment, include a readable syntax-highlighted excerpt
  of the actual before/after change in the animation. A diagram does not replace
  the code. Reflow excerpts at the established large font size and animate changed
  expressions visibly; omit surrounding boilerplate before shrinking text.
  Keep grouping syntax when it teaches the mechanism: show related members inside
  one visible struct, and preserve that same struct while inserting alignment or
  padding. Do not show disconnected declarations when their shared layout is the
  point. In Short 07, `struct Counters` and its braces remain visible while both
  member declarations gain `alignas(128)`.
- Compose deliberately for the available space after removing overlays. Do not
  leave holes where deleted headings used to be or shrink a wide card into a
  larger blank canvas.
- Related objects get the same visual treatment. The early choice to highlight
  only left and right scores while ignoring the center was rejected. Use selective
  emphasis only when the new subject gives it a clear semantic reason.
- Match all physical labels to the data shown in code. In Short 06, both `score`
  and `history` must be labeled. Neither label substitutes for the other.
- Keep foreground text on the darker portion of the gradient. When moving text,
  reconsider the orange highlight position as part of the same composition task.
- Maintain separation between code and the model action throughout the timeline,
  including transient flips, underlines, lifted objects and overshoot.
- Measure alignment using visible glyph/shape bounds. Align an arrow with the
  optical centers of adjacent values, not their text baseline origins.
- Check moving cues at phone size, not only static labels. Give data pulses
  enough travel time to follow and hold update cues long enough to read. Thin
  warm-colored paths on the warm ground need a contrasting clay hue and adequate
  thickness; a small shadow alone is insufficient. Preserve the native matte
  clay shading. Toon/black outline treatments were rejected for inconsistent
  styling; solve contrast through the palette, lighting and shape instead.
- When color communicates ownership of an entire region, color that region
  clearly. A thin rim-only change was too subtle in the false-sharing scene.
  Keep the independent variables' worker identities stable as ownership changes.
- Give ownership transfers a physical action when that helps explain the subject.
  In Short 07, the shared cache-line assembly travels left to right and back
  throughout the contention scenes,
  carrying both counters and its label while its color follows the owner.
  Preserve member offsets and geometry during this motion. This represents a
  coherence handoff, not an address change; the later padding move changes b's
  relative placement. Do not rely only on a color switch for this opening.

### Causal handoff timing and sustained activity

Make dependent steps visibly sequential: the request pulse travels and arrives,
then the entire cache line takes the requester's color, then the tray transfers
to that core. Do not change color or move the tray before the pulse arrives.
Allow enough time to read each step. The revised Short 07 handoff uses about one
second of pulse travel, a short arrival/color hold, and a 1.5-second transfer,
inside a four-second handoff cycle. Its opening lasts eight seconds for a round
trip; these are editable source durations, not a narration pacing requirement.

Continue the back-and-forth through every scene in which the cores still contend
for the shared line. Stopping tray motion after the opening contradicts the
mechanism. Stop the handoff when the layout comparison separates the counters.
Give each rising +1 its own lifetime so a new request, ownership change or clip
boundary does not truncate it. In the separate layout, continue independent
pulses, numeral changes and rising +1 bubbles through the benchmark and discussion
scenes. Hold the result text while the underlying demonstration stays active.

### Increment feedback and three-color separation

For counter updates, let a raised `+1` clay bubble rise into the open vertical
space above the variable. Keep it readable long enough to follow. A flat `+1`
stamped onto the variable face was rejected. Pair the bubble with a visible
numeral increment and a small press/settle so the value change is unambiguous.
Keep the variable label stable and clear. Illustrative update counts are schematic,
not fabricated measured totals or a processor trace.

For the Short 07 palette, retain the orange Retro Sunset ground and cobalt worker;
use a distinct turquoise-cyan (`#008F88`) for the other worker. This is a three-color
composition. Carry each worker color through its core, counter, path, pulse and
owned region. Judge the lit materials together at phone size: separation from
both the cobalt peer and orange ground matters more than isolated color swatches.
Keep dark recessed faces and ivory lettering; do not restore toon outlines.

### Canvas and safe-area decisions

The base lower-screen layout is governed by the linked visual guidelines:
2160 × 2352 under a 2160 × 1488 presenter region in a 2160 × 3840 master.
For this animation family, the creator explicitly widened the asset to
**2360 × 2352**, adding 100 px on each side with the same gradient and no content
rescaling. Retain that revised source size when continuing this family unless
the next brief specifies another destination. It is not a new vertical-master
resolution standard.

The early 200 px downward correction was implemented before the clay rebuild.
The latest larger-code render later moved the code origin down 100 px and the
orange highlight down 100 px. The new pending correction is **another +100 px
for all foreground content relative to that latest render**. Do not add offsets
from old, superseded camera setups to an arbitrary baseline.

Review layout at native resolution and at ordinary phone size. Before release,
follow the actual platform-interface checks in the visual guidelines and the
[Short Upload Gate](../../docs/operations/short-upload-gate.md). A successful
local bounding-box test does not establish that TikTok headers are clear.

When the creator supplies a safe-zone overlay, composite the actual template
over the complete vertical master at its proportional scale, with the animation
at its intended edit position and size. The repository's
[1080 × 1920 template](../assets/all-platforms-safe-zone-template-1080x1920.png)
scales 2× on a 2160 × 3840 master; do not stretch it to the shorter animation
asset. Measure visible glyph bounds against the template with inner padding,
including the header and right-side controls. Retain a separate overlay proof;
never bake the guide into the delivered animation.

Make this a required check before final scene rendering: inspect the opening,
changed-code transition (including moving rows and underlines), padding layout,
benchmark and final hold beneath that overlay. Audit essential text and object
labels across all frames, including overshoot and rising update bubbles. Use the
template's safe rectangle x=120–1872, y=440–2840 at 4K, with extra inner padding
for code and results. If placement changes in the edit, repeat the check.

For the approved Short 07 revision, the source asset is **2160 × 2300**, placed
at (0, 0) in the 2160 × 3840 master, leaving the recording region below. This
explicit composition supersedes the older lower-screen layout for that Short.
The still established Menlo at 150 font units with visible bounds approximately
x=210–1707, y=503–981. The creator subsequently rejected putting `alignas(128)`
on a separate row: keep it inline with each atomic declaration. Reduce the code
font consistently to fit the longest complete declaration inside the safe zone,
retaining sharp native outlines and syntax colors. Both layouts keep the same
four-row struct. Keep the template proof separate from final media.

## Reusable scene structure and components

Retain three explicit collections, with descriptive object/material names:

| Collection | Responsibility |
| --- | --- |
| `01 • Clay models` | Physical objects, assembly roots and their labels |
| `02 • Code and results` | Camera-parented code rows, underlines, values and arrow |
| `03 • Studio` | Camera, continuous ground and studio lights |

Build each compound model under an assembly root. Animate the root so shell,
inset, label and value remain attached. Keep studio, typography, data geometry
and motion controls separate so a new subject can replace one without rebuilding
the others. Expose content, semantic palette assignment, spacing, offsets, counts,
camera, beat times, frame end, render quality and output paths as configuration.
This is the recommended interface for future builders, not a claim that a generic
factory script already exists.

### Canonical objects

| Reusable element | Construction and use |
| --- | --- |
| Gold scalar tile | Thick continuous rounded shell; broad recessed amber face; raised ivory field label and value. Use for an active scalar, item or node when appropriate to the new subject. |
| Navy collection cradle | Continuous rounded open container; separate dark front plaque; raised ivory label. Use for retained/grouped data, not as a decorative empty box. |
| Cobalt data card | One rounded card mesh, duplicated for the actual number of elements. Its count and spacing must communicate the data truthfully. |
| Ivory arrow | One rounded filled silhouette with depth; directional relationship or result transition. |
| Code block | Independently animated syntax-colored rows on a dark background, with a deliberate changed-line transition. |
| Result group | Bold primary value, smaller unit, aligned arrow, second value and only the essential comparison. |

The native `build.py` contains rounded-ring lofting and supported recessed-face
construction. Reuse its `points`, `loft`, `rounded`, `text`, material and light
helpers when a new canonical component is necessary. Use the current animation's
duplication logic rather than the old still's per-object fitting loop.

### Uniformity is structural

The general duplication rule is in Visual Asset Guidelines. In Blender:

1. Build one complete canonical assembly for each object family. The current
   corrected scene uses the center score and center history as its masters.
2. Make linked duplicates of the meshes (`copy()` with shared `data`). Duplicate
   the entire assembly, including labels/insets and modifier configuration.
   Copy font data only when the displayed value must differ.
3. Keep local component transforms, dimensions, bevel/subdivision settings,
   materials and deformation parameters identical within a family.
4. Use one common scale/depth specification and equal scale animation for peers.
   Position them as a group or on shared rows. Do not fit each peer to a target
   projected width by independently changing its scale.
5. Use local/object-space sculpture coordinates for repeated clay contours.
   World/global displacement produced different silhouettes at different positions.
6. Check actual evaluated/world dimensions as well as data sharing and appearance.
   Linked meshes alone did not prevent the earlier inconsistent parent scales.

Natural perspective shows different sides at the frame edges; directional light
also changes highlights. These are not reasons to compensate by resizing peers.
When apparent equality is essential, solve camera/layout for the family together.

For Short 06 specifically, retain scores 7, 2, 9, three score labels, three history
labels and fifteen history cards per player, forty-five total. These are episode
data invariants, **not fixed contents of every future animation**. New subjects
must supply their own labels, counts, relationships and measured results.

## Materials and colors

### Approved sculpted-clay upgrade

The creator selected the September 9 [native hand-sculpted study](../shorts/short-07-false-sharing/assets/blender-clay-scenes/extreme-clay-study-v2/README.md)
as the continuing aesthetic. Use its actual Blender geometry, shader nodes and
light rig. The older material table below describes the original Short 06
baseline; this approved sculpted treatment supersedes its smoother finish.

- Build thick hand-rolled rims with broad, irregular thumb compression and a few
  soft physical folds. Sculpture must affect silhouette and shading, rather than
  relying only on a surface bump map.
- Reuse one sculpted master mesh per family with linked duplicates and common
  modifiers. Handmade geometry is not permission to change peer dimensions.
- Use nonperiodic worked-clay smears, fine grain and restrained pigment variation;
  matte roughness around 0.68–0.84, no clear coat, restrained specular and shallow
  subsurface scattering preserve crisp studio definition.
- Use softly beveled, raised physical lettering. Keep code and results as sharp,
  unlit native glyphs with the approved syntax colors and safe-zone placement.
- Retain warm directional key, cool edge separation and restrained fill. For the
  current native scene, the approved key is 1650 W / size 2.2, edge strip 780 W /
  size 1.1, fill 140 W. Copy the rig with its scene scale rather than applying
  those wattages blindly to unrelated geometry.
- When animated ownership colors feed a pigment ramp, animate both ramp colors
  with the ownership state. Keying only the disconnected Principled Base Color
  input would leave the visible material frozen.


Handmade detail must read as physical clay. Concentric or radial-wave shader
marks used as fingerprints were rejected because they looked like rendering
glitches. Prefer broad irregular sculpted presses and nonperiodic surface
smears; inspect these details at native resolution and phone size.

These are the implemented reference settings, not flat sampled display colors.
Hex colors are converted from sRGB to linear before use in Blender nodes.
Reuse the actual node groups and color-management settings to match the render.

| Material / role | Reference color | Roughness | Bump strength | Emission strength |
| --- | --- | --- | --- | --- |
| Gold shell base | `#F7A71B` | 0.56 | 0.20 | 0 |
| Cobalt cards | `#2558BE` | 0.56 | 0.15 | 0 |
| Plum/navy cradle | `#40485E` | 0.56 | 0.18 | 0 |
| Recessed amber face | `#532707` | 0.84 | 0.18 | 0.02 |
| Dark history plaque | `#211728` | 0.79 | 0.09 | 0.04 |
| Raised ivory lettering | `#FFF0D5` | 0.64 | 0.05 | 0.22 |
| Ivory clay arrow | `#FFEBD0` | 0.44 | 0.018 | 0 |
| Ground base, overridden by gradient | `#9E4027` | 0.89 | 0.30 | 0.035 |

The gold height ramp supplies the final hand-tinted appearance: `#883701` at
normalized height 0, `#C77508` at 0.52 and `#FFB522` at 0.90, with eased blending.
Clay materials use zero metallic and a Principled specular IOR level of 0.32;
the ground uses 0.12. Typical fine-grain noise has scale 42, detail 2 and bump
distance 0.014. Broad color variation uses scale 3.5/detail 3. Surface variation
must remain subtle enough that labels and silhouettes stay clean.

The shell/cradle contour uses a small Clouds displacement: scale 0.32, depth 1,
strength 0.021, mid-level 0.5. The current animation correctly evaluates this in
`LOCAL` coordinates for duplicates. Do not restore the old `GLOBAL` setting.

### Continuous Retro Sunset background

Use a physical continuous ground with a camera-mapped, eased radial/elliptical
color gradient and contact shadows. Reference gradient stops, center outward:

| Position | Color |
| --- | --- |
| 0.00 | `#C67653` peach |
| 0.45 | `#B35C45` muted warm orange |
| 0.80 | `#572536` burgundy |
| 1.00 | `#2D1223` deep plum |

The source uses camera-space ellipse scales 8.5 and 6.4, fine ground noise at
scale 48/detail 2, brightness modulation 0.82–1.12, and ambient occlusion distance
0.72 with a 0.75 contact multiplier. Preserve continuous shading and texture
across the entire rectangular canvas. The material center in the latest render
is approximately (1123.30, 1918.61) source pixels, after its implemented +100 px
shift. That material center is not necessarily the brightest lit pixel.

Do not make the backdrop uniformly bright or put its warm hotspot behind white
code. Keep scene-light adjustments and background-highlight positioning separate.

## Camera and studio lighting

The selected native setup uses a perspective camera at `(0, -22, 22)` aimed at
the origin, 80 mm focal length and 36 mm sensor width. The early clean animation
used an orthographic camera; the clay rebuild superseded it. Retain perspective
for this look unless a new brief requires a different camera.

Reference lights in this scene's world-unit scale:

| Light | Position | Aim | Energy | Shape / size | Color RGB |
| --- | --- | --- | --- | --- | --- |
| Warm studio key | `(-5,-4,7)` | `(0,-3,0.8)` | 1600 W | Rectangle 2.7 × 4.5 | `(1,.92,.82)` |
| Cool edge strip | `(3.5,1,6)` | `(0,-3,1)` | 720 W | Rectangle 1.4 × 4.5 | `(.69,.82,1)` |
| Restrained front fill | `(1,-12,5)` | `(0,-3,.9)` | 170 W | Disk, size 6 | `(.88,.93,1)` |
| Arrow softbox, camera-local | `(-.35,2.6,-6)` | camera-local `(0,1,-7)` | 95 W | Rectangle .65 × 1.4 | `(1,.96,.88)` |

World background color is `(0.3,0.23,0.25)` with strength 0.035. Color management
is `Khronos PBR Neutral`, look `None`, exposure 0. Scale these physical settings
coherently if a new scene uses different units; copying wattages into a vastly
different scene does not guarantee the same appearance.

Preserve a strong warm key, cool edge separation, restrained fill and rich
contact shadows. Soft shadow edges should coexist with crisp object contours.
Use dark recessed label faces so lighting cannot wash out white text. Evaluate
the font/background contrast in the rendered frame, not just the material swatch.

## Typography and code transitions

Use packed native Blender text. The selected code face is **Menlo**; object
labels use Arial, object numerals Arial Bold, and result numbers Arial Black.
Keep field labels within each family identical in size, position and treatment.
Code and timing text use emission materials for stable, light-independent color;
physical labels retain the ivory clay material and shallow raised depth.

| Syntax role | Color |
| --- | --- |
| Default / punctuation / identifiers | `#FFF0D5` ivory |
| Keywords such as `struct`, `for` | `#DCAEF1` lilac |
| Types and type names | `#84E3D4` aqua |
| Numeric literals | `#F3C56B` amber |
| Changed-line underline | `#7AF5C4` mint |

The latest code size is **1.5× the original clay video's size**: font data size
`105 * unit` instead of `70 * unit`. This is a Blender font-size parameter, not
a promise of 105 px visible glyph height. At this camera-local plane,
`unit = (7 * 36 / 80) / 2360`, with text at camera-local z=-7.

The rendered layout uses x=285 and first baseline y=415, line step 107 px, with
37 px removed from the blank gap before the loop. The pending whole-content
shift would make the first baseline y=515. Preserve the readable font size;
reflow long snippets and whitespace before making code tiny again.

An immediate old-code/new-code cut was too easy to miss. Use a visible staggered
transition: outgoing changed rows slide/flatten, incoming rows unfold/slide into
place, and brief mint underlines identify the changed expressions. Keep unchanged
rows stable. In the reference, row starts are staggered by 0, 3, 6 and 11 frames;
outgoing motion lasts 8 frames, incoming rows appear on +9 and settle by +24.
Incoming vertical scale overshoots to 1.10, then settles to 1. Outgoing movement
is -38 px and incoming offset +65 px. Underlines reveal, hold briefly, then retract.
Carry underlines with the code whenever changing placement.

## Arrow and minimal result

The early clay arrow looked corrupted. Its replacement is **one continuous,
rounded, filled outline**, extruded and beveled. Do not build it from intersecting
tubes or overlapping shaft/head parts. Check its silhouette and evaluated mesh:
one closed component with no non-manifold edges in the reference check.

Reference arrow construction uses a rounded seven-corner outline, 3 px-equivalent
extrusion and 9 px-equivalent bevel, bevel resolution 6, with a slight 8° tilt.
Use the existing clean arrow asset rather than rebuilding the head by eye.
Draw it on with a material mask in **Object/local X coordinates**, normalized to
the arrow's actual bounds. `Generated` coordinates on the filled curve caused an
all-or-nothing reveal. Inspect a partially revealed frame, not only the final arrow.
The reference normalization spans `-209 * unit` to `211 * unit`, with reveal
progress from -0.02 to 1.02. Recompute that span if the arrow's shape changes.

Every benchmark result must show both measured times **and the measured speedup
multiple**, for example `244.52 ms → 44.19 ms` with `5.5× faster` in Short 07.
The multiple is essential result information; minimal copy does not mean removing
it. Compute it from the same matched measurements, round defensibly, and animate
its entry after the timings. Keep it visible through the final result hold.

Use strong, readable comparisons with minimal copy. Short 06 keeps only
`4.36 ms → 0.35 ms` and `12.5× faster`: coral `#FF8D6C` for the first timing,
mint `#7AF5C4` for the second/result. Timing digits have measured glyph height
145 px, units 55 px, and the ratio 136 px. The arrow and both values share optical
center y=490 in the current render; the ratio centers at y=775. Their pending
targets are y=590 and y=875 when the whole foreground moves down 100 px.

Animate entry with restrained scale/position settling and a directional arrow
reveal. Do not reintroduce benchmark prose, qualifiers, hardware labels or extra
explanation as overlays. Necessary evidence and qualifications belong in the
episode's script/notes; the numbers must still match the actual evidence.
Never reuse Short 06's measured speedup as evidence for a different animation.

## Motion grammar and ending

Use movement to make the conceptual transformation visible: establish a state,
direct attention to the changed element, move/reorganize it, settle, then show
the outcome. Keep retained information visibly present. Animate assembly roots
and shared family scale values so components remain attached and peers remain
consistent. Use eased Bezier keys with clamped handles, controlled anticipation,
clear lift arcs, small landing compression and a restrained bounce.

Reference Short 06 cues at 24 fps, supplied as a recipe rather than fixed future
timing:

| Frames | Action |
| --- | --- |
| 1–159 | Readable initial code and interleaved model arrangement |
| 159–194 | Staggered code transformation; underlines finish retracting by 217 |
| 166–185 | Scores anticipate and lift |
| 185–213 | Scores gather while histories move into their retained row |
| 213–242 | Land, small bounce and settle |
| 289 | First benchmark value appears |
| 294–308 | Clean arrow draws on |
| 305 | Second value enters |
| 314–329 | Speedup enters and settles |
| 360 | End on the completed result |

The score lift was increased from 0.9 to 1.55 world units to clear the histories.
The landing uses about 3% vertical compression and a 0.07-unit bounce. These are
reference-scene values: recompute clearance for different shapes or scales.
Never rely solely on matching opening and closing frames; inspect the crossing.

The return-to-code outro was explicitly removed. **End on the final meaningful
result; do not append a code recap or pad the animation to 19 seconds.** The
creator will handle duration in the edit. The current file happens to be 15
seconds; new animations should use the time their own action needs. Deliver
silent video by default. The early mechanical treatment's sound stem is not
part of the selected clay system.

## Production workflow

### Production location

The creator's September 7, 2026 instruction: **build and render directly in the
`assets/` subdirectory under the episode or Short's folder in Content HQ**.
The creator needs to see previews and work in progress there immediately.

- Create the animation package there before building the first scene. Keep
  scripts, editable Blender files, previews, numbered scene videos, stills,
  manifests and verification reports in that package from the start.
- Put intermediate frames and logs in a clearly named subdirectory such as
  `_render/` inside the same package. Do not render into a separate Codex
  workspace, temporary output folder or unrelated working directory and copy
  the final files over later.
- Resolve output paths from the package location. Archive prior revisions
  inside that assets package before replacing them, so immediate feedback
  refers to the current project files.
- This is the ongoing production default, not merely a final-copy destination.

### Scene export contract

The creator's September 7, 2026 standing instruction: render **N separate,
self-contained video files, numbered 1 through N, one per scene**, so each can
be placed and timed independently in the edit. This replaces the single-long-
animation delivery default for all future animations.

- Map the script's distinct scenes to an ordered manifest before rendering.
  Use zero-padded filenames such as `01-crowded-opening.mp4`,
  `02-shared-cache-line.mp4`; include each scene exactly once without gaps.
- Each clip contains its complete background, objects, necessary labels and
  in-scene action. It must play correctly by itself, with its own timestamp
  origin; do not require another video, external overlay or previous clip's
  decoder state to display it.
- Keep resolution, frame rate, color management, camera, safe-area placement
  and semantic object styling consistent across the set. Preserve intentional
  continuity between neighboring scenes without baking transitions across
  file boundaries or inserting title cards, black frames or fades.
- Start with the scene's readable setup and finish with its complete outcome.
  Match useful action/holds to that scene's script needs; the creator controls
  final timing. Self-contained does not require a frozen last pose: ongoing
  processes can remain active while the result text holds. A discussion scene
  can hold the completed result with continued underlying activity. Do not add
  an unrelated outro or force a duration for the whole set.
- One editable Blender timeline with named markers/frame ranges is acceptable;
  the delivered videos must still be separate. Record clip number, filename,
  purpose, source frame range, frame count and duration in the manifest.
- Verify every clip separately: first/last frames, full decoding, resolution,
  fps, duration, frame count, silent audio default, and correct end state.
  Deliver the numbered clips, matching previews and source package in Content
  HQ. Produce a concatenated viewing copy only when requested.

### Build and review

1. Establish the concept, object meanings, exact labels/counts and end state.
   Keep script/data decisions separate from visual styling.
2. Reuse the current native scene and its components. For a genuinely new visual
   direction, explore inexpensive stills first. Generated images are look targets,
   not production geometry or proof of data counts.
3. For a material, lighting or object-form change, establish it in a native
   Blender still before spending time on the whole sequence. The first clay video
   failed because its objects and light did not resemble the chosen sample.
4. Honor explicit review pauses. Continue already authorized implementation and
   rendering without asking the same permission again. A new topic using an
   established look does not itself require another theme-selection exercise.
5. Make low-cost native previews of the opening, transition/crossing and result.
   Compare them against the relevant reference for silhouette, color, light,
   typography and composition. Check true phone-size readability.
6. Audit all-frame placement and uniformity, and inspect intermediate geometry
   and partially revealed arrows. Correct problems before the expensive render.
7. Render every authorized scene to completion, encode its own numbered clip,
   decode-check all exports, inspect key native frames and verify each ending.
8. Verify the completed package already in Content HQ, preserve prior revisions,
   record verification and any unresolved placement issue, and hand over the videos.

### Rendering implementation

Use native Blender/Cycles for the production clay animation. The reference was
made in Blender 5.1.2 on an Apple M1 Pro. Working Metal configuration on that
machine: GPU enabled, kernel optimization `OFF`, MetalRT `OFF`. A shader-compiler
crash was resolved with those settings. Treat this as a tested local configuration,
not a universal requirement for every machine; do not silently save global prefs.

| Pass | Reference maximum samples | Notes |
| --- | --- | --- |
| Moving models | 32 | Denoise; adaptive threshold .02 |
| Opening model hold | 96 | Denoise; threshold .012 |
| Settled model hold / hero still | 256 | Denoise; threshold .004 |
| Transparent code/results | 64 | Threshold .008 |
| Background region | 128 | Threshold .008 |
| Editable full-frame scene default | 96 | Threshold .012 |

Use a 1 px reconstruction filter. These pass settings were chosen after a native
comparison: the earlier 32-sample moving pass differed from a 96-sample reference
by about 0.60 RGB code values out of 255 on average, with the 99th percentile at
3/255. This is evidence for this scene, not a guarantee for new materials or motion.
Increase quality where a new scene exhibits noise, crawling texture or bad edges.

Cache only identical scene states, including object transforms, visibility,
curve reveal parameters and material animation. Invalidate caches when geometry,
fonts, placement, background, lighting or sampling changes. Reuse verified static
holds; do not synthesize moving frames with interpolation. Preserve all data
throughout the animation, even when out of focus or partially occluded by motion.

The current optimization renders upper 1050 px and lower 1302 px separately at
native width, then composites the transparent code/result layer over the actual
background. It is valid only while content and shadows obey that partition.
**The pending +100 px foreground change invalidates blindly reusing this split.**
Recalculate the boundary or render/composite full-frame layers; inspect seams.
Keep the editable `.blend` capable of conventional full-frame rendering.

Encode the native dimensions without resizing: H.264, CRF 16, medium preset,
`yuv420p`, BT.709 metadata, fast-start, no audio. The tested preview is
1180 × 1176, Lanczos downscale, CRF 18. Frame count and end time must come from
the actual sequence, not an assumed 19-second template.

## Verification and handoff

Before calling a render complete, verify:

- Every frame fits the declared local foreground region, including animated
  glyph bounds and overshoot; distinguish this from platform-interface approval.
- Peer mesh data, local geometry/modifiers and world dimensions match; family
  scales and depth placement stay consistent throughout motion.
- Labels, values, object counts and ordering match the current subject.
- Lift/crossing/landing geometry clears other objects; arrow reveal is continuous.
- White and syntax-colored text remain readable under the actual lighting and
  background at native and phone size.
- The canvas remains opaque and continuous; no seams, accidental padding, hidden
  cropped code or clipped shadows appear after compositing.
- The final frame is the intended outcome, with no unwanted return to code.
- `ffprobe` confirms dimensions, fps, frame count, duration and audio absence;
  both native and preview videos fully decode without errors.

Package the numbered native MP4s, matching smaller viewing copies, scene manifest,
packed editable `.blend`, key-frame
PNGs, build/render/finish scripts, README and meaningful verification reports in
the new subject's Content HQ `assets/` directory. Keep intermediate PNG caches
and logs in its `_render/` subdirectory. Preserve previous finished versions
before replacing the canonical path and update the subject's append-only log.
Render directly there from the first preview; a final copy from another workspace
does not satisfy the production-location rule.

The existing scripts contain absolute paths into the original production
workspace. When starting a new subject, parameterize or replace those paths and
frame-dependent constants before running them. Both `build.py` and
`build_animation.py` trigger rendering when executed; reading this playbook or
making a note is not authorization to run them.

## Decision history and reference precedence

| Decision / correction | Final treatment to carry forward |
| --- | --- |
| Mechanical assembly was too busy | Remove nonessential overlays and explanatory graphics; use the complete canvas deliberately. |
| White text on blue was washed out | Dark recessed faces, stable code colors and rendered contrast checks. |
| Only left/right scores were highlighted | Equal treatment for peers; selective attention requires a conceptual reason. |
| `history` existed but `score` was missing | Label every needed physical field consistently. |
| Result screen had too many words | Keep only measured timings, a clean arrow and the essential comparison. |
| Canvas needed more width | +100 px each side, same gradient, no content scaling; 2360 × 2352 for this family. |
| Initial content was outside the reel-safe area | Implemented +200 px in the old clean scene; later clay placements supersede its raw coordinates. |
| Timing arrow was vertically misaligned and dull | Optical alignment, coral/mint typography, smaller units, draw-on and restrained settling. |
| Code change was easy to miss | Staggered flips/slides and brief underlines, with stable unchanged rows. |
| Three theme directions were explored | Retro Sunset was selected as the ongoing theme. |
| Soft enamel, precision hardware and playful soft-touch were explored | Playful clay was selected; the other studies are not the production default. |
| First native clay video failed to match the generated hero | Establish native silhouette, materials and lighting in a still before the full sequence. |
| Clay arrow was corrupted | One filled, rounded, extruded outline; inspect topology and partial reveal. |
| Lighting felt cheap / toy-like | Directional warm key, cool strip, restrained fill, deep shadows and crisp material definition. |
| Clean-arrow studio still was approved | Reuse its native camera, materials and light rig; animation was then explicitly authorized. |
| Scores intersected histories during motion | Raise the lift arc and check the entire crossing, not only endpoints. |
| Code was too small | 1.5× font size; preserve readability when adapting content. |
| Box sizes were inconsistent despite shared meshes | Duplicate full canonical assemblies, remove independent scale fitting, use local sculpture and check dimensions. |
| Ending returned to code and ran to 19 seconds | Remove that segment; end on the result, current export 15 seconds; creator controls final timing. |
| Larger code still sat too high | Implemented code-origin +100 px and orange-highlight +100 px, with a tighter blank gap before the loop. |
| TikTok headers still cover current content | Latest pending whole-foreground +100 px; no render requested or performed for this note. |
| One long animation makes editing difficult | Deliver N self-contained scene videos, numbered 1 through N, with consistent export settings and a scene manifest; no combined video by default. |
| Separate render locations delay feedback | Build and render directly in the episode/Short's Content HQ assets package, including previews and intermediate files. |

### Source map

| Source | Use / caution |
| --- | --- |
| [Current clay animation package](../shorts/short-06-data-layout/assets/blender-clay-animation/README.md) | Main reusable scene/components and corrected duplicates. Current media predates the latest pending placement correction. |
| [Current animation builder](../shorts/short-06-data-layout/assets/blender-clay-animation/build_animation.py) | Canonical duplication, larger code, motion/reveal and implemented gradient shift. Contains old workspace paths and auto-renders previews. |
| [Native studio still](../shorts/short-06-data-layout/assets/blender-clay-studio/retro-sunset-clay-studio.png) and [builder](../shorts/short-06-data-layout/assets/blender-clay-studio/build.py) | Approved light/material execution and original mesh construction. Its per-object fitting and global contour coordinates were superseded by the animation builder. Its old “video paused” README is historical. |
| [Generated clay hero](../shorts/short-06-data-layout/assets/retro-sunset-clay-hero/README.md) | Original art-direction reference, not exact geometry/counts or production pixels. |
| [Object studies](../shorts/short-06-data-layout/assets/retro-sunset-object-studies/README.md) | Alternatives and prompts; its “not selected” note predates the clay selection. |
| [Original 19-second clay package](../shorts/short-06-data-layout/assets/blender-clay-animation-original-19s/README.md) | Archive only; do not restore small code, inconsistent scales or code outro. |
| [Short 06 production log](../shorts/short-06-data-layout/log.md) | Dated evidence and superseding corrections. Contains earlier decisions that must be read in order. |

Keep this playbook focused on reusable decisions. Record future per-animation
data, dates, exports and measurements in that subject's log/package. Promote a
new standing rule here only when the creator selects it or evidence supports
changing the common system.
