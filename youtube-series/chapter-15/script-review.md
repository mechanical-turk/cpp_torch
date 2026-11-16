# Chapter 15 preparation and review

Script: [script.md](script.md). Keyword research: [keyword-research.md](keyword-research.md).
Verifier: [verify-script.mjs](verify-script.mjs), last run in `verification/last-run.txt` and
`verification-run.json`. Experiments: `docs/logs/content-experiments.md` (2026-10-26 to 2026-10-28),
code and raw runs in `youtube-series/experiments/ch15-momentum-regime/` (PyTorch screens, untracked)
and `youtube-series/experiments/ch15-cpp/` (C++ replays, untracked).

## History of this script

- Creator direction (2026-10-27/28, in order): find a regime where plain SGD is measurably worse than
  momentum, on any network, keeping MNIST; then a regime where momentum is worse than Adam, "based on
  observations we can make in the episode"; limit time spent on Adam; "we don't need to use the existing
  residual network"; then "go ahead and write the script".
- Chapter 14's recorded ending promised "training on more data", "momentum and velocity" and "hopefully
  the Adam optimizer" (captions, final minute). This episode delivers momentum and Adam only. **Scope
  change:** training on more data moves to a later episode (named in the next-episode list). The
  creator chose the optimizer focus; it is recorded here as an L01 scope note.
- The network changes from Chapter 14's sixteen residual tanh layers to one hidden layer of 256 ReLU
  units, so runs take 15 to 80 seconds in the series' own engine. This follows the creator's
  "we don't need to use the existing residual network".
- Starting code: the checked-in Chapter 14 `main.cpp` (git `47db7ed`, identical to
  `verification/episode-14-baseline.cpp`, compared byte for byte). Chapter 14's script.md is stale and
  was not used.

## Scope and checklist plan

| ID | Plan for this draft |
| --- | --- |
| L01 | Promise: add momentum and Adam to the MNIST network and measure how much faster each trains than plain stochastic gradient descent. Curiosity question: does remembering past steps help, and by how much. Limitation: plain gradient descent forgets each gradient. Distinctive benefit: all three optimizers are written from scratch in about thirty lines and compared on the same network, with the weak spots shown (batch 64, a narrow learning-rate window). Scope boundary: no theory of Adam, no AdamW, no more data. |
| L02 | First sentence names momentum, the Adam optimizer and stochastic gradient descent and the comparison. Title overlay on the open `train_mnist` for five seconds. Thumbnail alignment is PENDING until packaging exists. |
| L03 | The first action is the model edit at about 0:25, which creates the test bench every later result depends on. |
| L04 | The first delivered result is the baseline run at about 3:30. This misses the one-minute target; see audit. |
| L05 | A test bench with settings as constants; momentum; Adam; the batch-64 check; a data-side fix. |
| L06 | Momentum's rule is spoken before its code; Adam's preview is two sentences and its corrections are explained while typing; the settings constants arrive when many runs are needed. |
| L07 | Every update rule is narrated from the line on screen; the reasons for dropping decay and for the 0.1 added to the spread are spoken. |
| L08 | Every edit has exact Before/After against the checked-in code; `verify-script.mjs` replays all 25 and compiles and runs every command. |
| L09 | Every run shows loss and test correct count; the learning-rate table and the multi-seed claims are recomputed by the verifier. |
| L10 | Directions name the block or line to select; the learning-rate table is the one planned overlay. |
| L11 | Short connected sentences; one aside (data-side fix) marked as first to cut. L11a: see runtime estimate. |
| L12 | Delivers the promised measurements and states what is not explained. Ends with a concrete next list. |
| L13 | Itemised recap, three-line next list, exact sign-off, five clean seconds. |
| L14 | Filename first, one `>` narration, directions separate. |
| L15 | Keyword map in keyword-research.md; spoken terms audited below. |
| L16 | Evidence limits below; Shorts techniques not used. |

## Evidence

What the episode shows (all from the script's own C++ code, verified):

- Batch 250, five epochs, raw pixels: plain SGD at its best rate 1.0 ends at loss 0.162 (1,826 of 2,000
  test images); momentum 0.9 at 0.316 ends at 0.077 (1,875); Adam at 0.01 ends at 0.051 (1,873).
- Learning-rate window (table, one starting weight set): SGD 1.0 gives 0.162, 1.78 gives 2.14, 3.16 and
  above stop with an infinite loss; Adam stays under 0.08 for four of seven rates tried.
- Batch 64, two epochs: SGD 0.562 gives 0.219 (1,833), momentum 0.1 gives 0.209 (1,785).
- Standardised pixels, batch 250, five epochs: SGD 0.052 (1,872), momentum 0.031 (1,866).

Narrated claims beyond the displayed runs, replayed with other starting weights (seeds 1 to 5):

- Momentum's loss is 0.48 to 0.65 of SGD's (batch 250); Adam's is 0.57 to 0.71 of momentum's.
- At batch 64 momentum gets fewer test images right than SGD on all six starts (five seeds plus the
  shown run).

Limits that belong in the review and, where noted, in the narration:

- Single dataset slice: the first 10,000 training images, in file order, first 2,000 test images.
- Each optimizer's learning rate was tuned by a seven-value sweep (narrated and tabulated). The
  result is sensitive to the exact rate: momentum at 0.316 ends at 0.0769, at 0.316228 at 0.0841 (a
  harness run). The displayed rates are the ones the verifier replays.
- The PyTorch screens that located the regimes (S1 to S11, `docs/logs/content-experiments.md`) are
  not shown on screen. They used float32, random batches and a different initialiser, and some of
  their conclusions did not carry over: Adam beat momentum clearly only with a mean-squared-error loss
  and standardised inputs at full batch, not under the series' cross-entropy; momentum's gain over
  SGD at batch 256 was 1.86x to 2.15x in steps to a loss target (below the 2x rule fixed in advance).
  The episode therefore makes loss-after-fixed-epochs claims only.
- Why momentum or Adam wins here is **not established**. The hypothesis I pre-registered (Adam wins
  because per-weight gradients differ by about 1,400x) was refuted in S8 and is not in the script.
  The batch-64 gap is explained in narration only as "a common explanation ... we haven't tested that".
- Adam's test count (1,873) is not higher than momentum's (1,875) on the shown run; the narration says so.

## Runtime estimate

Narrated words: see `verification-run.json` (1,146 on the final script). Edits: 22 Before/After blocks (verifier
count), of which four are substantial (small network, momentum_step, adam_step, pixel statistics) and
eighteen are one to five lines; eight of those only change the settings constants between runs. Seven runs are shown; each takes 15 to 80 seconds of machine time.

Calibration from the two recorded episodes (2.0 to 2.3 minutes per edit; Episode 13: 13 edits, about 30
minutes; Episode 14: 26 edits, 52 minutes) projects **44 to 50 minutes** for 22 edits. That calibration
mixes heavy and light edits; if the eighteen light edits cost closer to half a minute each, the total
falls near 21 to 26 minutes. Neither figure is measured for this script. **This is a named runtime risk
for L11a and the 15 + 5 + 10 minute budget.** Cut order if rehearsal runs long: (1) section E,
the data-side fix (7 blocks, about a quarter of the narration), (2) the learning-rate table overlay,
(3) the batch-64 section. Cutting E leaves 15 blocks. A rehearsal that times the settings edits is
the cheapest way to settle the estimate.

## Design decisions

- Command-line settings (7 light edits) replace retyping constants for seven runs. The optimizer branch
  carries its final validation (`unknown optimizer` throws) from the first edit, so no temporary
  whitelist is written and later replaced.
- Learning-rate decay is removed on camera so that each optimizer has one fixed rate; the reason is spoken.
- Loss after a fixed number of epochs, not steps to a target, because the series' loop reports epoch
  loss and a full-batch or large-batch demonstration is impractical in this engine (about 16 seconds
  per full-batch step, measured).
- Plain SGD, momentum and Adam each use their own tuned rate; the table makes that tuning visible.
- Adam's update is written in one statement with named corrections, no helper abstraction.
- The data-side section is last and marked cuttable.

## Keyword audit of the actual narration

- "stochastic gradient descent" spoken in the opening sentence, then "plain gradient descent" and the
  recap's "plain gradient descent": the abbreviation SGD appears only in code, commands and the table.
- "momentum" and "the Adam optimizer": opening sentence, section headings' spoken lead-ins, recap.
- "velocity": spoken once in the momentum preview and again while writing the body, tied to the lists
  named `velocities`.
- Primary phrase "momentum and Adam optimizer from scratch in C++": the title carries it; the narration
  says "Today we add momentum and the Adam optimizer to our MNIST network" without reciting the title.
- No keyword repetition beyond what the lesson names. Captions must be rechecked after recording.

## Checklist audit

Points are awarded against the exact draft. PASS full weight, PARTIAL half.

| ID | Status | Points | Evidence and repair |
| --- | --- | ---: | --- |
| L01 | PASS | 10 | The opening names the three methods and the measurement; "Momentum remembers" supplies the curiosity; scope change recorded above. |
| L02 | PARTIAL | 5 | First sentence and overlay are in the script; the thumbnail-title-opening comparison is pending until packaging exists. |
| L03 | PASS | 8 | The model edit begins within about 25 seconds and the next seven blocks build the bench. Time not measured; repair at rehearsal. |
| L04 | PARTIAL | 4 | First delivered result is the baseline loss at about 3:30 (estimate). Repair: record the real time at rehearsal; if the bench edits run long, start the baseline run earlier by deferring the decay edit. |
| L05 | PASS | 8 | Each section ends with a runnable capability: bench, momentum, Adam, diagnosis, standardise. |
| L06 | PARTIAL | 4 | Momentum and the command line arrive with a spoken need. Adam's preview is two sentences but the bias-correction reasoning still lands in a spoken block of about 40 words while a large function is typed; a rehearsal should check whether it reads as one natural passage. |
| L07 | PASS | 8 | Each update rule is narrated from the line on screen; the decay removal and the 0.1 are explained. |
| L08 | PASS | 10 | `verify-script.mjs` replays all 25 edits against the evolving source, TensorNode unchanged, and compiles and runs all seven displayed commands. |
| L09 | PASS | 6 | 15 displayed output lines match real output; the 21-cell table and the multi-seed claims are recomputed; full tests stay in `main`. |
| L10 | PARTIAL | 2.5 | Directions name what to select, but only the table overlay is a designed visual. Repair at the visual plan stage; legibility is unverified until recorded. |
| L11 | PARTIAL | 2.5 | The narration is short and connected, but the projected runtime is outside 10 to 15 minutes and unmeasured (see estimate); delivery has not been rehearsed. |
| L12 | PARTIAL | 2 | The measurements are delivered and the limits stated, but the main result (why momentum and Adam help) is not explained, and no explanation was invented. |
| L13 | PASS | 4 | Itemised recap, three-line next list, exact sign-off, clean tail. |
| L14 | PASS | 2 | MP4 filename first, one `>` narration, directions and output blocks separate. |
| L15 | PASS | 2 | Research dated before drafting; spoken terms audited above. |
| L16 | PASS | 2 | Evidence limits, refuted hypothesis and unmeasured items are stated; no Shorts transfer. |

## Critique

1. **Runtime is the largest risk.** Projected 20 to 44 minutes against a 15 + 5 plan and a 30 cap, by the
   only calibration available. The repair is scope, not speed: cut section E first. Consequence if
   ignored: another recording well past the budget, as in Episode 14.
2. **The episode shows that momentum and Adam help here but cannot say why.** That is honest, but the
   viewer is left with a measurement and two general mechanisms. Consequence: some viewers will want
   the cause. Next repair: one measured mechanism experiment, only if the creator wants it.
3. **First payoff late.** The baseline result arrives around 3:30, not one minute. The bench edits are
   eight blocks of setup before any optimizer is compared.
4. **The learning-rate tuning is a hidden lever.** The results depend on each method's tuned rate and
   are sensitive to its exact value. The table and the narrated sweep disclose it; the recording must
   keep the table on screen long enough to read.
5. **Single data slice and a file-order batch loop.** Statements are limited to this setup.

## Verification and remaining checks

- Verified by `verify-script.mjs` (see `verification/last-run.txt`): voice lint; 25 edits replayed
  against the checked-in Chapter 14 source with unique Before blocks; seven commands compiled and run
  with matching displayed output lines; the 21-cell learning-rate table; narrated ranges over seeds 1
  to 5 (momentum/SGD 0.48 to 0.65, Adam/momentum 0.57 to 0.71); batch-64 test counts on six starts.
- Not verified: spoken rehearsal, measured runtime, rendered legibility of the table overlay, thumbnail
  and title alignment, captions, and the creator's recording checkout (the verifier never touches it).
- The standardise section compiles and runs in the replay, but its claims are limited to the displayed
  runs; no multi-seed claim is made for it.

## Final score

Most important remaining weakness: the projected runtime, unmeasured, probably above the budget.

Score: 80/100. Decision: rework (mandatory checks L02, L04, L06 and L12 are PARTIAL).

## Revision 2026-11-09: command-line segment removed

The creator judged the command-line settings and the not-compiling step wasted time. The script now keeps
OPTIMIZER, learning_rate, BATCH_SIZE and EPOCHS as constants above the epoch loop (one edit), and each run
changes only the constants it needs before recompiling. `train_mnist` and `main` keep their original
signatures. Narration is 1,118 words. Counts above were updated from 19 to 22 edits; the runtime risk is
slightly higher by the calibration. Bulk verifier runs (table, seeds) use a copy whose constants are read
from argv; displayed runs use the unmodified edited code. The checked-in demo `main.cpp` is currently
modified, so the verifier warns that it differs from the frozen Episode 14 baseline copy.

## Revision 2026-11-10: trace-reading walkthrough for momentum

Added from the creator's own trace experiment (reproduced exactly by the replay): a trace-end edit (trace on
first and last batch), the SGD trace reading, momentum at the same rate 1.0 (loss 0.499629, 1,642/2000), a
divide-by-ten step (0.1: loss 0.171738, 1,832/2000), and the choice of 0.316 from the sweep. Now 25 edits
and nine displayed runs; narration 1,410 words. By the 2.0 to 2.3 minutes per edit calibration this projects
50 to 58 minutes, or roughly 25 to 30 if the 21 light edits are fast; neither is measured. The runtime risk
for L11a is higher than the 44 to 50 minutes recorded above; cut order is unchanged and the new
momentum-rate walkthrough adds three runs and three edits to section B.
Evidence limits: the trace values come from one seed; "the velocity approaches ten times the gradient" is
arithmetic for steady gradients, not a measured cause; the sweep claim (0.178 and 0.316 better, 0.562
worse) rests on the verified table cells. The script makes no claim that gradients explain momentum's gain.
Full verifier run passed (25 edits, 28 output lines, 21 table cells, seed ranges 0.48 to 0.65 and 0.57 to 0.71).

## Revision 2026-11-11: Adam built in four steps, 1.78 explained

Adam's `adam_step` is now built in four edits (first moment, second moment, divide by the root of the second
moment, bias correction) instead of one large block. The final function is unchanged, and the Adam run still
prints loss 0.0510026 and 1873/2000. The script now has 28 edits; the three added blocks are small and the
recorder types only the new lines, so the 2.0 to 2.3 minutes per edit calibration likely overstates them, but
runtime is still unmeasured. The 1.78 learning-rate spacing is explained in the narration as a chosen grid
(four steps per factor of ten), not a derived value. Quick verifier passed (28 edits, 28 output lines); the
full table and seed check was last run before these two changes.

## Revision 2026-11-12: standardise section removed, Adam step number tested

- Section E (per-pixel standardising) removed at the creator's request; its text is kept in
  `verification/removed-section-E-standardise.md`. The recap now follows batch 64. Section D (batch 64) was
  not named and was kept; it is the next cut if runtime needs it.
- Adam is built from a copy of `momentum_step`, then in small steps. It is first run WITHOUT the step number
  (seed 42: Epoch 1 loss 1.18179, Epoch 5 0.134096, 1823/2000), then the first-step arithmetic is walked
  through, then the correction and a step counter are added (Epoch 1 0.550623, Epoch 5 0.0510026, 1873).
- Evidence (stored in `youtube-series/experiments/ch15-adam-bias/`, six starts, rate 0.01, batch 250, five
  epochs): without the step number the final loss is 0.087 to 0.134, with it 0.050 to 0.056, worse without
  every time; at rates 0.056 and 0.1 the uncorrected program stopped on all six starts. The uncorrected step
  is c1/sqrt(c2) times the corrected one, for a steady gradient: 3.16 at step 1, 6.53 at step 10, 3.24 at step 100.
  Corrects an earlier wording that called the averages "too small" without saying the steps come out too big.
- Limits: the cause is shown by the arithmetic and by the loss spiking in the first steps of one seed, not by a
  separate measurement of step sizes; the six-start ranges come from the stored runs.json, which the verifier
  reads and does not recompute.
- Now 24 edits, 8 runs, narration 1,720 words (the Adam explanation is longer). Runtime is unmeasured; by the
  calibration this is still a risk. Full verifier passed (24 edits, 28 output lines, 21 table cells, seed
  ranges, step-number claims). The earlier counts in this file (19, 22, 25, 28 edits) are superseded.
