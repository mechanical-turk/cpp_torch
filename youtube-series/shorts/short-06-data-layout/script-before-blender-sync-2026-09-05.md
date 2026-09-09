# Short 06: Keeping related data together slowed this C++ loop

MP4 filename: `cpp-data-layout-related-fields-performance-short-06.mp4`

Target: 18-19 seconds; final duration unverified.
Revision **10 / 20**. [Critique](iterations-2026-09-05/round-10.md) ·
[Iteration index](iterations-2026-09-05/README.md)

## Creative decision

- **Position:** I would split these player records for the score-only lookup.
  Keeping related fields together made this measured loop substantially slower.
- **Belief challenged:** a player's related fields belong together in memory.
- **Intended reaction:** disbelief at a familiar design losing, or an urge to
  defend keeping the fields together for maintainability and other workloads.
- **Expected objection:** “Of course separating scores helps that one loop.
  What happens when you actually need the whole player?”
- **Deliberate omissions:** an AoS/SoA lecture, cache hierarchy, every workload,
  and arguments about overall application architecture. The opposing access
  pattern becomes the ending. Do not pretend that structs are inherently slow.

## Script

### 00:00-00:02.5 | Challenge the familiar choice

> Keeping related data together made this loop slower.

First frame: [scene_1.cpp](../../../aliases/01-screen-short-form/short-06-data-layout/scenes/scene_1.cpp)
shows the Player definition and actual score lookup. Use one red bracket to
group `score` and `history` inside the struct. Quietly highlight `.score` in
blue. Face and pointing hand are already visible.

Full opening caption, present immediately:

```text
Keeping related data together
made this loop slower
```

Emphasize **related data together** in yellow and **slower** in teal.
Smaller callout beside the declaration: **Keep fields together?**
The caption is the main read; the code shows exactly which grouping we mean.
No fade-in, greeting, or qualifying preface.

### 00:02.5-00:06 | Show the cost of that choice

> It only reads scores, but they're buried between player histories.

Keep the lookup in place. Replace the declaration with three player records:
`[7 | history] [2 | history] [9 | history]`. Label the state **By player**.

On **reads scores**, pulse 7 and 9 and retain their outlines. On **between
player histories**, bracket their separation and spread your hands. The grey
history blocks are real stored data. Do not animate reads through them.

### 00:06-00:10 | Take a position and change it

> I'd store scores together and keep the histories separate.

Bring all three blue score cells into one lane and all three grey history
blocks into another. Keep every value and the same player order. Change the
state label to **By field**; label the lanes `scores` and `history`.

Compress the score lane with your hands. Keep `for (int id : ids)` fixed;
change `players[id].score` to `scores[id]`, matching
[scene_2.cpp](../../../aliases/01-screen-short-form/short-06-data-layout/scenes/scene_2.cpp).
A red arrow connects the packed score lane to the new lookup expression.
Finish the move with the sentence; no second walkthrough.

### 00:10-00:13.5 | Prove the choice

> The same lookups ran over twelve times faster.

Show both timing rows and their conditions on **The same lookups**.
Reveal the ratio on **over twelve times faster**; point and circle the lower
time. Use the same layout names as the demonstration.

```text
Score-only lookups
~12.5x faster

Median batch time
By player    4.36 ms
By field     0.35 ms

~1.05M ordered IDs
~4.19M players
Normal -O3 · Both scalar
```

The ratio leads; the aligned rows support it. Keep conditions readable.
Use teal on both the faster result's frame and text. These are recorded
medians, not a live timer or a universal speedup.

### 00:13.5-00:19 | Invite the counterargument

> Would you put them back together if we read both? That's what I'm testing next.

As the question starts, replace the entire result card with the familiar
split lanes. Remove all timing, ratio, and winner styling together.

Main text: **Would you put them back together?**
Smaller label: **Next test: read both fields**

On **read both**, outline the histories belonging to the selected scores 7
and 9. Point between those scores and histories. Leave the middle player's
data visible but unselected. The question asks whether to reverse the design
choice; do not animate a reversal or imply a new measured winner.

Cut immediately after **next**. No follow request or end card.

## Director checklist

- Use the [current vertical layout](../../production/visual-asset-guidelines.md):
  `2160 x 3840`, webcam above the code/visual region. Keep captions clear of
  the face and hands, and essential content clear of platform controls.
- Hold the complete opening caption through its sentence. Then use short
  synchronized captions with selective yellow/teal emphasis and an outline.
  Do not stack an automatic caption over the held hook.
- Keep one purposeful red annotation per beat and meaningful hand movement
  through the explanation, edit, result, and question. Preserve code legibility.
- Reuse the same score and history shapes throughout. History blocks are wider
  than score cells but not drawn to literal byte scale. Never resize the blocks
  during the transformation or crop data to fit the frame.
- Internal example: IDs 0 and 2 select scores 7 and 9, sum 16, before and after.
  Keep unselected score 2 and all three fifteen-value histories. IDs and H0/H1/H2
  labels stay off-screen; selection uses extra outlines, not color alone.
- The spacing bracket runs from the right edge of 7 to the left edge of 9.
  Before it spans history 0, score 2, and history 1; afterward only score 2.
  It illustrates separation, not bytes fetched, cache misses, or timing.
- There is one separate histories array. Pack all scores, not only selected
  ones. Preserve IDs, order, values, and additions. The final question adds
  the complete histories for the same selected players, not an all-player scan.
- Camera scenes are eight-line viewport fragments. Setup stays off-screen;
  `scores` names the split score array. Diagrams show vector data buffers.
- Keep the full scoped measurement visible through the result sentence; remove
  it completely for the unmeasured question. No fake timer over conversion,
  second read animation, filler pause, or delayed answer to the current claim.
- Timecodes are edit targets. Record naturally and cut sooner if the read ends
  sooner. Measure the actual export with `ffprobe`; it must be below 20 seconds.
  All [upload-gate checks](../../../docs/operations/short-upload-gate.md) remain
  **UNVERIFIED** until final-media review.

## Technical and editorial checks

- [Benchmark evidence](../../../aliases/01-screen-short-form/data-layout/LOOKUP-RESULTS.md)
  and [repeat-run data](../../../aliases/01-screen-short-form/data-layout/results/2026-09-05/lookup-repeat.json):
  1,048,576 ordered active IDs among 4,194,304 players. Repeat medians
  4.355233 ms versus 0.347342 ms give 12.54x; the first run gave 12.26x.
  Clustered and shuffled queries gained roughly 3-4x. Keep the claim scoped.
- The measured object holds one four-byte score and fifteen historical scores.
  Both layouts retain all histories. Timing excludes allocation, conversion,
  sorting, and validation; it measures the same lookup batch in existing data.
- Both linked kernels use scalar loads and four scalar accumulators under
  normal `-O3`, without vectorization-disabling flags or pragmas. Unequal SIMD
  is not the explanation here. Address generation and memory-system effects
  were not isolated; do not claim a measured cache-miss reduction.
- “Related data together” refers to the score and history grouped by player in
  the displayed code. It is not a general claim that all related data should be
  separated, that structs cannot be fast, or that this is a whole-game benchmark.
- The score-plus-history ID lookup is a proposed next test, not a completed
  measurement or a scheduled release. Older sequential all-field scans do not
  settle it. Preserve the open design question rather than inventing its answer.
- Candidate search language: C++ performance, data layout, structure of arrays,
  player data, hot/cold splitting. Platform copy still needs its own keyword
  research. This script is not SEO or upload approval.
