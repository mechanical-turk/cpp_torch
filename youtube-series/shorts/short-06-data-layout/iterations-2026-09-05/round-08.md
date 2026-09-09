# Round 08: make the script usable while recording

Input: [Round 07](round-07.md).
Input canonical SHA-256:
`f96baa2d30c2aa873c4d2d167602e1172a6266e62f6a6e358e02e44e338d2665`.

Previous turn: progress; Round 07 produced the current complete revision.
The interruption added no work and left no running command to resume.

## Critique and lesson

1. The spoken lines are buried beneath long paragraphs of directions. Put each
   spoken beat first, followed by its essential synchronized actions.
2. Identity, scope, and animation warnings repeat across scenes and recording
   notes. Consolidate them into one director checklist; retain the constraints.
3. The production plan is harder to execute than the 50-word lesson requires.
   Keep one transformation, one result card, and one question state. Remove
   repeated explanations of those same instructions.

Apply R06's uninterrupted flow and R07's distinct answer/question states.
[E1](evidence.md) supports coordinated speech and visuals as a working pattern,
not the causal effect of this reorganization. Existing playbook rules cover
the repair. The user's request to speed up also calls for leaner review records.

## Rewritten script

The complete revised spoken/visual core follows. Technical evidence remains
in the canonical script; narration, measurements, and data are unchanged.

### 00:00-00:02 | The unused field

> This unused field is slowing your loop.

First frame: [scene_1.cpp](../../../../aliases/01-screen-short-form/short-06-data-layout/scenes/scene_1.cpp),
face, a ready downward-pointing gesture, and a red circle around `history`.
Keep its letters clear and `.score` quietly highlighted in blue.

Show the complete caption immediately and hold it through the hook:

```text
This unused field
is slowing your loop
```

Emphasize **unused field** in yellow and **slowing** in teal. The smaller
callout above the code reads **Unused here, still slower?** The full caption
is the main read; the circle and code support it. No fade-in or silent setup.

### 00:02-00:05.5 | Show the spacing

> We're only adding scores, but histories sit between them in memory.

Keep the lookup fixed. Transform the declaration directly into three records:
blue scores 7, 2, 9, each followed by a grey history block. Remove the opening
callout. Label the diagram `Scores apart` and `Memory layout example`.

On **adding scores**, pulse 7 then 9, point, and retain their selection outlines.
On **histories**, bracket the gap between those selected scores and spread
your hands. The grey blocks contain stored history, not empty space.

### 00:05.5-00:10 | Change the layout

> Store the histories separately and pack the scores together.

Move every history block into its own lane while all three scores pack
together. Preserve their order, dimensions, and selection outlines. Label
the lanes `scores` and `history`; change the state label to `Scores packed`.

Keep `for (int id : ids)` fixed. Change `players[id].score` to `scores[id]`
as the scores move together, matching
[scene_2.cpp](../../../../aliases/01-screen-short-form/short-06-data-layout/scenes/scene_2.cpp).
Compress the score lane with your hands. The spacing bracket contracts with it.

By **scores together**, finish the edit and replace the bracket with a red
arrow from the packed scores to `scores[id]`. Keep that view through the phrase.
No second read animation or walkthrough.

### 00:10-00:13.5 | Deliver the result

> The same lookups ran over twelve times faster.

On **The same lookups**, replace the diagram with both measured timing rows
and their conditions. On **over twelve times faster**, reveal the ratio,
circle the packed time, and point. Keep the whole card through **faster**.

```text
Score-only lookups
~12.5x faster

Median batch time
Scores apart     4.36 ms
Scores packed    0.35 ms

~1.05M ordered IDs
~4.19M players
Normal -O3 · Both scalar
```

The ratio is the main read; align the supporting rows and keep the footer
legible. Use teal for the packed result's frame and text. These are recorded
batch medians, not a live timer. The rows already reveal the winner; the ratio
adds emphasis, not another cliffhanger.

### 00:13.5-00:19 | Open the next question

> Would this still win if we read the history too? That's what I'm testing next.

On **Would this still win**, replace the entire result card with the familiar
packed-score and history lanes. Remove its ratio, times, footer, and winner
marker together. Main text: **Still faster with both?** in white, with a smaller
`Next test` label. Keep the selected scores outlined.

On **history too**, outline only their corresponding first and third history
blocks; point to them with your hand and a red annotation. Keep the middle
score and history visible but unselected. Hold this question state through
the final sentence and cut immediately after **next**.

## Director checklist

### Layout and captions

- Use the current [visual layout](../../../production/visual-asset-guidelines.md):
  a `2160 x 3840` master, webcam above the lower code/visual region. Keep
  essential content inside platform-safe areas and verify it at phone size.
- Reserve a caption band in the webcam region, clear of eyes, mouth, and hands.
  The smaller opening callout has its own slot above the code. Removing it
  must not move the lookup. Do not shrink the code to accommodate more text.
- After the held opening sentence, use short synchronized captions with
  selective yellow/teal emphasis and a high-contrast outline. Never stack
  automatic captions over the held hook. Maintain eye contact and purposeful
  hand movement throughout.
- Use one dominant red marker per beat, with a clear target. Do not cover
  characters, introduce decorative transitions, or add extra comparisons.

### Data and geometry

Internal construction map, not on-screen ASCII:

```text
Selected IDs: 0, 2
Before: [7 | H0] [2 | H1] [9 | H2]
After:
scores    [7] [2] [9]
histories [H0][H1][H2]
```

- Each H block represents that player's complete fifteen-number history.
  Keep all three scores and histories, the same IDs, query order, and selected
  sum of 16. Pack all scores, not only 7 and 9. Do not narrate the arithmetic.
- Show score values, one history label before the edit, and lane labels after.
  Keep IDs, H0/H1/H2, and selection legends off-screen. Mark selection with
  extra outlines, not color alone.
- Use one fixed blue score-cell template and a wider fixed grey history-block
  template. Preserve dimensions through the move. The schematic is not a
  literal fifteen-to-one byte scale; neither arrangement may crop its data.
- The bracket runs from the right edge of 7 to the left edge of 9. Before,
  it spans H0, score 2, and H1; afterward it spans only score 2. Do not mark
  score 2 as history. This shows spacing, not fetched bytes or cache misses.
- Pulse only the selected scores in the first layout. Retain their outlines
  afterward; do not animate faster reads or sweep through unselected data.
- The final question adds outlines only to H0 and H2. H1 remains stored and
  unselected. There is no measured result or predicted winner for that test.
- Camera scenes are eight-line viewport fragments, not standalone programs.
  Setup stays off-screen; `scores` is the split score array. The diagram
  depicts vector data buffers, not the control fields inside `SplitPlayers`.

### Edit checks

- Keep every numerical claim beside its scope and conditions for its entire
  display. Remove them together when the new question replaces the result.
- Animate storage reorganization before showing timings. Allocation and
  conversion are outside the measured workload. Do not put a timer over them.
- Cue changes from the spoken phrases, not pauses added to meet the provisional
  timecodes. Record a dry read; never pad a shorter delivery or rush words to
  complete unnecessary animation.
- No follow request, extra lesson, end card, or audio tail. The final export
  must be below 20.000 seconds, measured with `ffprobe`.
- All four [upload-gate checks](../../../../docs/operations/short-upload-gate.md)
  remain **UNVERIFIED** until the exact final media is reviewed.

## Second look

The recording sequence should now be scannable without losing the director's
accuracy constraints. This is a production-readability improvement, not a new
audience experiment. Actual animation timing and phone-size clarity remain
unverified. Next, reassess the premise as a cold viewer rather than adding
more production instructions.

## Verification

- Canonical output SHA-256: `98a3d036ec6240d30ce532c0dd0380a6124b7e6158ea84d1c24af5705df351f5`.
- File shortened from approximately 2,800 to 1,486 whitespace-separated words;
  all five spoken beats remain unchanged at 50 words.
- Complete revised core archived; links, prior archive integrity, measurements,
  and benchmark-source hashes checked. No media or benchmark was generated.
- Progress: 8/20. Final-media checks and the remaining twelve rounds are open.
