# Round 04: connect the code to memory

Input: [Round 03](round-03.md), reread alongside the canonical `script.md`.
Input canonical SHA-256:
`ac0f103f363bb6caed65a39913d9fef30ccab2d66403ac0936713484ea67c6d2`.
The preceding turn was progress: its recorded output is the current file and
its complete revision is archived. There is no live wait or blocker.

Use [E1, E3, and E5](evidence.md): synchronized explanation is a working
creative pattern, the benchmark fixes the data contract, and direct feedback
identified a clarity concern. None proves comprehension of this unmade edit.

## Critique of the input

1. **The explanation leaves `memory` to a small visual label.** `Histories sit
   between them` might describe the diagram without explaining that it shows
   how the data is stored. Repair: name memory in the same short sentence that
   names the scores. Keep the hook and move directly into the explanation;
   do not add a definition of a struct or a cache.
2. **The struct disappears before its relationship to the records is clear.**
   A cut from a declaration to three boxes asks the viewer to supply that
   relationship. Repair: carry the highlighted score field into the blue
   score cells and the circled history field into grey history blocks during
   one direct transition. Keep the actual lookup fixed. E1 makes this a useful
   synchronization test, not a reason for a separate animation preface.
3. **The bracket does not match the selected scores.** The pointer selects 7
   and 9, while the specified bracket sits under the history between the first
   two scores, 7 and 2. Repair: show the spacing between the same selected pair
   before and after. Preserve the unselected score 2 inside that span; do not
   relabel it as history or quietly change which IDs are read.
4. **The geometry does not yet enforce unchanged stored data.** Saying that
   blocks move is weaker than specifying that each retains its dimensions.
   A renderer might shrink the history blocks to fit the second lane, implying
   data compression or removal. Repair: keep each score cell and history block
   the same size through the transformation. Fit the initial composition with
   both arrangements in mind rather than rescaling one side later.
5. **A moving read pointer can imply more than the evidence establishes.**
   Travel through grey blocks or a faster sweep after packing could appear to
   show actual reads or measured memory latency. Repair: pulse only the two
   selected score cells, at the same illustrative cadence in each layout.
   Use the bracket for spatial separation, not execution time. E3 supports the
   measured layout win, not a hardware-counter or cache-miss animation.

Decision: **rework the code-to-memory bridge; keep the same claim and result**.
Carry forward the concrete values, reduced labeling, and matched result labels
from R01-R03. Do not restore an introductory lecture.

## Lesson applied

R04: make the representation change visible at the moment it is named. Match
annotations to the exact selected data, preserve object geometry, and keep
illustrative motion separate from performance evidence. This applies existing
semantic-consistency, synchronized-reveal, and evidence-matches-headline rules.

Evidence-note correction: Round 03 called the exact workload counts
eight-digit values. Both 1,048,576 and 4,194,304 have seven digits. Its recorded
counts, rounded display values, and benchmark calculations were correct. This
correction does not change the experiment or rewrite the archived round.

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

Keep the loop in the same screen position. Carry the declaration's `score`
field into blue score cells and its circled `history` field into grey history
blocks as the declaration becomes the three-record diagram. Use one direct
transition during this sentence, not a separate one-player lesson or an
animation of creating data. Remove the opening curiosity callout; captions
continue. Label the state `Scores apart`, with `Memory layout example` below.

On **adding scores**, pulse 7 and then 9 and point toward them. Their extra
outlines persist through the change. Keep unselected 2 legible in its ordinary
frame. Every score cell uses the same blue accent as `.score`; color alone
must not indicate selection. Do not display the ID row or H0/H1/H2 labels.

On **histories**, bracket the gap from the right edge of score 7 to the left
edge of score 9 and spread your hands. The intervening blue score 2 remains
visible, alongside the grey history blocks. The single `history` label refers
only to grey blocks, not the whole gap. Finish the caption with **in memory**.
These blocks are stored data, not blank padding or reads made by the loop.

> We're only adding scores, but histories sit between them in memory.

### 00:05.5-00:10 | Keep the data, change its layout

Bring the scores into one array and move the histories into a separate array.
Animate the same cells and blocks; do not redraw a different set of values.
Keep each score cell and each history block the same size during this move.
Retain the extra outlines on 7 and 9 and leave 2 between them. Every grey
history block moves into the separate history lane in the same player order.
Label the two resulting lanes `scores` and `history`, without individual ID
or history labels. Change the state label from `Scores apart` to `Scores
packed` in place. Compress the score lane with your hands.

Keep `for (int id : ids)` fixed; change `players[id].score` to `scores[id]` at
the same screen position. The spacing bracket follows scores 7 and 9 as the
gap contracts; score 2 stays between them. On **scores together**, replace the
bracket with one red arrow connecting the packed score lane to `scores[id]`.
Then pulse 7 and 9 again in the same order and at the same illustrative cadence.
Do not sweep a read pointer through score 2 or the histories, or speed up the
pulses as a substitute for the measured result. The unchanged query still
selects IDs 0 and 2; those numbers remain director bookkeeping.

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

The spacing bracket uses the same endpoints in both states: the right edge of
7 and the left edge of 9. Its initial span contains H0, score 2, and H1; its
final span contains score 2. It illustrates separation, not which bytes the
CPU fetched. Do not mark the intervening score as history.

Use one fixed-width blue cell template and one fixed-width grey history-block
template throughout the comparison, with the history block wider than a score
cell. Their dimensions do not change when they move to separate lanes. The
diagram is schematic, not drawn to the fifteen-to-one payload ratio. Choose
the initial composition so both arrangements fit without compressing data
blocks or removing labels. The selected cells pulse at the same cadence in
both states; actual timing appears only in the benchmark card.

The transformation must be understandable without reading two different
struct definitions. The code anchors the work; the moving cells explain the
storage change. Rendered clarity is still unverified.

## Second look at this revision

The explanation now names memory in the same sentence as the scores. The
diagram comes directly from the displayed fields, and its spacing marker
follows the two scores the lookup actually selects. Moving blocks keep their
dimensions; pulses identify reads without purporting to time them. These
changes retain R01's identities, R02's reduced labels, and R03's result mapping.

The draft has 52 spoken words, two more than Round 03. The explicit memory
reference carries useful meaning rather than introducing another prerequisite.
No cache hierarchy or vector-control-block explanation enters the narration.
The measured payoff and adjacent question remain unchanged.

The planned transition still needs a real edit: it must finish while the
explanation continues, without turning into a separate animated introduction.
Actual timing, readability, and comprehension remain unverified. Next, review
the first frame as a coordinated hook. The circle, code highlights, caption,
and curiosity callout all arrive immediately, but the script has not yet
specified their reading hierarchy as carefully as the benchmark's.
Decision: advance to Round 05; no recording or upload approval.

## Verification

- Input canonical SHA-256:
  `ac0f103f363bb6caed65a39913d9fef30ccab2d66403ac0936713484ea67c6d2`.
- Output canonical SHA-256:
  `7c4a7de5e0fcd9193c0a72ce21b3a9431c67e9a616644361a4200f89d7968a10`.
- Five critiques, five spoken beats, 52 spoken words. The complete archived
  spoken/visual core matches the canonical revision after rebasing links.
- Round 03 remains unchanged at archive SHA-256
  `b50b1aefbdd7a920fa5c8f5ec0dbcc233e0c6ac86e83b7dd110790983105ae8f`.
- Checked local links, narration formatting, and absence of em dashes or
  trailing whitespace in the touched documents.
- A symbolic arrangement check confirms the bracket between 7 and 9 spans
  H0, score 2, and H1 before the edit, and only score 2 after it. The data check
  retains all scores, IDs, and fifteen-value histories, with a sum of 16 for
  both selected-score queries. Neither check verifies rendered geometry.
- The result sequence and its conditions remain unchanged from Round 03;
  this round does not introduce another performance claim or new measurement.
- Lookup kernels, query generation, and build flags still match loop-start
  hashes. Both camera fragments remain eight lines. No benchmark was rerun.
- The digit-count correction is verified: each exact workload count has seven
  digits. No workload value or displayed approximation required correction.
- All final-media checks remain unverified, including the new transition,
  bracket placement, block dimensions, captions, movement, and export duration.
