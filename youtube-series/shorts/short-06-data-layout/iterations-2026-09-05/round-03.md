# Round 03: make the measured winner easy to identify

Input: [Round 02](round-02.md), reread alongside the canonical `script.md`.
Input canonical SHA-256:
`91187933e28e49a07ad9e961bb1ec16eac62b21ce39f49099a42452f31cea4d1`.
Use [E1, E3, and E5](evidence.md) for the payoff, measurement, and clarity checks.
The previous turn made verified progress: its rewrite and archive match, and
the canonical hash still matches Round 02's recorded output.

## Critique of the input

1. **The result labels rely on memory.** `Before` and `After` tell viewers when
   a version appeared, not what distinguishes it. Repair: introduce `Scores
   apart` and `Scores packed` with the corresponding diagrams, then reuse those
   exact labels beside the times. E5 is direct feedback that scene-to-winner
   mapping needs attention; it is not a measured audience failure rate.
2. **Exact eight-digit counts draw unnecessary reading effort.** The large
   dataset and ordered subset matter, but their full decimal expansion does
   not help a viewer understand the result. Repair: show `~1.05M ordered IDs`
   and `~4.19M players`, with the approximation explicit. Preserve exact counts
   in the technical notes and source evidence. Do not remove order or scale.
3. **The planned hierarchy gives three things equal priority.** Two times and
   a ratio are all called primary, while the metadata occupies the first
   lines. Repair: make the speedup the main read, the two labeled times its
   supporting evidence, and the shared conditions a stable readable footer.
   E1 identifies small benchmark text as a risk worth testing. It does not
   establish that this proposed hierarchy will increase retention.
4. **The outro adds a diagram to an already full card.** Reserving unspecified
   space does not resolve the reading load. A persistent ratio beside a new
   all-field question can also look like a result for that unmeasured test.
   Repair: replace the two timing rows and their heading with the two familiar
   lanes under `Next test: read both?`. Keep the ratio explicitly labeled
   `Score-only lookups`. Reuse the same footprint without shrinking the text
   or assigning a winner to the next workload.
5. **The payoff sentence leaves the layout-to-result connection implicit.**
   `The same lookups run twelve times faster here` identifies the workload but
   not the change that delivered the win. Repair: name packing the scores in
   the sentence and retain the scoped comparison. Use `over twelve times` for
   the measured 12.54x ratio. This adds a few useful words without turning the
   reveal into a methods explanation or a claim about measured cache misses.

Decision: **rework the result sequence, preserve the opening and experiment**.
Carry R02 forward by reducing interpretation effort, not just shortening text.

## Lesson applied

R03: give the result the same semantic labels as the demonstration. Separate
the verdict, supporting measurements, and conditions visually. When the next
question enters, replace an already-read element rather than stacking another
task on top, and keep the measured claim's scope explicit. Existing visual
hierarchy, fair-task, and complete-payoff rules cover this lesson.

## Rewritten script

Proposed MP4: `cpp-data-layout-unused-fields-id-lookup-short-06.mp4`.
Target: 18-19 seconds, final runtime unverified. The [shared contract](evidence.md)
and canonical technical notes remain in force.

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
above it with three adjacent player records. Remove the opening curiosity
callout now; the captions continue. Label this state `Scores apart`, with
`Memory layout example` as its smaller descriptor. The concrete values and
selected IDs are specified below, but do not put the ID row or H0/H1/H2
identifiers on screen.

On **adding scores**, point to 7 and then 9. Give those two cells an extra
outline that will survive the layout change. Keep the unselected score 2
legible in its ordinary frame. Use the same blue accent for every score cell
and `.score`; selection must be recognizable without relying on color alone.

On **histories**, replace the read pointer with a red bracket under the grey
history block between the first two score cells. Spread your hands. Use one
plain `history` label for these repeated blocks, not a label on every block.
These are stored values, not empty padding or source-level history reads.

> We're only adding scores. The histories sit between them.

### 00:05.5-00:10 | Keep the data, change its layout

Bring the scores into one array and move the histories into a separate array.
Animate the same cells and blocks; do not redraw a different set of values.
Retain the extra outlines on 7 and 9 and leave 2 between them. Every grey
history block moves into the separate history lane in the same player order.
Label the two resulting lanes `scores` and `history`, without individual ID
or history labels. Change the state label from `Scores apart` to `Scores
packed` in place. Compress the score lane with your hands.

Keep `for (int id : ids)` fixed; change `players[id].score` to `scores[id]` at
the same screen position. On **scores together**, connect the packed score lane
to `scores[id]` with one red arrow. Then use the read pointer on 7 and 9 again,
in that order. Do not animate a read of 2 or every history block. The unchanged
query still selects IDs 0 and 2; those numbers remain director bookkeeping,
not another viewer-facing text row.

[scene_2.cpp](../../../../aliases/01-screen-short-form/short-06-data-layout/scenes/scene_2.cpp)
contains the matching code for this state. Use one continuous layout change,
not an animation followed by a second walkthrough of the same edit.

> Store the histories separately and pack the scores together.

### 00:10-00:13.5 | The measured payoff

Replace the diagram and code with the result card. Reuse the exact state labels
`Scores apart` and `Scores packed`; do not rename them `Before` and `After`.
Show the apart time as the preceding sentence finishes. On **Packing the
scores**, reveal the packed time. Reveal the speedup on **over twelve times
faster**, within that same continuous sentence. No spinner, fake timer,
countdown, or extra pause. These are recorded batch medians.

The speedup is the main read, followed by the two labeled times. The conditions
form a stable, readable footer; they must be present from the first displayed
measurement and remain through the question. Show the population and query
counts as explicit approximations, not rounded numbers presented as exact.

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

Keep matching row baselines and one shared time column. Use teal for the packed
result's frame and text; circle its lower time in red and point to it as the
ratio lands. The ratio can be larger than the rows, but the labels and footer
must remain readable at phone size. Do not add bars, the full benchmark report,
or another miniature layout beside each row.

> Packing the scores made these lookups over twelve times faster.

### 00:13.5-00:19 | Ask whether the result survives

Keep `Score-only lookups`, the speedup, and the measurement footer fixed.
Replace only the `Median batch time` heading and two timing rows with `Next
test: read both?` and the familiar score/history lanes. Use the same reserved
footprint; do not stack the lanes beneath the full table or shrink everything.

Bracket both lanes in red and point between them on **history too**. The next
test reads the same selected players' scores and complete histories. The
persisting 12.5x result belongs only to the already-measured score-only query,
not to this proposed follow-up. Do not add a time, winner accent, or predicted
speedup to the next-test lanes. Their shapes and colors retain the established
score/history encoding.

> Would this still win if we read the history too? That's what I'm testing next.

Cut immediately after **next**. No follow request, end card, or audio tail.

## Concrete layout example for the edit

Director's notation, not literal on-screen ASCII. Use the state labels `Scores
apart` and `Scores packed` in the same place, above the smaller descriptor
`Memory layout example`. Reuse the state labels verbatim in the timing rows.
The illustrative values do not claim that the benchmark timed only three
players; the result card names the actual large workload with rounded counts.

Viewer-facing information: score values 7, 2, and 9; matching grey history
blocks; one history label before the edit and two lane labels after it. An
extra outline marks 7 and 9 in both layouts. The loop, short captions, and
current red pointer or bracket remain. Do not display the ID row, `Selected
IDs` text, or H0/H1/H2 notation below. Do not add a selection legend.

Internal identity map for constructing and checking the animation:

```text
Selected IDs: 0, 2

Before: [7 | H0]  [2 | H1]  [9 | H2]
ID:         0         1         2

After:  scores    [7] [2] [9]
        histories[H0][H1][H2]
ID:               0   1   2
```

H0, H1, and H2 each represent that player's complete fifteen-number history,
not a single scalar. These names identify the blocks for the editor only.
All three scores and histories survive, with no player renumbering. Both
layouts select 7 and 9, giving the same sum of 16; do not narrate that arithmetic
or add a sum card. The selected values are closer after the edit, but the
unselected score remains between them and keeps its readable value.

The transformation must be understandable without reading two different
struct definitions. The code anchors the work; the moving cells explain the
storage change. Rendered clarity is still unverified.

## Second look at this revision

The result now carries the demonstration's labels directly into the two timing
rows. The spoken payoff names the changed layout and says `over twelve times`,
consistent with the recorded ratio. The card's main read is the speedup;
rounded, explicitly approximate counts preserve the large ordered workload
without eight-digit numerals. The next question replaces already-read rows,
and the persistent verdict remains scoped to score-only lookups.

The narration is 50 words, two more than Round 02. Those words support the
payoff's causal link and numerical qualification; word count is not the only
measure of a clear script. The reveal is staged within the spoken sentence,
not an artificial wait for the second result.

Remaining risk: the diagram still has to turn a struct declaration into a
recognizable memory layout in a very short transition. The spoken explanation
does not yet say `memory`; it relies on a small descriptor and the animation
to establish what `apart` means. Review that code-to-memory bridge next, while
avoiding a new cache lecture or unnecessary prerequisite. The current card
hierarchy and next-test scope also still require a real phone-size inspection.
Decision: advance to Round 04, not to recording or upload approval.

## Verification

- Input canonical SHA-256:
  `91187933e28e49a07ad9e961bb1ec16eac62b21ce39f49099a42452f31cea4d1`.
- Output canonical SHA-256:
  `ac0f103f363bb6caed65a39913d9fef30ccab2d66403ac0936713484ea67c6d2`.
- Five critiques, five narration beats, 50 spoken words. The complete archived
  spoken/visual core matches the canonical revision after rebasing local links.
- Round 02's archive hash remains
  `052cb9da74cf7db6316b6e8ffd4bad7ec0d9d79b8b73edc594b0583f128b49c4`.
- Checked local links, narration formatting, and absence of em dashes or
  trailing whitespace in the touched documents.
- Existing repeat-run JSON gives 4.355233333383997 ms and 0.3473418750218116 ms,
  or 12.538751145713448x. These round to 4.36 ms, 0.35 ms, and approximately
  12.5x. The spoken `over twelve times` is supported for this ordered case.
- 1,048,576 and 4,194,304 round to 1.05 and 4.19 million respectively. Both
  visible abbreviations include `~`; exact counts remain in the technical
  notes. Ordered IDs, normal `-O3`, and scalar execution remain on the card.
- Lookup source, query generation, and build flags match the loop-start hashes.
  No benchmark or fresh audience analysis was run. No scene code changed.
- The original illustrative scores, histories, IDs, and query order remain in
  the storyboard. The new result labels do not change the work being timed.
- First-frame readability, animation, gestures, subtitle placement, real
  duration, and the final composed payoff remain unverified.
