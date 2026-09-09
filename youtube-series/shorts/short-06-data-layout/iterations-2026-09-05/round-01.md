# Round 01: make the transformation concrete

Input: [baseline](00-baseline.md), read from the current `script.md` before
editing. Apply E5's direct clarity feedback alongside E1's synchronized
explanation pattern. Evidence IDs refer to [evidence.md](evidence.md).

## Critique of the input

1. **The memory diagram is underspecified.** Instructions to draw repeated
   records do not establish which values the viewer should track. Repair:
   use one small, explicitly illustrative window with stable score values and
   player IDs across the transformation. This applies the existing semantic
   consistency and concrete-opening checks, not a new audience finding.
2. **"Spreads them across memory" remains abstract.** The viewer needs to
   understand what the loop adds before understanding its layout. Repair:
   point to two selected scores and name the addition directly. Keep their
   history blocks visibly between the values before moving the blocks.
3. **A strip of packed scores could silently change the work.** It might look
   like we kept only the queried players. Repair: leave an unselected score
   visible between the same two selected IDs after the edit. Do not depict the
   selected values as newly adjacent when their IDs are not adjacent. E3
   requires preserving the entire score array and exact query sequence.
4. **The caller-to-storage relationship is hidden in the snippets.** In scene
   2, `scores` is a function input supplied from the split storage; merely
   showing a struct with a same-named member is weak visual proof. Repair:
   connect the visible score lane directly to `scores[id]` with the same accent
   used for `players[id].score` before the edit. Keep the code minimal rather
   than adding an off-topic calling-convention explanation.
5. **The unrendered plan cannot support a confidence claim.** This version
   still needs a phone-size visual check. A concrete storyboard is progress
   because it constrains the next render, but it cannot prove comprehension
   or retention. Keep the visual and runtime gates unverified.

Decision: **rework the explanation and storyboard, retain the topic and hook**.
Do not add a second benchmark or a longer setup.

## Lesson applied

R01: give the viewer stable values and identities to follow through a layout
change. Show the untouched data and unchanged query selection. Cite the
existing fair-task, visual-consistency, and prerequisite-burden checks rather
than adding a duplicate playbook rule.

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
above it with three adjacent player records. Use the concrete layout example
below, with IDs 0 and 2 selected. Point first to score 7, then score 9. Leave the
unselected score 2 present but less prominent.

The score cells use the same blue accent as `.score` in the loop. Each grey
history block belongs to one player. A red bracket spans the history between
score positions as your hands spread. These are stored values, not empty
padding or source-level reads of the histories.

> We're adding these scores, but their histories keep them apart.

### 00:05.5-00:10 | Keep the data, change its layout

Bring the scores into one array and move the histories into a separate array.
Animate the same cells; do not redraw a different set of values. Scores 7, 2,
and 9 retain IDs 0, 1, and 2. Histories H0, H1, and H2 remain visibly stored in
their own array. Compress the score lane with your hands.

Keep `for (int id : ids)` fixed; change `players[id].score` to `scores[id]` at
the same screen position. Connect the score lane to the changed expression
with one red arrow. Repeat the selection of IDs 0 and 2. Do not move the
unselected score 2 out of the array, put the selected scores directly next to
each other, or animate a scan over every player.

[scene_2.cpp](../../../../aliases/01-screen-short-form/short-06-data-layout/scenes/scene_2.cpp)
contains the matching code for this state. Use one continuous layout change,
not an animation followed by a second walkthrough of the same edit.

> Keep the histories in a separate array, so the scores can sit together.

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

> The same lookups run twelve times faster here.

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

## Concrete layout example for the edit

Director's notation, not literal on-screen ASCII. Label the visual `Layout
example`; these illustrative values are not a claim that the benchmark timed
only three players. The result card names the actual large workload.

```text
Selected IDs: 0, 2

Before: [7 | H0]  [2 | H1]  [9 | H2]
ID:         0         1         2

After:  scores    [7] [2] [9]
        histories[H0][H1][H2]
ID:               0   1   2
```

H0, H1, and H2 each represent that player's complete fifteen-number history,
not a single scalar. All three scores and histories survive. Both layouts
select 7 and 9, giving the same sum of 16; do not add a spoken arithmetic
detour or another result card for that simple identity. The selected values
are closer after the edit, but the unselected score remains between them.

The transformation must be understandable without reading two different
struct definitions. The code anchors the work; the moving cells explain the
storage change. Rendered clarity is still unverified.

## Second look at this revision

The concrete example now gives the editor an exact invariant to preserve:
IDs 0 and 2 select scores 7 and 9 before and after, with score 2 and every
history retained. The language names the addition and the separate history
array. This is stronger specification, not evidence of successful rendering.

Remaining risk for the next round: tracking IDs, score values, and history
labels may introduce too much simultaneous reading in a very short shot.
Evaluate that burden against the clarity gained; do not automatically add
more labels to solve it. The result-card density and exact vocal pacing also
remain open. Decision: advance this version into Round 02, not into upload.

## Verification

- Input canonical script SHA-256:
  `ff242c72d2413052bff4b067145f85bb1ac97c70fc45ddcca2fe361809468470`.
- Output canonical script SHA-256:
  `05c124a99fb0d63bb620c6249f7655ec2926db8dc2d24fbeece8ea03fcdb1195`.
- Five itemized critiques; five spoken beats; 53 spoken words. This archived
  narration matches the canonical script for Round 01.
- Local links resolve. The illustrative lookup gives 16 in both layouts;
  all scores, histories, and IDs remain. This checks the storyboard's data
  relationship, not its rendered legibility or audience response.
- Lookup kernels, query-generation code, and CMake flags are unchanged from
  loop start. No benchmark was run and no new performance result is claimed.
- First-frame clarity, animation, captions, gestures, and final duration remain
  unverified until actual media is reviewed.
