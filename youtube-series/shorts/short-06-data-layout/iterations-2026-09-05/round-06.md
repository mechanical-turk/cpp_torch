# Round 06: finish the edit, then deliver the result

Input: [Round 05](round-05.md), reread alongside the canonical script.
Input canonical SHA-256:
`3a9197e943e2862aa91442cb0f5a692d224cc77eaefa4bdaffda61552dd41bb9`.
Previous turn: progress. Its canonical output and complete archived revision
match the recorded hashes. No process wait or blocker applies.

Use [E1, E3, and E5](evidence.md). The Short 5 final-media report observes a
comparatively stable middle where the spoken edit and its visual action land
together. That is a reason to preserve synchronization, not proof that this
revision will improve retention. E3 establishes the unchanged lookup task;
E5 motivates making the comparison easier to follow. No new data was pulled.

## Critique of the input

1. **The payoff repeats the action instead of advancing the explanation.**
   `Pack the scores together` is immediately followed by `Packing the scores
   made...`. The repetition does identify the winning change, but the finished
   diagram and matching result labels already do that. Repair: use `The same
   lookups ran over twelve times faster.` This adds the useful unchanged-work
   connection while cutting two words. Keep the labels and scoped conditions
   so brevity does not detach the number from the experiment.
2. **A second read sequence can become a visual pause after the edit.** The
   script finishes packing, changes the bracket into an arrow, and then pulses
   both selected values again. Those pulses repeat the earlier reads after
   the spoken action is essentially complete. They are not required to show
   preservation: the selected-score outlines and fixed ID loop already do
   that. Repair: retain those outlines, finish the source edit and arrow with
   the packing phrase, and omit the second pulse sequence. Do not rush several
   extra animations into the final word or wait for them before the result.
3. **The result transition can erase the layout at the moment it resolves.**
   Showing the apart time `as the preceding sentence finishes` competes with
   the arrow and newly packed layout that are meant to appear on `scores
   together`. Repair: keep that completed state through the end of the phrase,
   then replace it with the comparison on `The same lookups`. Show both timing
   rows with the conditions and reveal the ratio on `over twelve times faster`.
   This is one continuous spoken transition, without a silent hold or a timer.

This focused pass found three substantial repairs. Do not manufacture two
additional faults to meet a preferred critique count. The opening, memory
explanation, and final discussion question remain useful and stay unchanged.

Decision: **rework the edit-to-result transition**. Apply R03's label continuity
and R04's truthful storage example while removing an unnecessary replay.

## Lesson applied

R06: after showing an action, use the next sentence for its consequence or a
new useful connection. Preserve a completed visual long enough to match its
spoken phrase, then move on. Do not add another demonstration merely to fill
an edit target. The existing uninterrupted-chain, synchronized-visual, and
honest-reveal rules cover this repair; no new global rule or causal audience
finding is needed.

## Rewritten script

Proposed MP4: `cpp-data-layout-unused-fields-id-lookup-short-06.mp4`.
Target: 18-19 seconds, final runtime unverified. The [shared contract](evidence.md)
and canonical technical notes remain in force.

### 00:00-00:02 | The unused field

Open on [scene_1.cpp](../../../../aliases/01-screen-short-form/short-06-data-layout/scenes/scene_1.cpp).
The eight-line player definition and score lookup are visible immediately.
Use one reading order: complete hook caption, circled field, supporting code.
The viewer should not need to parse the whole struct to understand the promise.

Opening caption, fully visible on the first decoded frame:

```text
This unused field
is slowing your loop
```

Hold both lines through the spoken hook. Do not reveal them word by word or
start with only `This unused`. Emphasize **unused field** in yellow and
**slowing** in teal from frame one, with a high-contrast outline. This replaces
the ordinary changing subtitle for this sentence; do not show both versions.

Smaller curiosity callout above the code: **Unused here, still slower?**

Reserve the two-line caption band in the webcam region, clear of the eyes,
mouth, and pointing hand. Put the callout in its own slot above the declaration
in the code/visual region, inside the platform-safe area. Keep both readable,
but do not give the callout the same headline weight as the main caption.
Removing it for the next beat must not move the lookup code.

Circle only the `history` identifier in red, leaving its letters and neighboring
code unobscured. This is the dominant code marker. Keep `.score` marked with a
quieter static blue cue so the actual read is visible without another moving
target. Do not circle the whole struct or begin by animating the circle's stroke.

Record with a small downward point already visible and continue the gesture
toward `history` as speech begins. Keep eye contact. Cut away any preparation
before the first word, not into it. The full caption, callout, code, circle,
blue cue, and presenter must already be present. No fade-in or silent setup.
Do not show the packed layout or benchmark yet.

> This unused field is slowing your loop.

### 00:02-00:05.5 | Show what the field does

Keep the loop in the same screen position. Carry the declaration's `score`
field into blue score cells and its circled `history` field into grey history
blocks as the declaration becomes the three-record diagram. Use one direct
transition during this sentence, not a separate one-player lesson or an
animation of creating data. Remove the opening curiosity callout; captions
switch from the held hook to short synchronized phrases for this sentence.
Label the state `Scores apart`, with `Memory layout example` below.

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
the same screen position while the scores come together. The spacing bracket
follows scores 7 and 9 as the gap contracts; score 2 stays between them. By
**scores together**, the layout and code edit are complete. Replace the bracket
with one red arrow connecting the packed score lane to `scores[id]` and keep
that state through the end of the phrase.

Keep the outlines on 7 and 9; do not replay their read pulses after packing.
The unchanged loop and selected values establish the same query without a
second demonstration. Do not sweep a read pointer through score 2 or the
histories. The query still selects IDs 0 and 2; those numbers remain director
bookkeeping. There is no post-sentence animation to wait for before the result.

[scene_2.cpp](../../../../aliases/01-screen-short-form/short-06-data-layout/scenes/scene_2.cpp)
contains the matching code for this state. Use one continuous layout change,
not an animation followed by a second walkthrough of the same edit.

> Store the histories separately and pack the scores together.

### 00:10-00:13.5 | The measured payoff

Replace the diagram and code with the result card. Reuse the exact state labels
`Scores apart` and `Scores packed`; do not rename them `Before` and `After`.
Keep the completed layout visible through **scores together**. On **The same
lookups**, show both timing rows and their conditions. Reveal the speedup on
**over twelve times faster**, within that same continuous sentence. The two
times already show which layout won; do not pretend the ratio is another
unresolved question. No spinner, fake timer, countdown, or extra pause. These
are recorded batch medians, not a timer running during the layout change.

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

> The same lookups ran over twelve times faster.

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
blocks or removing labels. Pulse the selected cells in the initial layout,
then retain their outlines through the move. Do not add a second read sequence
after packing; the unchanged selection remains visible. Actual timing appears
only in the benchmark card, not in the speed of the animation.

The transformation must be understandable without reading two different
struct definitions. The code anchors the work; the moving cells explain the
storage change. Rendered clarity is still unverified.

## Second look at this revision

The spoken passage now moves from an action to its measured consequence without
repeating the packing phrase. `The same lookups` reinforces the fair comparison
while the familiar `Scores apart` and `Scores packed` labels identify the two
states. There are 50 spoken words, down from 52; the objective is better flow,
not a word-count minimum.

The visual edit also has a cleaner boundary. Complete the layout and source
change by `scores together`, retain that view through the phrase, then display
the two medians as the next sentence starts. The selected outlines remain;
another read animation is unnecessary. Displaying both times already makes
the winner available, so the ratio is emphasis rather than a second cliffhanger.

This removes a planned source of delay. It does not prove that the animation
fits the narration or that a viewer understands the physical arrangement.
Keep the existing timecodes provisional. A natural read and actual edit must
determine those boundaries without padding a shorter delivery.

Next, inspect the result-to-question transition as a complete frame. The
score-only speedup remains above a new score-plus-history question. The labels
scope it in writing, but their combined visual impression needs another
review: the viewer must not mistake an earlier measurement for evidence about
the next test. Preserve the genuine question, not a follow request.
Decision: advance to Round 07; no recording or upload approval.

## Verification

- Input canonical SHA-256:
  `3a9197e943e2862aa91442cb0f5a692d224cc77eaefa4bdaffda61552dd41bb9`.
- Output canonical SHA-256:
  `95dadec89944123b93db74ab14cfc155b1523c9b4622d696ffc729f73efb2c91`.
- Three substantive critiques, five spoken beats, 50 spoken words. Only the
  fourth spoken beat changed. The complete archived spoken/visual core matches
  the canonical script after rebasing links.
- Round 05's archive remains unchanged at SHA-256
  `4e792f532d6893eaa6762710a1067be34c23f60c57a1d9084507ee1f23c8ae98`.
- Verified removal of the second read sequence and alignment of the completed
  layout, spoken phrase, timing rows, and ratio in the written instructions.
  This is a script consistency check, not rendered timing evidence.
- The outro remains unchanged. All scores, histories, selected IDs, and order
  remain in the example. A symbolic check gives a sum of 16 for both layouts
  and preserves each fifteen-value history; it does not test a final visual.
- Checked local links, narration formatting, absence of em dashes and trailing
  whitespace, source hashes, and the two eight-line camera fragments.
- Existing repeat-run JSON still supports rounded medians of 4.36 ms and
  0.35 ms and an approximate 12.5x ratio. Benchmark kernels, query generation,
  and `data-layout/CMakeLists.txt` retain their loop-start hashes.
- No benchmark run, new platform-data collection, media rendering, or publishing
  occurred. Actual timing, readability, movement, and comprehension remain
  unverified; this round does not pass the upload gate.
