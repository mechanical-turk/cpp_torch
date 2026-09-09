# Short 06 animation production log

## September 5, 2026: Blender mechanical-assembly animation built

After the creator accepted “This struct is killing performance.” as the hook,
they approved a mechanical 3D assembly concept and asked for it to be built.
Created `assets/blender-mechanical-assembly/` with an editable Blender 5.1.2
scene, packed fonts, timeline cues, reproducible scripts, a native 2160 x 2352
animation, a smaller preview, six full-resolution stills, a storyboard, and an
original snap sound stem. The native and preview exports were measured at
19.000 seconds, 456 frames, 24 fps. They are lower-screen assets for placement
at y=1488 in the existing 2160 x 3840 presenter composition.

The sequence shows three player records, highlights scores 7 and 9, marks
their separation, extracts all three scores, retains all 45 history plates,
shows the existing ordered-lookup evidence, then connects the selected scores
to their corresponding histories for the unmeasured next-test question.
All 456 scene frames were checked for preservation, ordering, static-hold
equality, model/code separation, and result/question visibility. Six key states
and an extraction frame were visually inspected. See the package README and
scene audit for exact boundaries and recording cues.

No narrator or presenter has been recorded for this animation package. The
existing rejected Round 10 script and 9/20 iteration index were preserved;
this is animation production following the later creative discussion, not
completion of that earlier revision loop. No benchmark was rerun or changed.


## September 5, 2026: simplified Blender render replaces the initial treatment

The creator requested removal of titles, captions, banners, narration, and
nonessential result copy; a fresh composition with syntax-highlighted code;
better white-on-blue contrast; consistent treatment of the center score; and
explicit score labels on the physical models.

The current animation package is now `assets/blender-clean/`. The earlier
`assets/blender-mechanical-assembly/` package is retained as the previous version.
The revised scene contains larger/deeper models, syntax-highlighted Player
and SplitPlayers snippets, three score labels, three history labels, and only
4.36 ms → 0.35 ms plus 12.5x faster during the result. All query-subset outlines,
connection lines, titles, captions, banners, and audio have been removed.
All three scores receive the same treatment; all 45 history plates remain.
Dark matte score-face insets prevent stage lighting from washing out the white
labels and numerals. Native-render pixel probes were identical RGB (29, 60, 91)
across all three face samples.

Verified all 456 scene frames for state preservation, code/model separation,
content restrictions, syntax materials, and static holds. Inspected the new
assembly, extraction, final arrays, and minimal-result frames. Both encoded
videos are 19.000 seconds, 24 fps, with video only; the native export is
2160 x 2352 and the viewing copy is 720 x 784. The native video decoded without
errors. Source benchmark, existing scripts, and prior iteration counts were
not changed. Exact evidence remains in the package notes and original report.


## September 5, 2026: canonical narration synchronized to the clean animation

At the creator's request, replaced script.md with a six-beat spoken script
matched to the existing clean animation. The recommended new opening is
“This struct wrecks performance.” The subject and consequence arrive in four
words. The extraction, retained histories, payoff, and next-test question align
with the rendered transitions at approximately 6.92, 10.04, 12, and 15 seconds.
The presenter supplies the gestures; removed render overlays and selective
highlights are not reintroduced. The animation remains silent and unchanged.

Preserved the prior canonical script as script-before-blender-sync-2026-09-05.md.
Checked narration formatting, local links, and timing alignment against the
render metadata. The recorded delivery and complete export duration remain
unverified; the existing 19.000-second animation duration is verified. This
update does not complete the earlier 20-round iteration request or change its
9/20 record. No new benchmark, render, platform copy, or publication occurred.


## September 5, 2026 — wider clean Blender derivative

At the creator's request, regenerated the clean animation at 2360 × 2352,
adding exactly 100 pixels on each side. The original models, code, materials,
lighting and animation remain unchanged. Adjusted the orthographic camera
span to preserve the original pixel scale and continue the actual studio
background. Verified 250,368 projected points across 456 timeline frames;
maximum deviation from the expected 100-pixel horizontal shift was below
0.001 pixels. Six native key-frame crop comparisons have mean RGB differences
below one code value per channel from rendering at the new width.

Rendered 111 distinct native frames and reused only previously verified
static holds. Both the 2360 × 2352 native MP4 and 1180 × 1176 preview decode
without errors: 24 fps, 456 frames, 19.000 seconds, one video stream and no
audio. Saved the video, updated editable scene, stills and verification in
assets/blender-clean-wide. Original assets/blender-clean is preserved.
This is a wider derivative for placement, not a new vertical-master standard.
No benchmark, script, voice recording or publication was changed.


## September 6, 2026 — lower placement and animated code/results

At the creator's request, retained the 2360 × 2352 canvas and shifted the
existing composition down 200 pixels using the orthographic camera. All-frame
foreground bounds are approximately x = 252–2064 and y = 391–2102.
Replaced the immediate code cut with staggered line slides/flips and brief
mint underlines on the changed declarations and lookup. Syntax highlighting
and stable unchanged lines remain. Rebuilt the timing comparison with bold
coral/mint values, smaller units, an arrow draw and traveling accent, followed
by value/ratio settling motions. Both timing values and the arrow share the
measured optical center y = 510. No extra text, banners or audio were added.

Rendered the revised upper 1100 pixels at native resolution for 166 distinct
scene states. Reused the unchanged native model frames below that partition,
translated by exactly 200 pixels with no resizing. Compared both regions
against three full-scene reference renders; mean RGB differences are below
two code values per channel. The model geometry, lighting, 45 history plates
and all score labels remain. All 456 frames were checked for foreground bounds.

Native MP4 is 2360 × 2352; preview is 1180 × 1176. Both decode without errors
at 24 fps for 19.000 seconds, with 456 frames and no audio stream. Saved video,
editable scene, stills, scripts and verification in assets/blender-motion.
Earlier versions are preserved. Actual platform composer safety remains
unverified; this change implements the creator's requested pixel placement.
No script, benchmark, voice recording, platform copy or publication changed.


## September 6, 2026 — Retro Sunset selected; object form studies

The creator selected Retro Sunset as the theme going forward: dark burgundy
to peach background, golden scores with dark amber faces, and cobalt histories
with navy label faces. Generated three still-image form studies: soft enamel,
precision hardware, and playful soft-touch. Saved samples and exact prompts
in assets/retro-sunset-object-studies. These are ImageGen design concepts;
generated card counts are illustrative and must be corrected to fifteen per
player in a native Blender implementation. Object style is not selected yet.
The approved composition, editable animation, video and benchmark are unchanged.


## September 6, 2026 — clay direction selected and hero sample

The creator committed to the playful clay look within Retro Sunset. Generated
a final result-screen hero sample with refined clay materials, warm/cool
lighting, contact shadows and a rounded clay arrow. Saved image and prompt in
assets/retro-sunset-clay-hero. This is a visual-direction sample; exact card
counts and composition must be enforced in native Blender. No video or scene
was regenerated for this sample request.


## September 6, 2026 — native clay still rebuilt; video paused

The creator rejected the first native clay adaptation because its geometry,
lighting and materials did not resemble the selected generated hero. Video
work is explicitly paused. Rebuilt a fresh single-frame Cycles scene against
the hero: deeper continuous gold shells, recessed amber faces, taller navy
cradles, front history plaques, a perspective camera, clay surface variation,
soft studio lighting, and a textured burgundy-to-peach ground.

Saved the 2360 × 2352 native PNG, editable scene with packed fonts, construction
script and verification in assets/blender-clay-still. Rendered with 192 maximum
samples and denoising. Inspected the exported image and verified three score
labels, three history labels, all three values and exactly 45 history cards.
A Metal shader-compiler crash on the first full-size attempt was resolved by
disabling Metal kernel optimization and MetalRT for the successful render.

This is a new native still for creator review, not a claim of a pixel-identical
copy or an approved replacement animation. The reference image is not used as
an image plate or texture. No video was rendered or replaced, and no script,
benchmark, audio or publication changed.


## September 6, 2026 — clean arrow and stronger studio lighting

The creator called the native clay still nearly perfect and requested a clean
arrow plus sharper, more vibrant, high-contrast studio lighting. Rebuilt the
arrow as one rounded, filled outline with depth. Inspected an enlarged native
render and verified one closed component with zero non-manifold edges.

Replaced the broad lighting with a directional warm rectangular key, a cool
edge strip and restrained front fill. Reduced ambient illumination and refined
material roughness for clearer highlights, while retaining the clay surface
texture. Rendered a new 2360 × 2352 still with 256 maximum Cycles samples,
adaptive threshold 0.004, denoising and a one-pixel reconstruction filter.

Saved the PNG, packed editable scene, source and checks in
assets/blender-clay-studio. Verified zero movement in all model bounds against
the prior clay still, all six field labels, and 45 history cards. Reviewed the
full-size export. This supersedes the previous still for the current review;
the previous version is preserved. Video generation remains paused.


## September 6, 2026 — clay studio look approved; animation authorized

The creator explicitly approved the clean-arrow, stronger-studio-lighting
still and authorized the full video animation. The approved native look is
assets/blender-clay-studio/retro-sunset-clay-studio.png and its editable scene.
Animation production is underway using that scene as the base, retaining the
19-second timing, visible code transition, score extraction, retained histories
and minimal result. This entry records approval and work in progress; export
completion will be recorded separately after rendering and verification.


## September 6, 2026 — approved clay animation rendered and verified

Completed the authorized full Blender sequence using the approved native clay
studio scene. Saved the 2360 × 2352, 24 fps, 456-frame, 19-second silent MP4,
viewing preview, packed editable Blender scene, seven native stills, source
scripts and verification records in assets/blender-clay-animation.

The sequence retains the safe placement and Retro Sunset lighting/materials:
three interleaved score/history pairs, visible staggered code changes, the
scores lifting and gathering into a dense row, retained history trays, a small
landing bounce, and the minimal timing result with a clean arrow reveal.
Raised the score flight path and checked the crossing segment for clearance.
Verified all six field labels and exactly 45 history cards, frame bounds, final
pose, export resolution, duration, frame count and silent audio state. Both
MP4s decoded completely without errors. Inspected native transition, gathering,
arrow-reveal, result and final-code stills.

Moving model frames are native-resolution Cycles renders with 32 maximum
samples and denoising; a native comparison against 96 samples measured mean
RGB difference 0.596/255, with the 99th percentile at 3/255. Static holds reuse
identical scene states. The settled model and result holds retain the approved
256-sample still pixels; the assembled result PNG matches that approved PNG
exactly before video compression. No motion frames were interpolated.

This completes the animation asset authorized after still approval. It does
not record approval of the new video or a platform release. Previous versions
are preserved. Script, benchmark, narration and publication state are unchanged.


## September 6, 2026 — larger code, canonical objects and shorter ending requested

The creator requested a 1.5× code font, then an additional 100-pixel downward
placement and a matching downward move of the orange background highlight.
Reflowed the code with a smaller blank gap before the loop to retain separation
from the histories. Final geometry audit places the visible HUD bounds at
approximately x=255–2043, y=348–1037 on the unchanged 2360 × 2352 canvas.
The gradient's material center moves from y=1818.61 to y=1918.61.

The creator also identified inconsistent box sizes. Replaced the per-object
screen-size corrections with complete duplicates of the central score and
history assemblies, linked mesh data, local sculpture coordinates, and one
shared scale animation per family. Checked matching world dimensions at key
poses and common scale/depth on every frame, plus score/history clearance.
The sequence now ends at frame 360 on the benchmark result: 15 seconds at
24 fps, with no return-to-code objects or appended duration.

The creator explicitly authorized the entire render using these final
revisions. Full-resolution Cycles rendering is underway; completion and the
updated Content HQ final render will be recorded after export verification.


## September 6, 2026 — final requested clay revision rendered and installed

Completed the explicitly authorized full render with the 1.5× code font,
lowered text placement and orange gradient highlight, uniform canonical
score/history duplicates, and benchmark-only ending. The native MP4 is
2360 × 2352 at 24 fps: 360 frames, 15 seconds, silent. The final frame retains
the complete timing comparison and speedup; the return-to-code segment is gone.

Inspected the native opening, phone-size code readability, transition and final
result renders. Verified all-frame composition and matching family transforms,
world dimensions at key poses, retained field labels and 45 cards, and clearance
through the score/history crossing. Both native and preview MP4s decode fully
without errors and have the expected resolution, frame count and duration.

Installed the complete revised package at assets/blender-clay-animation,
including the final MP4, preview, editable packed Blender scene, six native
stills, sources and verification records. Compared copied file hashes.
Preserved the prior 19-second package at
assets/blender-clay-animation-original-19s. Workspace originals also remain.

This records animation-asset completion, not publication or release approval.
Script, benchmark, narration and publication state are unchanged.


## September 6, 2026 — TikTok header overlap noted; animations playbook created

The creator reports that TikTok headers cover the current animation content and
requests another 100-pixel downward shift of the whole foreground. This is
relative to the latest 15-second render, not another code-only shift. The canvas
and scale should remain unchanged; preserve text/background contrast and recheck
bottom and platform-interface clearance when applying the change. The earlier
local bounds audit did not establish actual TikTok header clearance.

The creator explicitly requested a note only, with no rerender. The new offset
is pending: the current Blender scene, scripts, PNGs and MP4s retain the prior
placement. Added a prominent pending-correction note to the asset README.

Created youtube-series/production/animations-playbook.md to preserve the full
selected animation system: Retro Sunset clay, canonical duplicate assemblies,
scene collections, geometry sources, material/color settings, studio lights and
camera, typography, code transitions, clean arrow construction/reveal, minimal
results, motion grammar, ending/duration choices, rendering/cache settings,
verification, Content HQ handoff and the decisions/failures that led to them.
It distinguishes reusable defaults from Short 06 data and measured parameters,
and distinguishes implemented changes from the latest pending correction.

Added the playbook to AGENTS.md routing and linked it from the visual guidelines
so future Blender tasks load it before reusing the native reference assets.
No video, still, scene, rendering source, benchmark, script or publication changed.
