# Chapter 14 preparation and review

Recording script: [script.md](script.md). Research: [keyword-research.md](keyword-research.md).
Verifier: [verify-script.mjs](verify-script.mjs), report: [verification-run.json](verification-run.json).
Publishing package: [publishing.md](publishing.md). Release state: [distribution.md](distribution.md).

## History of this script

This is the first draft. The creator set the scope in conversation, in order:
Chapter 13 introduces learning rate decay; Chapter 14 is focused on residual
connections plus gradient debugging machinery; momentum, velocity, Adam and
optimizer classes move to the following episode. The creator also asked that the
network be extended until the vanishing gradient shows up strongly enough that
residual layers visibly solve it. The first idea (eight hidden layers) did not
qualify: at eight layers the creator's own ReLU network reached about 92% with decay, so
it was never truly broken. Sixteen hidden layers does qualify (see the evidence
table). The creator also asked for a result that does not need 40 epochs; the
script trains for 10 epochs and mentions the 40-epoch run only as an offline
measurement in the closing section.

The creator then found the first draft's opening too abrupt and asked it to
mention what was tried with learning rates and decay. The cold open now names
the network and dataset, says that a bigger learning rate and a decaying one
both helped, and says that at sixteen layers neither gets it to learn. That is
a brief orientation, not a recap, and it avoids referring to an earlier
episode. The creator also questioned the first table: it says eight hidden
layers but shows seventeen rows. The report prints one row per `Layer` object,
so the flat network has a Linear row and a tanh row for each hidden layer plus
the output layer. The narration now says this before the run, and its
directions say rows instead of layers. A cleaner table would need the
`hidden_layer` refactor before the first report, which delays the first payoff
further (see the critique).

Chapter 13's recorded closing list says the next episode covers why signals
shrink, residual connections, and momentum and velocity. This episode delivers
the first two and defers momentum and velocity, so Chapter 13's closing list
needs a creator decision (edit it, or accept the mismatch).

## Scope and checklist plan

The starting point is the Chapter 13 final source as the script derives it
(`verification/episode-13-baseline.cpp`, SHA-256
`b58ca27507023b69d81069569ebdbebdee950a6508acb9a63debe4e0198c9f27`), not the
creator's live `main.cpp`, which has diverged (for example ReLU layers and
epoch constants). The creator must reconcile the two when recording.

New code, in order: `Sequence::forward_traced`, `root_mean_square` and
`print_signal`, `Sequence` becomes a `Layer`, the `hidden_layer` helper, a
sixteen-layer model, the training setup (rate 0.5, 10 epochs, decay 0.9), a
`Residual` layer wrapped around fifteen of the sixteen hidden layers, and a
lowered learning rate (Section D).

- **Opening promise:** the network stops learning once enough layers are
  stacked; build a tool for debugging gradients that looks inside the network,
  then fix the problem with residual connections.
- **Curiosity question:** what is happening inside a network that cannot leave
  the guessing loss, and what changes when a layer adds to its input? Payoff:
  the layer-by-layer table (signal and gradient shrink), the stuck sixteen-layer
  run, then the residual network at 58.85% with a growing gradient, then the
  same network at 91% once the learning rate is lowered.
- **Distinctive viewer benefit:** a gradient report written by hand that turns
  "vanishing gradient" into numbers they can read on screen, and a residual
  layer that is about ten lines because `Layer` and `Sequence` already exist.
- **First useful action:** begin the first edit (`forward_traced`) after about
  76 spoken words, about 0:30.
- **First payoff:** the first table, with the signal and gradient shrinking
  through the existing eight-layer network, after four edits and a 6-second run.

| ID | Intended treatment |
| --- | --- |
| L01 | Concrete promise and curiosity question above; boundary: no optimizers, no more data. |
| L02 | The first sentence names the C++ network and MNIST, the second and third say what was already tried (a bigger learning rate, decay) and where it fails (sixteen layers), and the fourth names the tool and the fix. Title overlay in the first five seconds. |
| L03 | Existing `Sequence` on screen from frame zero; the first edit starts after 76 words. |
| L04 | Audited as partial. The tool must be written before it shows anything, so the first measured insight is several minutes in. |
| L05 | A: a report of signal and gradient size per layer. B: sixteen layers as one line each, and the proof that plain training fails. C: a `Residual` layer and the same network trained. |
| L06 | `forward_traced` only when the report needs it; `Sequence` as a `Layer` only when sixteen layers make the list unwieldy; `Residual` only after the failing table. Each edit has a one or two sentence preview. |
| L07 | Why signal and gradient shrink (about 0.57 per layer, measured); why a plus sign keeps a gradient path; why only fifteen of sixteen layers can be wrapped. |
| L08 | Eleven literal Before/After edits replayed by the verifier against the frozen Chapter 13 source; three checkpoints compiled and run. |
| L09 | Each run answers a question: how big are the signals, does depth break training, does adding fix it. Unit checks stay off camera. |
| L10 | Directions name the exact function, edit region or output column to point at. Rendered highlighting is a production check. |
| L11 / L11a | 1,173 spoken words; see the runtime estimate. |
| L12 | Delivers the promised debugging tool and fix, states the limit (memorization), and ends with a concrete next list. |
| L13 | Itemized recap, three next-episode items, exact sign-off, clean tail. No Q&A. |
| L14 | `script.md` holds the filename, one canonical `>` narration, exact edits and expected output only. |
| L15 | Keyword research precedes the narration; the map is audited below. |
| L16 | Evidence, conditions and limits below; no reach prediction or release approval. |

## Evidence

All results use the creator's MNIST files (10,000 training images, 2,000 test
images), tanh layers of width 32, seed 42 unless stated, plain gradient descent.
Rows marked **replayed** are asserted by `verify-script.mjs`. Rows marked
**scratch** were measured earlier in this session with an equivalent harness,
are not replayed, and are not quoted in the narration except where noted.

| Finding | Result | Status |
| --- | --- | --- |
| Eight hidden layers, first batch, rate 1.0 halved each epoch (the starting source) | Signal 1.8e-01 to 1.5e-03 at the scores; gradient 2.6e-05 at layer 1, 4.7e-03 at the output (about 180 times) | replayed, displayed |
| Sixteen hidden layers, plain, rate 0.5, decay 0.9, 10 epochs | Loss 2.30346 to 2.30155; 11.7% accuracy | replayed, displayed |
| Sixteen plain layers, starting rate 0.1, 0.3 or 1.0, decay 0.9 | Final loss at least 2.29, accuracy at most 20% | replayed (spoken: "stays at 2.30") |
| Sixteen plain layers, per-layer shrink | Gradient first over last hidden layer 2.0e-4, about 0.57 per layer; signal last over first 1.5e-4 | replayed (spoken: "a little more than half") |
| Sixteen residual layers, same settings (rate 0.5) | Gradient 1.1e-02 at layer 1, 1.6e-03 at layer 16 (6.9 times, spoken "about seven"); signal 0.18 to 0.96 (5.4 times); epoch 1 loss 52.2632, epoch 10 2.44455; 58.85% | replayed, displayed |
| Same network at rate 0.1 | Epoch 1 loss 3.01616, epoch 10 0.119504; 91.05% | replayed, displayed |
| Same network, 40 epochs at rate 0.5, decay 0.9 | About 64% (63.95% scratch) | replayed (spoken: "only 64 percent") |
| Residual rate sweep, 10 epochs, decay 0.9 | 58.85%, 86%, 87.75%, 91.05%, 92.1% at rate 0.5, 0.3, 0.2, 0.1, 0.05 | scratch |
| Residual at rate 0.5, 20 epochs, or decay 0.5 | 60.05%; 37.95% | scratch (more epochs do not rescue rate 0.5) |
| Residual at rate 0.1, 20 and 40 epochs | 92%, 92.15% | scratch |
| Aside table | Probability to loss (0.99 to 0.01, 0.5 to 0.69, 0.1 to 2.30, 0.01 to 4.61, 0.000001 to 13.82, 2e-23 to 52.27); the score-gap table was cut in the second rewrite | replayed (every cell recomputed) |
| Epoch 1 (tanh, rate 0.5, seed 42), every training image re-scored | After epoch 1 all 10,000 are predicted as 0 (mean top probability 0.9998); 131 of 157 batches give one digit to at least 80% of images, a different digit from batch to batch; 100% of tanh outputs in the 15 residual layers have absolute value above 0.99 (0% at the start); image-to-image spread of the last residual layer 0.07 | scratch, NOT yet replayed by verify-script.mjs |
| Why saturation hides the image (tanh, 64-image batch, average over the 15 residual layers) | Start: weight rms 0.10, pre-activation rms 0.29 (image part 0.23, constant part 0.17), 99.8% of units change sign between images. End of epoch 1: weight rms 1.86, bias rms 0.90, layer input constant part 2.36 against image part 0.23, pre-activation rms 83.2 (constant 83.2, image 2.5), 0% of units change sign | scratch, NOT yet replayed by verify-script.mjs |
| Recovery as the rate decays from 0.5 to 0.19 | Collapsed batches per epoch 131, 60, 22, 10, 9, 2, 0, 0, 0, 0; distinct digits predicted 1, 3, 3, 4, 4, 4, 6, 7, 7, 7; tanh outputs still above 0.99 at epoch 10 (99.96%); test accuracy 58.85% | scratch, NOT yet replayed by verify-script.mjs |
| Epoch-1 loss 52.2632 corresponds to a correct-digit probability of about 2e-23 | exp(-52.2632) = 2.0e-23, 22 zeros after the decimal point | replayed |
| First twelve batches at rate 0.5, seed 42 | Largest score about 345, batch losses up to 135.9, loss within ln(10) of the mean score gap on every batch (a mathematical bound), accuracy 9.5% (73 of 768) | replayed (spoken: "scores reached the hundreds", "near chance") |
| Residual starting loss | Above the plain network's 2.30259 (2.384), so "the starting scores are too large" | replayed in the harness |
| Residual scale 0.3 on each correction (idea removed by the creator) | 92.7% at rate 0.5; sweep 86.85% (0.5), 92.65% (0.2), 91.45% (0.1); a learned scale started at 1.0 crashes, at 0.3 gives 92.35%; seeds 1, 7, 42 give 92.95%, 91.6%, 92.7% against crash, 82.2%, 58.85% unscaled; scaled gives 78.2% at rate 1.0 and 90.65% at rate 0.1 | scratch; not in the script |
| Residual, 40 epochs, rate 0.05, no decay | Final loss 0.00104, 93.15% | replayed (spoken in Section E) |
| Unscaled residual at 10 epochs, seeds 1 and 2 (rate 0.1, decay 0.9), first draft | 91.35%, 90.95% | scratch; measured before revision 2 |
| Plain at 16 and 32 layers, constant rates 0.1 to 1.0, 5 and 10 epochs, three seeds | Stuck at 2.30 in every run (10.25% to 11.7%) | scratch |
| Residual at 32 layers | 85.35% at 5 epochs | scratch |
| Residual, 40 epochs, seeds 1 and 2 | 92.85%, 93.25% | scratch |
| 8, 12, 24 residual layers at 10 epochs | 92.2%, 91.8%, 89.45% | scratch |
| ReLU instead of tanh (16 residual layers, 10 epochs) | 77.75% (83.45% at rate 0.05) | scratch; the creator's live model uses ReLU |
| Weight decay 0.001 or 0.0001 at 40 epochs | 92.8%, 92.55% | scratch; not used |
| 30,000 and 60,000 training images, 10 epochs | 94.2%, 95.2% | scratch; belongs to the next episode |

## Runtime estimate

Estimated at 2.5 spoken words per second, 3 seconds per newly typed line,
0.5 seconds per pasted or repeated line, about 15 seconds per run and about
25 seconds to read each output. These are planning numbers, not a rehearsal.

| Section | Spoken words | New code lines | Estimated end |
| --- | ---: | ---: | ---: |
| A. Look inside | 461 | 48 | 4:45 |
| B. Sixteen layers | 283 | 54 | 8:30 |
| C. Residual connections | about 330 | about 40 | 12:30 |
| Aside: What the loss measures | about 330 | 0 | 13:30 |
| D. Lowering the learning rate | about 170 | 1 | 15:00 |
| E. What is left | about 70 | 0 | 15:45 |
| F. Recap | about 115 | 0 | 16:30 |

Revision 2 adds Section D and the aside, so the projected cut is now about 15 to
17 minutes, above the 10-15 minute target; the aside (about 330 words, one
table) is the first thing to trim or move to a pinned comment or a separate
video. These are planning numbers
from the narration word count, not a rehearsal. The pace table above is the
first draft's and the section rows C to F are re-estimated by hand. If a rehearsal runs long, shorten Section D first, then the
`print_signal` explanation, not the reasoning in Section C.

Milestones as upper bounds: first edit about 0:30; first table (four edits and
a run) about 4:30; sixteen-layer failure about 8:00; residual result about 12:00.

## Design decisions

0. **Why root mean square for the signal.** A layer's output is a list of values,
   so the report needs one typical size. A plain average cancels positives and
   negatives, so the script says why it squares first, averages, and takes the
   square root (the root mean square), which is independent of layer width. The
   narration deliberately omits variance and standard deviation. Context for the
   creator: with a mean of zero, the root mean square equals the standard
   deviation, and the starting weights (uniform in plus or minus 1 over the
   square root of the input count) make each Linear layer multiply it by about
   0.58, close to the measured 0.57. The zero-mean condition was not checked.

1. **Report on top-level layers.** `forward_traced` records the output of each
   layer in the Sequence. Making `Sequence` a `Layer` and wrapping each Linear
   and tanh pair as one `hidden_layer` means one table row per hidden layer. The
   first table (the existing flat network) still lists Linear and tanh rows
   separately, which the narration uses: tanh leaves the size alone and each
   Linear shrinks it.
2. **Plain, non-template `Residual`.** It holds a `unique_ptr<Layer>` body, like
   `Sequence` holds layers. It requires the same input and output shape, so the
   first hidden layer (784 to 32) is not wrapped. The narration says so.
3. **Rate 0.5 with decay 0.9, 10 epochs (creator direction, revision 2).** The
   first draft used rate 0.1 because higher rates hurt the unscaled residual
   network. The creator keeps 0.5 (their live value) and wants the episode to
   show that growth, then fix it. The residual network reaches 58.85% at 0.5
   (91.05% at 0.1); Section D lowers the rate to 0.1. Keeping decay shows that the
   previous episode's fix does not rescue the plain network.
4. **No momentum, velocity or Adam.** Creator direction; they open the next
   episode, where training on more data (94% to 95% in scratch tests) gives them
   a concrete job.
5. **40-epoch figure as spoken evidence only.** Replayed by the verifier but not
   shown live, per the creator's direction that 40 epochs is too long.

## Keyword audit of the actual narration

| Term | Spoken in | Result |
| --- | --- | --- |
| C++ neural network, MNIST | Cold open, first sentence | Present. |
| debugging gradients | Cold open, second sentence | Present. |
| layer by layer, signal, gradient | Cold open; Section A before and after the first table | Present. |
| vanishing gradient | Section B, after the sixteen-layer table | Present once, at the point it is explained. |
| residual connection | Cold open; Section C where it is defined; recap | Present. |
| deeper network, sixteen layers | Sections B and C | Present. |

Recheck the captions after recording.

## Checklist audit

| ID | Status | Points | Evidence and repair |
| --- | --- | ---: | --- |
| L01 | PASS | 10/10 | The opening states the failure (stops learning), the tool and the fix; the question is answered by the first table and the residual run. Boundary: no optimizers, no new data. |
| L02 | PASS | 10/10 | The first sentence names the C++ network and MNIST before the limitation; the next two say what was tried and where it fails; the title overlay is specified. Thumbnail and title alignment stays pending until packaging exists. |
| L03 | PASS | 8/8 | 76 spoken words before the first edit, about 0:30 at 2.5 words per second, which is the outer target. Needs rehearsal; any added setup pushes it over. |
| L04 | PARTIAL | 4/8 | The report has to be written before it shows anything. First measured insight is about 4:30 (four edits, then the table). Repair options: cut the `print_signal` preview, or show a hand-drawn table of the expected pattern first (not done, because it would be an unmeasured claim). |
| L05 | PASS | 8/8 | Each section adds a capability: a report, a verified failure of plain training at sixteen layers, a residual layer that fixes it. |
| L06 | PASS | 8/8 | Each type appears at its use with a preview; `Residual` follows the failing table. |
| L07 | PASS | 8/8 | The reasons for a traced forward pass, a nested `Sequence`, the shape restriction on `Residual`, and why addition keeps a gradient path are spoken beside the code. The path claim is supported by the displayed gradient column. |
| L08 | PASS | 10/10 | 11 edits replayed against the frozen source, three checkpoints run, 59 displayed output lines matched, plus unit checks and sanitizers. |
| L09 | PASS | 6/6 | Every run answers a question; correctness, equivalence and finite-difference checks stay off camera. |
| L10 | PASS | 5/5 | Directions name the function, region or output column. Rendered highlighting is unverified. |
| L11 | PARTIAL | 2.5/5 | Connected narration, but Section A (461 words) carries four edits before the first result and the 16-line model blocks need stable screen time. A timed read is required. |
| L11a | PARTIAL | included | Estimated 12.5 to 14.5 minutes, inside the range but at the top. |
| L12 | PASS | 4/4 | Delivers the tool and the fix, names the remaining limit, and ends with a concrete next list. |
| L13 | PASS | 4/4 | Recap, three next-episode items, exact sign-off, clean tail. No Q&A. |
| L14 | PASS | 2/2 | `script.md` contains only recording material. |
| L15 | PASS | 2/2 | Keyword research precedes the narration; the audit above found each selected term at a natural moment. |
| L16 | PASS | 2/2 | Evidence, conditions and limits are stated; no reach claim, analytics refresh or publication step is implied. |

## Critique

1. **The first payoff comes late (L04).** The tool has to exist before it shows
   anything, so the viewer waits through four edits. The cold open promises it
   and the table delivers it, but a viewer who leaves at 1:00 sees only code.
   Next repair if rehearsal confirms the delay: shorten the narration before
   `print_signal` and make that edit the only one before the first run.
2. **Section A's first table is a noisier picture than the later ones.** The
   flat eight-layer network lists Linear and tanh rows separately, so the signal
   column repeats each value. The narration turns that into a point (tanh does
   not shrink the signal), but a viewer may need a second look. Switching to
   `hidden_layer` first would give a cleaner table at the cost of a later first
   payoff.
3. **The residual run starts above the guessing loss.** Epoch 1 is 3.02, higher
   than 2.30. The script names the reason (the larger starting scores, backed by
   the signal column) and moves on. This is a visible wrinkle, not a hidden one.
4. **The 40-epoch claim is not shown on screen.** It is a measured fact the
   verifier replays, but the viewer cannot check it in the video. The narration
   says it was run offline.
5. **Fifteen identical lines appear three times** (the plain list and the
   residual list). This follows the creator's requirement that layers be listed
   explicitly, but the screen time for those blocks is a pacing risk.
6. **Continuity with Chapter 13's closing list** needs a creator decision (see
   History).

## Verification and remaining checks

- `node youtube-series/chapter-14/verify-script.mjs` (frozen baseline, no flags)
  replays all edits, matches every displayed output line, runs the narration
  lint, the unit checks (`hidden_layer` equals the flat list bitwise, traced
  forward equals forward, `Residual` equals input plus body with finite
  difference gradients, nested `Sequence`), the signal and gradient assertions,
  the three rate variants, the 40-epoch run and an ASan and UBSan run of the
  final source. The creator's `main.cpp` is not modified. The last run passed.
- Not verified: a timed spoken rehearsal, rendered legibility of the table and
  the 16-line blocks, the thumbnail and title alignment, the creator's live code
  reconciliation, and results on other machines or seeds for the displayed runs.

## Final score

93.5/100. Decision: rework. L04 is a mandatory check and is partial, so the
rubric does not let the total average it away. The gap comes from the order the
tool requires and is repairable by tightening Section A or by accepting the
later first payoff as a recorded tradeoff. L11 and L11a await a timed read. This
is sequential self-review against a verified implementation, not audience
validation. No thumbnail, recording, publication or release is approved by this
score.

## Revision 2: gradient growth and the learning rate

Creator direction, in order: keep the learning rate at 0.5; after the first
residual run (58.85%), show that the gradient no longer vanishes and in fact
grows; reach a good test accuracy. A constant scale on each residual correction
was drafted and measured (92.7% at rate 0.5), then removed at the creator's
direction: it depends on knowing the number of layers in advance, interacts with
the learning rate, and belongs in a later episode. The ending uses the two
levers the creator named, a lower learning rate or more epochs. The creator also
asked for an aside that explains the loss numbers: why 2.30 is guessing, how
52 ties back (confidently wrong), and the cross-entropy and negative log
probability mechanics. It sits between Section C and Section D so both numbers
are already on screen.

What the measurements say about those two levers (unscaled network, seed 42):

- Lowering the rate works: 86% at 0.3, 87.75% at 0.2, 91.05% at 0.1, 92.1% at
  0.05 (10 epochs, decay 0.9). The script uses 0.1, the value the first draft
  already verified.
- More epochs at rate 0.5 does not: 60.05% at 20 epochs and 63.95% at 40 (a
  faster decay of 0.5 gives 37.95%). The narration says this, so the viewer's
  obvious "just train longer" question is answered by a run.
- The scale idea is a known technique (residual scaling in Inception-ResNet,
  ReZero, Fixup, LayerScale), but it is a separate topic. LayerNorm, which is
  usually paired with residual connections in transformers, does a related job
  (keeping activation size under control) in a different way and is also left
  out.

Consequences for the checklist: the L01-L16 audit and the final score above were
scored on the first draft and were not recomputed for revision 2. The first
payoff (L04) is unchanged. Section D adds about a minute, so L11 and L11a
(runtime) need a fresh timed read, and the Chapter 13 closing list and the
"next episode" list should be rechecked. A trailing-whitespace lint failure on
line 17 of the script (the cold open) was fixed.

The second aside rewrite (creator request: explain the 52, what it implies, the
tanh link, why the image is ignored, and the rescue by decay, without showing the
10,000-image data on camera) replaced the score-gap table with narration. Its new
causal claims were measured in scratch runs and are listed in the evidence table
as not yet replayed. The verifier was edited to match the new text and then re-run on
2026-10-22: 26 edits replayed, the six-row aside table, the first-epoch probe and
the ASan/UBSan run passed. The new causal claims in the evidence table above are
still not asserted by the verifier.

## Recording divergence (October 22, 2026)

The recorded export ends at a starting rate of 0.08, decay 0.95 and 20 epochs
(92.85%, 1857/2000, visible at 49:05), where this script ends at 0.1, 10 epochs
and 91.05%. The export is 52:24 long. The verifier replays the script, not the
video, so its results do not describe the published media. The publishing
package follows the video; see [publishing.md](publishing.md).
