# Episode 8: voice and literal-edit review

September 7, 2026. Script review, not a measured audience result.

## What failed

Short sentences still read like isolated facts. The script often announced a
concept without connecting it to the code we had just written. Instructions to
move storage or update callers also left the presenter reconstructing edits
while recording. More headings did not solve either problem.

## Repairs

- Connected the actual dependencies: retaining inputs leads to shared storage;
  gradients need recorded parents; parents give traversal a path; tensor-sized
  parents need a cell mapping; the arithmetic rules then compose into MSE.
- Rewrote the spoken track around the current edit, preserving reasons instead
  of replacing them with slogans, sentence fragments or forced informality.
- Replaced prose-only editing directions with 63 exact Before/After pairs,
  including storage reads, constructors, includes and all four operator callers.
- Kept preparation separate and identified incomplete multi-edit compile stages.
- Made the verifier replay those exact pairs with no extra transformations.
- Added causal section transitions to the long-form playbook's delivery check.

## Second review

The migration starts with ownership, not a backward helper. Each section now
answers a need left by the previous one. Broadcast strides are saved, while
cell indices are recomputed. The script explains repeated gradient writes and
does not claim matmul differentiation or training works in this episode.

All 63 edit pairs replayed successfully. All runnable checkpoints and 128
central finite-difference comparisons passed with address and undefined-behavior
sanitizers. Both demonstration source files remained unchanged. See
[verification](verification.md) for coverage and limits.

The guide is longer because it contains exact editing references. Those blocks
are not extra spoken content. Section A still has many mechanical changes, and
section D needs enough time for the viewer to follow the growing method. The
presenter must test that pacing; a text review cannot certify a natural delivery.

## Score and next check

92.5/100, rework under the playbook threshold. L04 is partial because the
first-minute payoff has not been timed. L11 is partial pending a spoken
read-through, and L15 awaits publishing keyword research. This corrects the
earlier overconfident 96.5 assessment rather than claiming new retention evidence.

Next: a paced read-through of A and D. Trim recording pauses or repeated
explanations if needed, without removing the reasons that make the edits clear.

## Follow-up: presenter rejected the transitions

The presenter identified the opening-to-storage jump as an example of a wider
problem. The previous wording named the solution without walking through the
decision, despite the review describing the explanations as connected.

Revised the segment boundaries again. The opening now connects remembering
inputs to retaining their storage. Later bridges describe the concrete next
edit: fix the constructor after moving fields, update callers after changing
the helper signature, attach history before returning results, and permit the
new rules after implementing them. Moved guidance ahead of code where it was
previously only a retrospective explanation. Kept all literal code pairs intact.

Score remains 92.5, rework. Presenter rejection is direct evidence about the
previous draft's voice; this additional text review does not establish approval
of the replacement. The longer bridges also need a pacing check.
