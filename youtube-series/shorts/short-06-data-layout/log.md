# Short 06 handoff: data layout, benchmark, and the unresolved hook

September 5, 2026. Prepared for restarting the conversation in Claude.
This is an internal handoff, not an approved script. Append future developments
below rather than rewriting this account of the session.

## Read this first

We have a working C++ experiment with a substantial measured performance
difference. We have not landed a hook and script the creator wants to record.
The immediate failure is creative, not a failed benchmark or a published Short
with poor analytics. There is no audience test of this Short in these records.

The assistant spent too many rounds polishing diagrams, labels, and production
instructions while failing the main requirement: sell a provocative idea to a
cold viewer immediately. The latest rewrite made that problem worse by putting
abstract setup before the performance claim.

The creator's latest correction is the most important instruction for resuming:

> The golden rule of hooks is that every word matters, and the important words
> that carry the higher signal should be said before.

Do not interpret “short hook” as merely a low total word count. The first words
must already communicate something interesting. A sentence that becomes
interesting at its end still wastes the opening.

## Current state and where things live

- Content repository: `/Users/keremkazan/Documents/Projects/Content HQ`.
- This package: `youtube-series/shorts/short-06-data-layout/`. This is the
  existing Short 06 folder; scripts and production notes stay here.
- [script.md](script.md) contains the Round 10 rewrite, including the opening
  the creator just rejected. Canonical file does not mean approved copy.
- [Iteration index](iterations-2026-09-05/README.md): nine completed, checked
  rounds out of a requested twenty sequential revisions of this same idea.
- [Round 10](iterations-2026-09-05/round-10.md) was written and the canonical
  script replaced. Its final verification and completion record were not
  finished before feedback redirected the work. The index still says 9/20.
  Do not claim twenty rounds or a final audit are complete.
- [Chronological iteration log](../../../docs/logs/short-06-script-iterations-2026-09-05.md)
  and [evidence register](iterations-2026-09-05/evidence.md) preserve detail.
- Demonstration code: `aliases/01-screen-short-form` points to
  `/Users/keremkazan/code`.
- Runnable experiment: [data-layout](../../../aliases/01-screen-short-form/data-layout/LOOKUP-RESULTS.md).
- Camera snippets: [scene_1.cpp](../../../aliases/01-screen-short-form/short-06-data-layout/scenes/scene_1.cpp)
  and [scene_2.cpp](../../../aliases/01-screen-short-form/short-06-data-layout/scenes/scene_2.cpp).

This handoff does not revise the script, run more iterations, refresh analytics,
or approve recording or upload. Resume the creative discussion first.

## What we are demonstrating

A player has a score and fifteen historical scores. A loop only needs the
current scores for a selected set of player IDs.

When each score sits inside a full player record, successive scores are spaced
apart by the histories. Separating the scores into their own array substantially
improved the measured lookup batch. All player histories remain stored in a
separate array. We change storage layout, not the requested answer or data.

The camera-facing before:

```cpp
struct Player {
  int score;
  array<int, 15> history;
};

int total = 0;
for (int id : ids)
  total += players[id].score;
```

The camera-facing after:

```cpp
struct SplitPlayers {
  vector<int> scores;
  vector<array<int, 15>> histories;
};

int total = 0;
for (int id : ids)
  total += scores[id];
```

These are viewport fragments, not standalone programs. Setup and the binding
for `scores` stay off-screen. The tested experiment lives separately.

Two related tensions have informed the pitch:

1. A field the loop does not read can still affect its performance.
2. Keeping related fields together, a familiar design choice, can hurt this
   score-only workload.

The second can invite a real defense of maintainability and access to complete
objects. Neither warrants claiming all structs are slow or all related data
should always be separated.

## What the technical work established

We first built a sequential-scan comparison. Its normal optimized version
showed a large gain, but the packed layout also gained SIMD. A scalar control
existed. The creator did not want another demonstration dependent on disabling
compiler optimizations after the criticism of Short 5.

We therefore built an active-player ID lookup. Under normal `-O3`, inspection
of the actual linked binary found scalar loads and arithmetic on both sides,
without vectorization-disabling flags or pragmas. Both kernels use four scalar
accumulators. This is the experiment the current Short must show.

At 4,194,304 players and the same 1,048,576 active IDs:

| ID order | Object layout, repeat median | Split layout, repeat median | Ratio |
| --- | ---: | ---: | ---: |
| Ordered | 4.355233 ms | 0.347342 ms | 12.54x |
| Clustered | 4.867926 ms | 1.271375 ms | 3.83x |
| Shuffled | 4.612306 ms | 1.272952 ms | 3.62x |

The first ordered run gave 12.26x. The smallest workload changed little.
These are existing measurements, not new measurements taken for this handoff.
See [LOOKUP-RESULTS.md](../../../aliases/01-screen-short-form/data-layout/LOOKUP-RESULTS.md)
for protocol, validation, assembly, and raw-data links.

Essential boundaries:

- Same player data, active IDs, query order, additions, and result per comparison.
- Histories remain stored on both sides. No deleting data to make the test win.
- Timing covers lookup batches in existing data. Allocation, conversion,
  sorting, and validation are outside timing.
- The roughly 12.5x result belongs to the displayed ordered workload and size.
  It is not a universal layout speedup or a whole-game performance claim.
- Unequal SIMD does not explain this particular compiled comparison.
  Address generation and memory-system effects were not isolated. We collected
  no hardware counters, so do not call the result a measured cache-miss reduction.
- Do not put these timings over the earlier sequential-scan code.
- A follow-up reading scores plus complete histories for the same selected IDs
  has not been measured. Older full sequential scans do not answer that test.

Keep decisive conditions legible with the evidence. Do not turn the spoken
hook into a methodology disclaimer or narrate machine specifications.

## What we learned from Short 5 and want to carry forward

This evidence is about Instagram Short 5, not long-form retention or proof of
what YouTube and TikTok will do. The source is the
[final-media and retention analysis](../../analytics/reports/2026-09-02-short-05-instagram-retention-and-creative-analysis.md).

- The 19.77-second Reel reached 104,182 plays at the report's checkpoint.
  Its complete opening proposition took about 3.7 seconds. The screenshot
  suggests roughly a third of viewers left by four seconds; it explicitly
  shows 43% remaining at 19 seconds. Intermediate values are estimates.
- The middle paired code changes with speech, arrows, circles, emphasized
  captions, and hand gestures. Retention declined more gradually there.
- `Inefficient loop?` provided a compact text hook. Yellow captions with teal
  emphasis made important words stand out. Preserve the coordinated system;
  do not claim an isolated causal effect for a sticker or color.
- The measured result came before a genuine technical question and an
  immediate cut. There was no request to follow.
- A later Insights screenshot showed 155 profile visits, 74 follows,
  86 comments, 134 shares, and 286 saves. These are a later capture, not a
  perfectly synchronized funnel with the earlier play count. Follows divided
  by profile visits is not a proven profile-to-follow conversion rate.
- Compiler and optimization objections generated substantive discussion.
  The creator believes that disagreement helped drive the breakout and wants
  to design for that participation deliberately. The exact effect on ranking
  and distribution is not measured.

The creator explicitly rejected improving follower conversion by sacrificing
discussion and reach. The outro should preserve an interesting question and
make another concrete experiment feel worth returning for.

## The creative contract

The current [Short-form playbook](../../production/short-form-playbook.md) makes
the top priority explicit: a thought-provoking hook and a strongly opinionated,
controversial claim that evokes a reaction. Bland correctness is insufficient.

- Sell the idea within the first second. Put the concrete subject, stakes, or
  contradiction first. Basic words and short sentences; no abstract warm-up.
- Challenge a familiar engineering choice viewers might defend. Know the
  specific objection we expect, not merely “people might comment.”
- Deliberately omit broader nuance. We do not need to preempt every compiler,
  workload, architecture, or maintainability objection in twenty seconds.
  Keep the central claim correct and the experiment honest. Do not provoke
  by making deliberate mistakes or feigning ignorance.
- First-frame code/image, spoken hook, readable caption, curiosity callout,
  and red annotation must all reinforce one idea immediately.
- Preserve selective yellow/teal caption emphasis, meaningful arrows/circles,
  and hands or other interesting presenter movement throughout.
- Start delivering immediately, then provide the complete measured payoff
  before the ending. Do not pretend the winner is still hidden after showing
  both timings.
- End with a genuine adjacent question plus a specific next test, then cut.
  The useful framing is “That's what I'm testing next.” No follow/like CTA,
  withheld original answer, generic cliffhanger, or end card.
- Final export must be strictly below 20 seconds. An 18-19-second script target
  and word count are not runtime verification.
- Use `>` for narration. Keep code compact: 14 preferred / 17 maximum visible
  lines, short safe types, no unnecessary setup or qualifiers in camera snippets.
- No em dash, corporate language, forced lowercase, or canned AI cadence such
  as “It's not X, it's Y.” Do not add filler to sound conversational.
- Public titles, captions, descriptions, filenames, and hashtags require the
  [copy and SEO audit](../../production/platform-copy-playbook.md). Candidate
  keywords are not an approved publishing package. Do not use `#shorts`.

Follow current visual guidelines for layout rather than assuming Short 5's
historic webcam position is the current template. No render or upload gate
has been passed by this script exercise.

## How the script iterations lost their way

The initial hook was:

> This unused field is slowing your loop.

The body showed score spacing, moved histories to separate storage, revealed
the faster lookup, and asked whether reading histories too would change the
winner. The creator questioned whether scene 1 being slower than scene 2 was
clear enough. That concern was valid, but reviews became dominated by visual
bookkeeping.

Rounds 1-9 repaired example values, identity continuity, layout labels, spacing
brackets, caption timing, duplicated narration, result-to-question transitions,
and an incorrect implication of multiple history lanes. Those improvements
helped accuracy and production clarity. They did not establish a stronger hook
or prove cold-viewer interest. None was an audience experiment.

The creator repeatedly asked us to move faster. Excessive rereading, long
production instructions, archive verification, and minor changes made the
process slow without proportionate creative progress. A large iteration count
became a distraction from the main requirement.

When challenged about controversy, the assistant admitted the script had
become a neutral tutorial. The creator reinforced the top-priority rule and
asked for the script to be deleted and rewritten.

Round 10 did challenge a design choice, but opened with:

> Keeping related data together made this loop slower.

The creator rejected it strongly. “Keeping related data together made this”
spends six words before identifying the loop or performance cost. “Slower” is
word eight. We corrected the argument while worsening its delivery order.

### Latest chat proposal, not approved or written into script.md

The assistant then suggested:

> This struct is killing performance.
>
> We only need the scores. Why are we putting all this between them?

Proposed frame: the Player struct already visible, with `history` circled.
The creator has not accepted this replacement. Do not call it the winning
hook, assume the continuation works, or treat it as a completed rewrite.

### Current on-disk narration, preserved here as rejected working context

> Keeping related data together made this loop slower.
>
> It only reads scores, but they're buried between player histories.
>
> I'd store scores together and keep the histories separate.
>
> The same lookups ran over twelve times faster.
>
> Would you put them back together if we read both? That's what I'm testing next.

The full file includes a planned three-player diagram, preserved histories,
matching lookup code, scoped result card, and a separate final-question frame.
Those assets are directions, not evidence that viewers understand the edit.

## Why we have not succeeded yet

1. We optimized explanation before attention. A correct, tidy lesson does not
   automatically give a scrolling viewer a reason to stay.
2. We evaluated whole sentences instead of the first few words. The latest
   rejected hook withheld its useful information until the end.
3. We softened the stance during critique. We kept qualifying and clarifying
   instead of preserving the deliberate tension around a familiar choice.
4. We confused mechanical progress with creative progress. Label fixes and
   checked archives did not answer whether the premise was compelling.
5. We made the viewer carry too much setup: players, IDs, scores, histories,
   layout names, and benchmark conditions. These may belong in the proof,
   but need not all become prerequisites for understanding the opening.
6. We have no cold-viewer test or approved delivery. More revisions cannot
   justify claims of proven clarity, retention, or distribution success.

## Best way to resume

Start with the hook, not another full-script rewrite or benchmark rerun.
Offer one strongest opening with its exact first-frame visual. Explain briefly
which words carry the subject and consequence immediately and what belief it
challenges. Do not give a long menu of near-identical alternatives.

Judge whether the first few words alone sell something interesting. Then
check whether the next sentence visibly advances the demonstration rather than
rephrasing the hook. Preserve the useful technical work and invite a meaningful
counterargument at the end.

Once the creator accepts that opening, build one lean script around it. Keep
the proof scoped and the outro genuinely open. Do not declare success based on
word count, bookkeeping, or reaching twenty rounds. The unresolved job is an
opening and delivery the creator actually wants to record.

Do not change benchmark kernels or compiler controls to rescue a weak pitch.
Preserve unrelated work and do not modify `.clangd`, `.clang-format`, or
`.vscode/settings.json`. No publishing, new analytics, or new research is
required merely to resume this handoff.


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
