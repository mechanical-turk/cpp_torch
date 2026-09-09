# Short 06: The unused field slowing your C++ loop

MP4 filename: `cpp-data-layout-unused-fields-id-lookup-short-06.mp4`

Target runtime: 18-19 seconds. The timings below are edit targets, not a measured
runtime. This is a recording draft, not upload approval.

Revision rationale: [focused critique and evidence](../critique-2026-09-05.md).

## Script

### 00:00-00:02 | The unused field

Open on [scene_1.cpp](../../../../aliases/01-screen-short-form/short-06-data-layout/scenes/scene_1.cpp).
The player definition and score lookup are already visible. Circle `history`
in red and highlight `.score` so the viewer can see what the loop actually reads.

Callout: **Never read, still slower?**

The opening caption, callout, circle, and code must all be present on the first
frame. Emphasize **unused field** in yellow and **slowing** in teal. Point toward
the circled field as speech starts. No fade-in or silent setup.

> This unused field is slowing your loop.

### 00:02-00:05.5 | Show what the field does

Keep the loop in the same screen position. Replace only the player declaration
above it with a memory diagram: repeated records with a narrow blue score and
a broad grey history. Label one `score` and one `history`; do not make the viewer
read the same labels on every record.

The arrows land only on the selected scores. A red bracket identifies the
intervening history, while your hands spread to match the spacing. These are
stored values, not empty padding or source-level reads of the history.

> We only read scores, but the history spreads them across memory.

### 00:05.5-00:10 | Keep the data, change its layout

Bring the scores into one array and move the histories into a separate array.
Keep both arrays visible, with the histories still labeled. Compress the score
lane with your hands as the red arrow follows the change. Keep `for (int id : ids)`
fixed; change `players[id].score` to `scores[id]` at the same screen position.
The same IDs still identify the same players. Do not animate a sequential scan
over every score.

[scene_2.cpp](../../../../aliases/01-screen-short-form/short-06-data-layout/scenes/scene_2.cpp)
contains the matching code for this state. Use one continuous layout change,
not an animation followed by a second walkthrough of the same edit.

> Store the history separately, pack the scores together, and run the same lookups.

### 00:10-00:13.5 | The measured payoff

Show the `Before` time as the preceding sentence finishes. Reveal the `After`
time and the ratio on **twelve times faster**, within the next second. Circle
the lower time and point to it. These are recorded medians, not a live timer;
do not simulate waiting for the computation.

```text
1,048,576 ordered lookups
4,194,304 players
Normal -O3 · Both loops scalar

Median batch time
Before     4.36 ms
After      0.35 ms

~12.5x faster
```

Make the two times and ratio the primary reading, with the context above them
in readable lines. If it crowds the frame, remove decorative elements, not the
workload condition or font size. Use matching label alignment and a cohesive
teal accent for the faster result. Do not add bars or the full benchmark report.

> Twelve times faster here, without deleting any data.

### 00:13.5-00:19 | Ask whether the result survives

Keep the result visible and bring back the score/history lanes beneath it.
Bracket both lanes in red and point between them on **history too**. The next
test reads each selected player's score and complete history using the same
IDs. Do not reveal or imply a winner for that unmeasured workload.

Use two compact labeled lanes, not the full earlier diagram. Reserve their
space in the result-card composition so the outro does not shrink the numbers
or create a second full-screen reading task.

> Would this still win if we read the history too? That's what I'm testing next.

Cut immediately after **next**. No follow request, end card, or audio tail.

## Technical and editorial checks

- **Claim:** separating the score from each player's history speeds up this
  measured score-lookup workload. The history is unused by this loop, not
  useless to the application.
- **Belief challenged:** a field that the loop never reads cannot affect its
  performance.
- **Expected objections:** "The compiler already optimizes this," "You just
  enabled SIMD," and "Splitting the fields can hurt when you need both."
  The third is the main discussion we want. The visible optimization label
  heads off a repeat of the disabled-optimization misunderstanding; do not
  spend the spoken hook defending the benchmark.
- **Deliberate omissions:** cache hierarchy, address-generation details, formal
  AoS/SoA terminology, every input order, and a data-oriented-design lecture.
  The field-access tradeoff becomes the outro rather than a spoken disclaimer.
- **Conditions that stay visible:** the actual indexed lookup, retained
  histories, ordered IDs, dataset size, and normal `-O3`. Both layouts use the
  same IDs, values, additions, and result. Timing covers repeated lookups into
  existing storage, not conversion or allocation. Do not put a conversion
  animation under a running benchmark timer.
- **Evidence:** the [ID-lookup report](../../../../aliases/01-screen-short-form/data-layout/LOOKUP-RESULTS.md)
  and [repeat-run measurements](../../../../aliases/01-screen-short-form/data-layout/results/2026-09-05/lookup-repeat.json).
  The recorded medians are 4.355233 ms and 0.347342 ms, a 12.54x ratio. The first
  run measured 12.26x. Clustered and shuffled IDs produced roughly 3-4x gains,
  not 12x. Keep the headline tied to the displayed ordered case.
- **SIMD objection:** inspection of the linked binary found scalar loads and
  arithmetic in both kernels under normal `-O3`, without vectorization-disabling
  flags or pragmas. Both loops also use four scalar accumulators. This removes
  unequal SIMD as the explanation in this build; it does not isolate cache
  misses from address calculation or other memory-system effects. Do not say
  the CPU reads every history field or that we measured twelve times fewer
  cache misses.
- **Next test:** score-plus-history lookups using the same active IDs. The older
  sequential all-field scan is a different experiment and does not settle this
  question. The script proposes this follow-up; it is not a claim that it has
  been run or scheduled.

## Recording notes

- Camera scenes are viewport fragments, not standalone programs. The inputs
  are populated outside the shot; `scores` refers to the split score array.
  The tested implementations remain in
  [lookup.cpp](../../../../aliases/01-screen-short-form/data-layout/lookup.cpp).
  Both scenes fit in eight lines and preserve the actual lookup expressions.
- In the memory diagram, retain every player's score and history with the same
  ID. Pack **all scores**, not just the selected scores. For example, highlight
  IDs 0 and 2 before and after, while leaving ID 1 visibly present. Do not imply
  that changing layout also sorts queries, renumbers players, or deletes data.
  This is a schematic storage diagram, not a cache-line or measured-traffic
  diagram. Keep the score cells legible instead of forcing a literal byte scale.
- Follow the current [visual layout](../../../production/visual-asset-guidelines.md):
  `2160 x 3840` master, webcam above the lower code/visual region. Keep essential
  content away from platform controls. Visuals described here still need to be
  made and checked at phone size.
- Keep captions short with selective yellow/teal emphasis. Update the circle,
  arrow, or bracket as the explanation changes. Hand movement must continue
  through the edit, result, and question, not stop after the opening.
- Use one visual language from the first frame through the final question.
  The benchmark card must not permanently erase the histories we refer to in
  the outro. No secondary slogan, new acronym lesson, sound-effect interlude,
  or extra comparison belongs between the edit and its payoff.
- Record a dry read. If it runs long, shorten pauses and transitions before
  rushing the words or deleting the engagement question. Verify the final
  export is below 20.000 seconds with `ffprobe`. If the read naturally finishes
  sooner than the target, cut sooner; never stretch it to fill the timestamps.
- Use the existing dated measurements for the result graphic, or rerun the
  lookup experiment and update the card and spoken ratio together. Never mix
  the old sequential-scan timings with this ID-lookup code.
- All four [upload-gate checks](../../../../docs/operations/short-upload-gate.md)
  remain **UNVERIFIED** until the final export is reviewed.
- Working search language: C++ performance, data layout, hot/cold splitting,
  score lookup. This file is not a platform publishing package. Research each
  platform's title, description, and hashtags before approving `publishing.md`.

