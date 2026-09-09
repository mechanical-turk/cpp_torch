# Round 02: reduce the viewer's reading burden

Input: [Round 01](round-01.md), reread alongside the canonical `script.md`.
The input canonical SHA-256 is
`05c124a99fb0d63bb620c6249f7655ec2926db8dc2d24fbeece8ea03fcdb1195`.
Evidence IDs refer to [evidence.md](evidence.md).

## Critique of the input

1. **History identities can become a second vocabulary lesson.** H0, H1, and
   H2 help the editor preserve the data, but the viewer only needs to recognize
   the same history blocks before and after. Repair: keep those identifiers in
   director's notes, not the rendered graphic. Use one plain `history` label
   and animate the existing blocks into their new positions. This preserves
   R01's identity check without requiring the audience to decode its notation.
2. **The ID row competes with the score values.** The numeral 2 represents a
   score in one place and a selected ID in another. In a short shot, that can
   turn a storage-layout demonstration into an indexing puzzle. Repair: retain
   the exact IDs in the production contract and the actual indexed loop, but
   remove the extra on-screen ID row. Show the same selected score cells before
   and after instead. Never remove the unselected middle score.
3. **The attention sequence is not explicit enough.** The opening callout,
   captions, new memory diagram, score selection, and history bracket may all
   compete when the explanation starts. Repair: retire the curiosity callout
   after the hook; point at the scores during the first clause and at the
   intervening history during the second. Keep the code anchor still. E1
   supports testing synchronized speech and visual actions, not a claim that
   this exact edit has already improved retention.
4. **The spoken edit asks for more time than it needs.** "Keep the histories
   in a separate array, so the scores can sit together" restates the visual
   action in thirteen words. Repair: use a direct nine-word instruction and a
   short preceding explanation. Preserve the hook, measured payoff, and real
   follow-up question; fewer words alone are not a reason to weaken them.
5. **Less-prominent cells are not a complete selection cue.** Dimmed data can
   look discarded, and color alone can hide which scores the loop selects.
   Repair: retain legible values for all three scores, with an extra outline
   around selected 7 and 9. Carry those outlines through the move. A red
   pointer follows the same two reads, not every cell. E3 requires the same
   selected subset, even when its numeric ID labels stay off screen.

Decision: **rework the reading load, retain the same experiment and hook**.
This is a production-specification improvement, not a cold-viewer test.

## Lesson applied

R02: distinguish editor bookkeeping from information the viewer must read.
Preserve stable values, selected cells, and all stored data through motion;
remove redundant labels rather than shrinking their font. Apply the existing
prerequisite-burden, synchronized-reveal, and semantic-consistency rules. No
additional global playbook rule is needed.

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
callout now; the captions continue. Label the diagram `Memory layout example`.
The concrete values and selected IDs are specified below, but do not put the
ID row or H0/H1/H2 identifiers on screen.

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
or history labels. Compress the score lane with your hands.

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

Director's notation, not literal on-screen ASCII. Use `Memory layout example`
as the small diagram heading. Its illustrative values do not claim that the
benchmark timed only three players; the result card names the actual workload.

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

The rewrite keeps R01's complete identity map while making the viewer-facing
sequence simpler: the same outlined scores, the same grey history blocks, and
one storage change. It removes the visible ID row and history identifiers,
specifies when the opening callout leaves, and assigns the pointer to one
spoken target at a time. Narration falls from 53 to 48 words without cutting
the measured result or engagement question.

This still does not prove that the distinction is clear to a cold viewer.
Before approving the edit, check whether someone can identify what moved,
what stayed, and which layout produced the lower time without our explanation.
No such viewer test or phone-size render has occurred in this round.

Next pressure point: the result card still combines exact workload sizes,
optimization context, two times, a ratio, and returning history lanes. Its
`Before` and `After` labels also depend on remembering the preceding layout.
Review that reading load and mapping next without hiding the conditions that
make the comparison honest. Decision: advance to Round 03, not to upload.

## Verification

- Input canonical SHA-256:
  `05c124a99fb0d63bb620c6249f7655ec2926db8dc2d24fbeece8ea03fcdb1195`.
- Output canonical SHA-256:
  `91187933e28e49a07ad9e961bb1ec16eac62b21ce39f49099a42452f31cea4d1`.
- Five substantive critique items, five spoken beats, and 48 spoken words.
  The complete archived spoken/visual core matches the canonical revision,
  including the director's identity map, with relative links rebased.
- Local links resolve; checked files contain no em dash or trailing whitespace.
- The illustrative transformation retains scores 7, 2, and 9 and all three
  fifteen-value histories. IDs 0 and 2 select a sum of 16 in both layouts.
  This checks data consistency, not rendered geometry or comprehension.
- Rechecked the existing repeat-run JSON: ordered medians at 4,194,304 players
  are 4.355233333383997 ms and 0.3473418750218116 ms. The displayed 4.36 ms,
  0.35 ms, and approximate 12.5x result remain consistent with those values.
- Lookup kernels, query generation, and build flags match the loop-start
  hashes. Both camera fragments remain eight lines. No benchmark was rerun.
- Actual first-frame clarity, annotation timing, gestures, phone readability,
  and exported duration remain unverified.
