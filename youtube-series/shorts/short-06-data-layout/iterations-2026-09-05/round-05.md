# Round 05: give the first frame one reading order

Input: [Round 04](round-04.md), reread alongside the canonical script.
Input canonical SHA-256:
`7c4a7de5e0fcd9193c0a72ce21b3a9431c67e9a616644361a4200f89d7968a10`.
Previous turn: progress. The current file matches the recorded Round 04 output;
the complete prior sequence exists. No wait or blocker applies.

Use [E1 and E3](evidence.md). Short 5's complete spoken novelty arrived around
3.7 seconds, during its steepest observed loss. Its combined callout, captions,
code, and annotations remain a useful creative pattern, not separately proven
causes. This round tests a clearer first-frame specification, not new audience
performance. The same measured data-layout claim remains in force.

## Critique of the input

1. **`Opening caption` is not an exact caption instruction.** A conventional
   word-by-word subtitle could show only `This unused` at the start, even while
   technically satisfying the instruction that a caption exists. Repair:
   specify the complete seven-word hook in two short lines from the first
   decoded frame. Hold it through the spoken hook, then resume short changing
   captions. E1 motivates testing earlier promise delivery, not merely earlier
   subtitle appearance.
2. **`Never read` overstates the scope of the unused field.** The history is
   unused by this query, not necessarily by the application. That distinction
   matters to the final question. Repair: change the callout to `Unused here,
   still slower?`. Retain the contradiction without suggesting that all
   history data is globally dead or should simply be deleted.
3. **The caption and callout lack a shared hierarchy.** Both may become large
   headlines competing with the code. Repair: make the full hook caption the
   main read, place the smaller curiosity callout with the code, and reserve
   separate space for each. Keep the callout readable; do not solve crowding
   by shrinking the source or covering the presenter.
4. **The code markers can compete or obscure their targets.** `Circle history`
   could mean the entire declaration or a thick stroke across the identifier,
   while an equally loud score highlight draws the eye elsewhere. Repair:
   make the circle around the `history` identifier the dominant code marker;
   leave `.score` as a quiet, static blue cue. Keep every code character clear
   and defer moving read highlights until the explanatory beat.
5. **The first gesture may arrive after the claim it supports.** `Point toward
   the field as speech starts` can produce a first frame with the hand still
   outside the shot. Repair: record the opening with a small downward point
   already visible and continue that movement during the hook. Maintain eye
   contact and keep the caption away from the face and pointing hand. Do not
   insert silent preparation or a staged pause to achieve the pose.

Decision: **retain the spoken hook and rewrite its first-frame treatment**.
No new metric or extra opening explanation is needed. R02's attention-order
lesson now applies before the diagram, while R01-R04's demonstration survives.

## Lesson applied

R05: distinguish having a caption on frame one from having the complete promise
on frame one. Give that promise priority, attach the callout to the evidence,
and make the first gesture support the same target. Existing opening,
annotation, and safe-area rules cover the repair; do not add a duplicate rule
to AGENTS.md or claim the audience has validated this treatment.

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

The first frame now contains the complete seven-word promise, not just an
unspecified subtitle fragment. The two caption lines contain 17 and 20
characters. The scoped curiosity callout supports that promise beside the
evidence, while the red circle, quieter score cue, and ready gesture have
different roles. None requires another spoken setup sentence.

All five narration beats remain unchanged at 52 words. The existing data
transformation, scoped benchmark, and engagement question survive intact.
This round improves production instructions; it does not establish an audience
effect or guarantee that all first-frame elements will fit at phone size.

The opening still combines text, code, and a presenter. Check the actual edit
for competing reads and caption overlap rather than assuming that the written
hierarchy solves those risks. Holding the complete hook is a proposed timing
treatment, not a proven improvement over the previous caption style.

Next, read the five spoken beats as one continuous passage. In particular,
check whether repeating `pack the scores` immediately before `Packing the
scores` reinforces the cause of the result or spends words the viewer no
longer needs. Also check whether the transition instructions fit that spoken
flow. Do not remove useful reinforcement merely to make another change.
Decision: advance to Round 06; no recording or upload approval.

## Verification

- Input canonical SHA-256:
  `7c4a7de5e0fcd9193c0a72ce21b3a9431c67e9a616644361a4200f89d7968a10`.
- Output canonical SHA-256:
  `3a9197e943e2862aa91442cb0f5a692d224cc77eaefa4bdaffda61552dd41bb9`.
- Five critiques, five narration beats, 52 spoken words. The complete archived
  spoken/visual core matches the canonical revision after rebasing links.
- Round 04's archive remains unchanged at SHA-256
  `42bd02130ea51fb08333b4b7ec61087b4b7e476f8fe8762dac890659071a5698`.
- Verified the exact two-line opening caption, its scoped callout, and the
  unchanged narration, measured-payoff sequence, and engagement question.
- Checked local links, absence of em dashes and trailing whitespace, source
  hashes, and the two eight-line camera fragments. The build-file comparison
  uses `data-layout/CMakeLists.txt`, not the unrelated root build file.
- Rechecked the existing repeat-run JSON: 4.36 ms and 0.35 ms rounded medians,
  with a 12.538751 ratio supporting the displayed approximate 12.5x result.
  No fresh benchmark, platform collection, or media render occurred.
- First-frame readability, caption placement, gesture timing, actual runtime,
  and audience comprehension remain unverified final-media checks.
