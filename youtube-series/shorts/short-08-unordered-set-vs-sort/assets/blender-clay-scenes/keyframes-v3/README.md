# Short 08 — Revision 3 review keyframes

Seven stills only; full video rendering remains stopped pending creator review.
Supersedes keyframes-v2. Native source remains 2160×2300 at (0,0) in the vertical
2160×3840 master. Code, colors, tactile clay materials and camera remain stable.

## Text policy

Only code, benchmark figures/units/speedup and data numerals. Removed all three
floating labels: unordered_set, sort + unique, flat hash table. No complexity
badges or explanatory text. The last scene retires the old benchmark before the
next unmeasured table is introduced through narration.

## Hash work and the comparison

The compact bucket rail leads to separately placed nodes. A substantial moving
pulse visibly follows the selected pointer; the duplicate lands beside the
stored key so the comparison is legible. Intended motion follows bucket selection,
pointer travel and key check sequentially. New distinct insertions seat a new
node and attach a link; duplicates add no node. No invented collisions, extra
hops, miss counters or rehashing. Distances are schematic, not actual addresses
or proportional delay.

The sorting scene retains multiple reorder beats. Only the subsequent unique
pass scans adjacent sorted values in order. More comparisons need not mean more
expensive memory access; this illustration is not a profile proving which cost
accounts for 9.68×. Technical background: [Abseil on memory indirection](https://abseil.io/fast/83).

The example remains 3,1,3,2,1 -> 1,1,2,3,3 -> 1,2,3. Equal values share colors:
1 teal, 2 cobalt, 3 raspberry. Tail slots remain allocated and unnumbered.
Code operates on prepared v; the benchmark's actual setup copy remains in its
original timed scope. No benchmark source, spoken line or measurement changed.

## Reproduction and outputs

build.py loads the actual Short 07 sculpted source and constructs seven constant
poses, audits text bounds and saves the packed editable short-08-keyframes.blend.
render_keyframes.py renders finite still passes on the authorized Omarchy RTX
3070 Ti / OptiX worker. compose_stills.py composes native passes, the review
contact sheet and separate proofs using the creator's actual safe-zone template.
No video supervisor is launched.

Physical frames 4 and 5, and text passes 1–4, are unchanged and reused from v2.
Other physical passes and result text are rendered again. This avoids spending
GPU time on identical states. render-report.json records only newly rendered
passes; reused passes retain their prior v2 provenance. Local assets here are
the canonical delivery location; the remote package is a dedicated render mirror.

1. 01-opening.png — input and active bucket-to-node route.
2. 02-speedup-tease.png — measured ratio above the hash structure.
3. 03-duplicate-insertion.png — duplicate and stored key compare side by side.
4. 04-sort-before-unique.png — five sorted values, direct v code.
5. 05-deduplicated-result.png — three retained values and minimal benchmark.
6. 06-memory-layout.png — pointer indirection versus adjacent retained values.
7. 07-flat-table-next.png — compact next-test storage, no labels or timing.
