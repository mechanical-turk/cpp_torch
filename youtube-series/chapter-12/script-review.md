# Chapter 12 script review

Current review: **September 15 three-setup comparison**, at the end of this file.
Earlier loading approaches, subset results and scores are retained as history,
not instructions for the current script.

## Source, scope and plan

Read actual main.cpp and git history at Chapter 10 public HEAD 1535f54 with
the creator's uncommitted Chapter 11 implementation. Freeze that actual source
for edit replay. Do not change the recording repository.

Chapter 11 promises MNIST, mini-batches, classification loss and accuracy.
The new script fulfills these with a small 784-32-10 MLP and real MNIST subsets,
not another XOR example. [Keyword research](keyword-research.md) precedes drafting.

| ID | Plan |
| --- | --- |
| L01 | Train the existing C++ network to recognize handwritten digits and measure held-out accuracy. |
| L02 | Show a real MNIST image, explain its pixels as inputs; no series recap. |
| L03 | Write the 784-input, 10-output model immediately after the anchored hook. |
| L04 | Show a concrete forward call producing ten scores for an image by about one minute; no claimed trained result. |
| L05 | Progress: image to scores, loss with gradient, mini-batch reader, training, test accuracy. |
| L06 | Introduce classification loss after explaining the ten scores; cached derivatives only for this loss; batch structure only when reading data. |
| L07 | Explain why digit labels are classes, softmax normalization, stable exponentials, mean reduction and probability-minus-target gradient. |
| L08 | Exact Before/After edits against frozen recorded code; forward and backward together before running. |
| L09 | Verify finite differences, extreme logits, invalid inputs, last batch, source preservation and real MNIST training outside recording. |
| L10 | Point to image pixels, score columns, correct label, data/gradient indices and held-out result. |
| L11 | Target 10-15 minutes; concise narration and approximately 200 new lines, with no generic loader framework. Reassess after drafting. |
| L12 | Show held-out accuracy and concrete predictions; no invented percentage or promise of production readiness. |
| L13 | Itemized recap, next-step list, standard sign-off and clean tail. |
| L14 | Script contains only narration, literal edits and scene cues; review/research separate. |
| L15 | Use the researched technical terms naturally, not as a spoken keyword list. |
| L16 | Record measured vs estimated evidence; code tests are not audience validation. |

Dataset preparation may supply plain text rows and an unaltered example image.
The on-camera C++ code must read, normalize, batch, train and evaluate them.
Use fixed deterministic training ordering to keep the loader compact, disclose
it as a simplification rather than implying per-epoch shuffling. Do not tune
hyperparameters on the held-out test set.

## Audit and critique

### Changes made during review

The first draft put the reader before the first forward pass. It delayed the
visible payoff with file handling. The revision starts with the actual image's
784 supplied pixel literals, normalizes them on camera and runs the existing
MLP before the reader. The literals contain no hidden implementation. The
untrained preview remains useful in the final example, rather than becoming
a throwaway failed test.

The final opening has about 120 spoken words through the first run. Meaningful
model construction starts after roughly 15 seconds; by 30 seconds the presenter
should be explaining dimensions while writing. The first ten-score output is
planned near one minute, with coding and speech overlapping. These are rehearsal
targets, not measured edited timing. Do not add a separate shape lecture or
read every pixel.

Cross-entropy and its backward rule are both complete before any use. The loss
caches its local derivative in forward; backward multiplies by the incoming
gradient. Labels are metadata, not differentiable parent Tensors. This is a
fused, first-order operation, not a general softmax API or higher-order autograd.
The score tensor remains its single parent.

The data reader consumes the fixed supplied whitespace format, validates labels
and pixels, normalizes in C++, accepts a smaller last batch and reports broken
image records. It is not a general-purpose CSV or hostile-input parsing library.
Training uses fixed shuffled order and plain gradient descent. No optimizer or
per-epoch shuffle framework is smuggled into the lesson.

### Verification

[verification-run.json](verification-run.json) records actual compiler runs.
All twelve exact Before/After edits replay against the recorded Chapter 11
baseline. Baseline, image preview and completed-loss stages run with ASan/UBSan.
Training and held-out evaluation run with normal -O2; a separate sanitizer
harness checks the new loss, graph integration, batches and accuracy.

- 33 finite-difference comparisons cover the loss scores and all parameters of a small MLP.
- Checks cover mean reduction, translation invariance, large logits, invalid shapes/labels/nonfinite scores, repeated backward accumulation and incoming-gradient scaling.
- Batch checks cover normalized values, label alignment, EOF, incomplete records, invalid labels, the partial final batch, and the 10,000/2,000 file counts.
- Argmax/accuracy checks cover both correct and incorrect answers.
- Dataset archives match the published Torchvision MD5s; selection keeps the official training and test partitions separate.
- Fixed experiment: 784-32-10 tanh MLP, seed 42, batch size 64, five epochs, learning rate 0.1. No hyperparameter search on the held-out set.
- Mean training loss: 0.985, 0.416, 0.332, 0.292, 0.266.
- Held-out result: 1,809 / 2,000 = 90.45%. This is not the full MNIST test benchmark.
- Both complete training runs reproduce the result locally. Standard-library random distributions may differ elsewhere.
- The recording source remains byte-for-byte unchanged. The frozen file only trims trailing blank lines; the report stores both hashes.

The final opening wording was shortened after the last compiler run. Its code
blocks and edit order are unchanged. The mechanical audit separately records
the narration-reviewed script hash; code results still apply.

### Checklist audit

| ID | Assessment and evidence | Points |
| --- | --- | ---: |
| L01 | PASS: MNIST, mini-batches, classification loss and accuracy fulfill Chapter 11's written ending; source supports the starting state. Final Chapter 11 captions remain unavailable. | 10/10 |
| L02 | PASS: real digit and pixels anchor the recognition promise; no recap or unexplained model reference. | 10/10 |
| L03 | PASS at script level: model construction follows the short hook, with dimensions narrated while typing. | 8/8 |
| L04 | PASS at script level: first real-image ten-score output planned near one minute; verified functional payoff, not a claimed trained result. Timing needs rehearsal. | 8/8 |
| L05 | PASS: image scores -> batch inputs -> classification loss -> training -> held-out evaluation. | 8/8 |
| L06 | PASS: each new function has a spoken purpose before its exact edit; no missing-backward demonstration. | 8/8 |
| L07 | PASS: labels versus regression, stable softmax, probability-minus-target, batch averaging and test isolation explained at their code. | 8/8 |
| L08 | PASS: twelve literal edits replay; actual code differs from the Chapter 11 draft and is preserved as baseline. | 10/10 |
| L09 | PASS: first scores, falling training loss, held-out accuracy, numerical and regression verification. | 6/6 |
| L10 | PASS for directions: image, dimensions, score columns, label, loss and loop locations are named. No final-video legibility claim. | 5/5 |
| L11 | PARTIAL: roughly 1,150 spoken words; estimated 12-15 minutes including coding holds and concurrent narration. First-run timing and natural delivery still need rehearsal. | 2.5/5 |
| L12 | PASS: measured held-out classifier result; saving/loading weights follows naturally. | 4/4 |
| L13 | PASS: recap list, next steps, exact sign-off, clean tail. | 4/4 |
| L14 | PASS: script-only recording document, MP4 filename, marked narration, exact code; review is separate. | 2/2 |
| L15 | PASS: dated keyword map preceded drafting; MNIST/C++/logits/softmax/cross-entropy/test accuracy occur naturally in speech. | 2/2 |
| L16 | PASS: long-form evidence kept separate from Shorts; own test result distinguished from external benchmarks and performance predictions. | 2/2 |

### Remaining critique

The loss is the densest section. It introduces a new objective and its gradient,
so it must not become a rushed tour of loops. Keep the three-line formula visible
while implementing it; explain the correct-class subtraction before proceeding
to backward. Rehearse this passage first. If the complete edit exceeds fifteen
minutes, split scope before recording rather than remove essential reasoning
or quietly accept another twenty-five-minute episode.

The early preview introduces a data-only include. Show the file contains only
pixel literals, explain the normalization while typing and do not turn it into
a preprocessor tutorial. The full runtime loader is still built on camera.

This is sequential self-review, not independent audience validation. The score
does not predict views or establish final-media readiness.

## Final score

Score: 97.5/100. Decision: advance to presenter rehearsal.
Actual voice, 10-15-minute timing and rendered code legibility remain unverified.
No publishing action, source push or upload is authorized by this score.

## Superseding review: explicit image loading

Creator rejected the data-only include: it introduced an unfamiliar technique
without enough context. The earlier claim that this shortcut was an effective
opening is withdrawn. A file containing data rather than code still requires
the viewer to understand how the program reads it.

Plan: anchor the image in MNIST, show its answer and pixels in a text record,
open it with ifstream, read the label separately, then read and normalize 784
pixels before constructing the Tensor and MLP. Preserve the later training
scope and result. The batch reader now explicitly repeats this familiar read
for multiple images. Remove the .inc generator and compiler include-path need.

Audit: L02, L03, L05-L08, L10 and L14 pass this text/code review. There are now
14 exact edits, all replayed successfully. Baseline, image forward, completed
loss, training, held-out evaluation and the 33-check numerical harness pass.
Held-out accuracy remains 1809/2000. The final shortened opening paragraphs
were edited after the compiler run began; code and edit sequence are unchanged.

L04 is now PARTIAL: useful file-reading work starts after roughly 50 spoken
words, but the first full ten-score output comes later than the one-minute
target. Do not claim a near-one-minute run from the superseded draft. L11 stays
PARTIAL pending rehearsal, particularly the total runtime and time spent on
loading. Other checklist statuses remain unchanged.

Critique: the single-image and batch readers share a few lines of parsing.
This repetition is now explicit and provides the transition from one image
to multiple rows. Do not add a parser abstraction or preprocessor trick to
save those lines. During rehearsal, trim repeated narration before considering
any reduction in the explanation of the data format.

Score: 93.5/100. Decision: rework the first-payoff timing in presenter rehearsal.
The context and loading repair is implemented and verified; this is not a
claim that timing or voice has been approved by the creator.

## September 15: original IDX revision, current review

The creator chose to read the original binary dataset. Preparation now only
downloads and decompresses its four archives. The recording builds the reader,
including header decoding, image/label validation and pixel normalization.
One reader supplies the opening image and subsequent batches. No generated
text file, preprocessor data include or duplicate single-image parser remains.

The revised plan puts useful file-reading code immediately after the anchored
image hook. Explain the two files, decode their small headers, read one batch,
and feed its first image into the existing MLP. Then build cross-entropy with
backward, train, and evaluate. This favors a complete, understandable data path
over claiming a ten-score result within one minute.

Training now uses the first 10,000 original training records, in original order
each epoch. Evaluation uses the first 2,000 original test records. Earlier
90.45% results came from different selected records and are superseded, not
evidence that text parsing performs better. No tuning used the test subset.

### Current audit

| ID | Status and evidence | Points |
| --- | --- | ---: |
| L01 | PASS: complete handwritten digit classifier with held-out evaluation. | 10/10 |
| L02 | PASS: actual MNIST digit anchors the task before file details. | 10/10 |
| L03 | PASS: begin the necessary binary reader after explaining its inputs. | 8/8 |
| L04 | PARTIAL: useful work begins early; ten scores require the reader first. | 4/8 |
| L05 | PASS: read images, score, calculate loss, train, evaluate. | 8/8 |
| L06 | PASS: introduce header decoding and batching where used; no data include. | 8/8 |
| L07 | PASS: preserve label semantics, normalization, stable loss and derivative reasoning. | 8/8 |
| L08 | PASS: all 15 exact edits replay; checkpoints and numerical checks pass. | 10/10 |
| L09 | PASS: real scores, decreasing loss and held-out accuracy; separate sanitizer harness. | 6/6 |
| L10 | PASS at script review: image, file headers, score columns and batch rows match narration. | 5/5 |
| L11 | PARTIAL: reader plus cross-entropy remains substantial; 10-15 minutes needs rehearsal. | 2.5/5 |
| L12 | PASS: complete classifier, then weight saving as a concrete continuation. | 4/4 |
| L13 | PASS: recap, next-step list, sign-off and clean tail cue. | 4/4 |
| L14 | PASS at script review: spoken blocks, literal edits and cues only. | 2/2 |
| L15 | PASS: MNIST, C++, classification, mini-batch, cross-entropy and accuracy fit the implementation. | 2/2 |
| L16 | PASS: measured subset result separated from full-MNIST and audience claims. | 2/2 |

### Verification and critique

The verifier replays all 15 edits against the actual recorded Chapter 11 source.
Baseline, image scores, completed loss, training and evaluation pass. The
ASan/UBSan harness passes 33 finite-difference checks plus binary-header,
truncated-record, invalid-label, final-batch, stability and accumulation checks.
Original file hashes and output are in verification-run.json. The live recording
source remains unchanged. Both public Chapter 11 programs also compile/run.

Measured with ordinary C++23 -O2: five epoch losses of 0.994, 0.427, 0.340,
0.299 and 0.272; test accuracy 1764/2000 (88.2%). The updated script displays
these results and instructs the presenter to use the actual recording output.

The loading path is more honest and reusable, but it delays the first neural
network output. Do not add a separate binary-format lecture. Explain the
headers while typing and use the same reader immediately. Runtime and natural
delivery still require presenter rehearsal; source tests cannot approve them.

Score: 93.5/100. Decision: ready for presenter review, not timing-approved.

## September 15: separate reader revision, current review

Creator explicitly moved file parsing out of the lesson. The plan now supplies
mnist_reader.hpp, caps its contract explanation at 30 seconds, and immediately
constructs the image Tensor and MLP in main.cpp. All ML code remains on camera.
The reader returns pixel/label vectors, without depending on Tensor or adding
a generic dataset abstraction. Its full source is available for inspection.

The previous L01-L16 plan/audit still applies except L03-L06 and L11: useful
action and first output no longer wait for implementing header decoding or
stream reads; the brief reader introduction leads directly to the existing
network. L03, L05 and L06 remain PASS. L04 remains PARTIAL until rehearsal
confirms time to the first output. L11 remains PARTIAL until the full edited
runtime is checked. All other awarded points remain unchanged, totaling 93.5.

The reader passage is 53 words, approximately 21-25 seconds at 130-150 words
per minute. This is an estimate, not a measured recording. Do not narrate its
implementation afterward. Exact main.cpp edits now total 11; verification
includes the separate header and records its hash. The numerical expectations
remain unchanged because selection, normalization and training are identical.

Critique: this removes an irrelevant opening detour without hiding the model
implementation. Cross-entropy is now the largest pacing risk; preserve its
explanation and avoid turning the reader overview into a binary-format tour.
Score: 93.5/100. Decision: advance to presenter rehearsal; timing not approved.

## September 15: training-progress revision

Scope: progress output only in the recording script. Keep model comparisons
in experiments/, outside the lesson and the live recording main.cpp. The
current 784-32-10 Tanh setup is a teaching baseline, not a best-known model.

Plan: preserve the L01-L16 plan and add an epoch-start message plus one updating
image-count/running-loss line every 2,048 images and at completion. L09/L10
gain visible evidence that training is advancing; L11 gets one short narration
passage, not a logging abstraction or timing tutorial. All mathematical code,
training data, epochs, architecture and learning rate stay unchanged.

Experiment protocol: compare width, depth, activation, learning rate, shuffling
and epochs in the actual C++ Tensor engine. Use the first 10,000 original
training records for updates and the next 2,000 for validation. Never open the
official test files for selection. Measure train and validation loss/accuracy
at identical weight states. Repeat baseline and validation-loss winner with
a second initialization seed; do not imply all models were repeated.

Audit: L01-L08 and L12-L16 unchanged from the separate-reader audit. L09/L10
remain PASS pending the affected compilation run; L11 remains PARTIAL because
recorded timing is unverified. The progress mean is an online training loss,
not a fixed-model validation score. Keep this distinction explicit.

Critique: more architecture code would crowd this episode. A small progress
display addresses the current recording need; the experiment report can guide
a later model-choice decision. Previous score 93.5/100 remains provisional
until the affected verification run completes. Decision: hold for verification.

Progress verification completed: all 11 edits replay, numerical/parser checks
pass, and the model still returns 1764/2000 on the unchanged test subset. The
epoch header prints immediately; progress updates at 2048, 4096, 6144, 8192 and
10000 images, followed by the epoch summary. No live recording source changed.
L09/L10 PASS verified. Score: 93.5/100. Decision: rework the still-unmeasured
first-payoff/runtime pacing in rehearsal; no technical blocker remains.

Model comparison completed in experiments/: seven configurations plus baseline
and selected-model second-seed repeats, nine training runs total. The leading
128/64 ReLU recipe reached 95.30% and 94.95% validation accuracy; original
32-unit Tanh reached 94.15% and 93.25% after the same fifteen epochs. See
experiments/findings.md for gaps, loss trends, selection protocol and limits.
These findings do not silently replace the recording's five-epoch baseline
or its separately measured test result. Progress output is the only lesson edit.

## September 15: three-setup comparison

Plan: add a short, three-column measured-results display after the completed
test evaluation and before recap. Select the shuffled 32-unit Tanh baseline
(94.00%), 128-unit ReLU (94.45%) and 128/64-unit ReLU (95.30%). Unlike using
the unshuffled 94.15% baseline, this keeps shuffling policy common to all three.
All use the same train/validation split, seed 42, 15 epochs, batch 64 and LR 0.1.

Keep the 11 code edits and five-epoch live example unchanged. The user asked
for a side-by-side display, not a model/configuration refactor. Identify this
as measured experiment output rather than pretending the live run trained all
three. Keep the implementation and full results available in experiments/.

Audit: L07-L10/L15-L16 require exact measured values, common controls, labeled
validation results and a connected transition from the completed classifier.
The display includes architecture, activation, parameter count, train/validation
accuracy and validation loss. Narration names both changes from small to wide
(width and activation), then the extra hidden layer. It does not attribute
the first gain to width alone or call a growing gap proof of overtraining.
Other checklist judgments remain unchanged. No new code behavior needs a
compiler run; replay and metric checks must pass before handoff.

Critique: the extra comparison adds approximately a minute and may be read
as a universal ranking unless the shared conditions remain visible. Keep the
table on screen; do not narrate every cell. The 128-unit ReLU middle model
was only measured with seed 42, so do not imply a replicated three-way ranking.
Score: 93.5/100, provisional whole-script score retained from prior audit.
Decision: rework first-payoff/runtime timing in rehearsal; no new scope expansion.

Verification completed: all 11 literal edits replay; the resulting C++ is
byte-identical to the previously compiled/verified final.cpp. All displayed
accuracy/loss values match the selected JSON records and validation accuracy
increases left to right. The added narration is approximately 140 words,
roughly one minute before additional visual holds. No benchmark rerun or
recording-code change was needed for this presentation-only addition.

## September 15: explicit repo-local MNIST setup

Plan: preserve the reader's brief introduction and the existing lesson. Replace
cache-dependent paths with data/ paths and supply one public download command.
Licensing sources conflict; data/README.md records the sources and the decision
to ship a downloader, not dataset binaries. This is uncertainty about the
applicable grant, not a claim that redistribution is prohibited.

Implemented: real original IDX files in the code repo's data/ directory,
SHA-256 verification, Git ignores for downloaded data, clear missing-file
errors, public README instructions and matching script snippets. No aliases.
The preparation helper now uses the same downloader instead of a separate
cache workflow. Existing recording code was preserved except its data paths.

Verification: all four downloaded files match expected hashes. Running setup
again verifies and reuses them. All 11 script edits replay against the frozen
baseline; image, loss, training, evaluation and sanitizer/parser checks pass.
The lesson still reaches 1764/2000 (88.2%). The verifier leaves current live
main.cpp unchanged. Current recording code also compiles and runs from the
repo root. At final inspection it does not contain the MNIST section; the
full lesson verification exercises that path in generated temporary programs.
No commit or push performed.

Critique: viewers need internet once and must run from the repository root.
The setup command and reader errors state both requirements. No extra parser
lecture or unrelated model changes were added. Prior provisional script score
93.5/100 remains unchanged; this resolves setup, not unmeasured spoken pacing.

## September 15: remove setup from the recording script

Fragment plan: open on main.cpp and name the recognition task, acknowledge
the supplied helpers in about ten seconds while adding the include, then
read the first image. Keep every literal C++ edit unchanged. Retain setup
instructions in README.md only. This follows the creator's explicit direction
and the long-form opening-retention rationale already linked above; no new
performance claim or Shorts transfer is involved.

Audit of this opening only:

| Check | Status | Points | Evidence or remaining check |
| --- | --- | --- | --- |
| L01 | PASS | 10 | MNIST recognition and testing on unseen images remain explicit. |
| L02 | PASS | 10 | Starts in main.cpp; no setup commands or header tour. |
| L03 | PARTIAL | 4 | Helper acknowledgment is 25 words, about ten seconds; rehearse time to reading the image after the promise. |
| L04 | UNVERIFIED | 0 | First runnable payoff needs a timed recording. |
| L05 | UNVERIFIED | 0 | Whole-episode capabilities not reassessed in this fragment pass. |
| L06 | PASS | 8 | Supplied reader is named immediately before use. |
| L07 | PASS | 8 | 28 by 28 explains 784 at the network call; row/column narration remains. |
| L08 | PASS | 10 | No literal C++ edits changed; preceding full verification still applies to the code. |
| L09 | UNVERIFIED | 0 | Whole-episode proof selection not reassessed. |
| L10 | PASS | 5 | MLP, include and image-loading code match their narration. |
| L11 | PARTIAL | 2.5 | Shorter connected opening; spoken timing remains unmeasured. |
| L12 | UNVERIFIED | 0 | Ending outside fragment scope. |
| L13 | UNVERIFIED | 0 | Ending outside fragment scope. |
| L14 | PASS | 2 | Narration uses >; no production setup checklist in script. |
| L15 | PASS | 2 | Existing researched opening terms retained; keyword map updated. |
| L16 | PASS | 2 | Editorial direction distinguished from measured retention effects. |

Critique: the helper mention still delays the first meaningful code by about
ten seconds. Add the include while speaking and move directly into the reader
call; do not expand it into another explanation. No full compile rerun was
needed for narration-only edits. Rehearse the opening before judging its pace.
Provisional fragment score: 63.5/100. Decision: rework timing in rehearsal;
this limited audit does not replace the earlier whole-script review.

## September 15: compose cross-entropy from log-softmax

Revision plan: preserve the approved opening of section B. Start the external
loss function and its target row before introducing softmax. Explain positive
relative scores, normalization and then logarithms at the actual call site.
Implement reusable row-wise log_softmax with its backward rule, without a
cross_entropy operation or loss-specific TensorNode storage. Use existing
multiply, sum and divide to compose the loss; keep the integer-label interface
for the training loop. No deliberate missing-implementation run.

L01-L05: keep the MNIST promise and first-image payoff; make section B deliver
a complete differentiable loss before training. L06-L08: explain each need
before its exact edit, including one-hot selection and cross-column gradient
dependencies; preserve the recorded prefix and verify the literal progression.
L09-L11: test stability, arbitrary incoming log-softmax gradients and end-to-end
loss derivatives, while keeping numerical test machinery out of narration.
L12-L14: preserve training, evaluation and ending, updating only affected calls.
L15: retain researched MNIST/logits/softmax/cross-entropy terminology at its
teaching point; amend the keyword map. L16: retain the historical comparison
as historical evidence and report any changed training result, not assumed parity.

## September 15: final directive supersedes decomposition proposals

The creator chose clarity and shorter implementation over building all the
primitives in this lesson. The log-softmax proposal was not implemented. The
intermediate exp/log/sum_columns draft passed its verification, including
88.2% test accuracy, but was explicitly superseded and removed from script.md.
Do not restore either abandoned plan from this historical log.

Final plan: preserve both approved paragraphs in B; open cross_entropy() before
teaching the row calculation. Explain the probability problem, positive values
and normalization as needed; use a tiny 2/3/5 reference, then introduce the
negative log at the loss line. Add Operation/cache/parent links only once we
have an actual loss and derivatives to retain. Keep the method under construction
until its forward and backward paths are complete. No deliberate failing run.

L01-L05: same MNIST promise and early image payoff, one completed loss then
training. L06-L08: smaller literal edits, connected narration, complete exact
Before/After progression, explicit reason for the native operation. L09-L11:
rerun stable-loss finite differences, accumulation, scaled gradients, parser
checks and real training; keep test machinery out of recording. L12-L14:
preserve training/evaluation/ending and > narration. L15-L16: update the spoken
keyword map and distinguish the editorial choice from a performance claim.

Final-version audit:

| Check | Status | Points | Evidence / remaining repair |
| --- | --- | --- | --- |
| L01 | PASS | 10 | MNIST classifier promise matches the trained/evaluated program. |
| L02 | PASS | 10 | Main.cpp opening and brief helper acknowledgment retained. |
| L03 | PARTIAL | 4 | Useful image path follows the promise; rehearse time to meaningful coding. |
| L04 | PARTIAL | 4 | Initial scores provide a real payoff, but its one-minute timing is unmeasured. |
| L05 | PASS | 8 | Image scores, complete loss, training and held-out accuracy remain distinct capabilities. |
| L06 | PASS | 8 | Function first; probability calculation next; graph fields only when attaching the loss. |
| L07 | PASS | 8 | Normalization, stable loss expression, derivative signs and incoming-gradient multiplication explained at their code. |
| L08 | PASS | 10 | All 13 exact edits replay and runnable checkpoints pass. No live main.cpp changes. |
| L09 | PASS | 6 | Numerical loss/model checks, accumulation/scaling, extreme-score stability and parser tests pass. |
| L10 | PASS | 5 | Score row and 2/3/5 normalization reference tied to the row loop; not a separate slideshow. |
| L11 | PARTIAL | 2.5 | 1,310 spoken words, 527 in B. Allow roughly 9-10 minutes speech plus 3-5 minutes coding/holds; rehearse against 10-15-minute target. |
| L12 | PASS | 4 | Actual held-out result followed by saving/loading weights as next capability. |
| L13 | PASS | 4 | Itemized recap, next-step display, standard sign-off and clean tail preserved. |
| L14 | PASS | 2 | Recording-only script with > narration and exact edits; review remains separate. |
| L15 | PASS | 2 | Existing researched keywords introduced at relevant calculation; final scope recorded in keyword map. |
| L16 | PASS | 2 | Editorial timing estimates and numerical evidence distinguished from retention claims. |

Verification: baseline, image-scores, loss-complete, trained-mnist,
evaluated-mnist and loss-and-batch-checks PASS. Five-epoch training again reaches
1764/2000 (88.2%); all printed epoch losses remain unchanged. Recording source
hash is unchanged. No GitHub push or publication. The earlier model-comparison
records remain historical runs, not new experiments performed this turn.

Critique: B is still the densest section. Its 527 spoken words take roughly
four minutes before extra coding holds. Keep the probability reference beside
the active loop and do not add a separate softmax lecture or derivation of
the complete Jacobian. The unfinished method has no temporary return and is
never run until both paths are complete. Actual narration pace, screen fit
and total edit duration still require rehearsal.
Score: 89.5/100. Decision: rework timing in rehearsal; no technical blocker.

## September 15: rebuild the explanation and remove derivative caching

Plan before drafting: preserve the approved prefix through the cross-entropy
introduction. Lead from the observed scores to the method boundary, then one
row's normalization, then its loss. Do not mention backward or allocate
derivative storage inside forward. Once the loss exists, explain why graph
history must retain the scores and correct labels. Store labels by value on
the loss node; recompute probabilities and local derivatives in backward.
This metadata is necessary because backward has no label argument, unlike an
optional probability/derivative cache. Explain that distinction before the edit.

L01-L05: unchanged opening promise and initial score payoff; complete a loss
and backward before training. L06-L08: each edit has a concrete spoken purpose,
exact Before/After and a location; split normalization, loss, graph attachment
and backward propagation instead of dropping the whole implementation at once.
L09-L11: test loss derivatives, repeated/scaled backward, label lifetime and
different losses on the same scores, plus real training. Audit narration alone
and estimate runtime; do not claim measured pacing. L12-L14: retain the ending,
training and evaluation, and preserve the live recording code. L15-L16: use
the existing keyword research and long-form retention evidence; this is an
editorial repair, not proof of a retention improvement. Supersede old cache
instructions in current docs while retaining this log's history.

Audit of the delivered version:

| Check | Status | Points | Evidence / remaining work |
| --- | --- | --- | --- |
| L01 | PASS | 10 | Same MNIST classifier promise and verified held-out result. |
| L02 | PASS | 10 | Approved main.cpp opening unchanged. |
| L03 | PARTIAL | 4 | Early image code preserved; measure actual time to useful action. |
| L04 | PARTIAL | 4 | Verified initial scores remain the first payoff; one-minute timing needs rehearsal. |
| L05 | PASS | 8 | B1 computes loss, B2 retains inputs, B3 propagates gradients; C trains. |
| L06 | PASS | 8 | No derivative discussion in forward; labels are saved only after explaining backward's need. |
| L07 | PASS | 8 | Row boundaries, normalization, log loss, target selection and gradient multiplication explained at their edits. |
| L08 | PASS | 10 | All 15 literal edits replay; forward/backward complete before a run; live code unchanged. |
| L09 | PASS | 6 | Numerical, accumulation, scaling, label-ownership, shared-score losses and parser checks pass. |
| L10 | PASS | 5 | One three-column example follows positive values to probabilities and the correct class's loss. |
| L11 | PARTIAL | 2.5 | Narration-only continuity pass completed; 1,401 words plus coding holds needs timing rehearsal. |
| L12 | PASS | 4 | Training and evaluation preserved; next capability remains saving/loading weights. |
| L13 | PASS | 4 | Recap, next-step display, sign-off and clean tail preserved. |
| L14 | PASS | 2 | Exact code pairs, > narration and separate recording cues; review outside script. |
| L15 | PASS | 2 | Existing keyword map retained, cache-removal clarification added. |
| L16 | PASS | 2 | Verified behavior separated from prose-level judgment and timing estimates. |

Verification completed on this exact script: all six program/check stages
pass, including 33 finite-difference checks, extreme-score loss stability,
repeated and scaled backward. Added tests mutate/destroy caller labels before
backward and combine losses with different labels on shared scores. Forward
leaves parent gradients untouched. Real training still reaches 1764/2000
(88.2%); epoch losses match the recorded reference. No derivative cache remains
in the generated code. Live recording main.cpp is unchanged.

Critique and repair performed: the first normalization illustration used
values greater than one, which could distract after subtracting the maximum.
Changed it to 0.5/0.5/1.0, then 0.25/0.25/0.5, and used the third column's
probability for the subsequent loss example. Read the narration without code
or headings to check that each move follows the preceding result.

Remaining risk: the new B1-B3 narration is 524 words, plus the approved prefix.
The complete 1,401-word script is roughly 9-10 minutes of speech at 140-160 wpm;
allowing 4-6 minutes for non-overlapping code/holds gives roughly 13-16 minutes.
The upper bound exceeds the 15-minute target. Rehearse B before recording; if
the edit runs long, the closing model-comparison discussion is the first scope
candidate to move out, rather than cutting explanations needed to follow B.
No claim of perfect voice, measured retention improvement or guaranteed runtime.
Score: 89.5/100. Decision: rework timing in rehearsal; technical checks pass.

### Expand loss selection and averaging into readable steps

Fragment plan/audit: preserve the creator's revised target construction and
removed validation lines. Replace the compressed log/multiply/negative-divisor
expression with named log probabilities, minus-one scalar, per-class losses,
selected losses, batch total, image count and mean loss. Three sequential edits
separate calculating candidate losses, selecting the correct class and averaging.
A three-class 0.2/0.5/0.3 example shows why elementwise multiplication by 0/1
selects the answer. Narration explicitly explains why whole-Tensor sum is now
appropriate: the desired result is one total batch loss, not per-image softmax
denominators. L06-L09 pass for this change; other checks retain their previous
provisional assessment. Extra explanation adds runtime, so the existing
rehearsal/scope risk remains; score is not raised merely for adding detail.

Verification: all 22 edits replay, all eight verification stages pass, and
training remains 1764/2000 (88.2%). The target prefix and live recording source
are preserved. No special TensorNode fields were introduced. Whole-script
score remains provisional at 89.5/100; decision: rework timing in rehearsal.

### Column-sum transition clarification

Fragment plan/audit: preserve the accepted exp-result passage. Acknowledge
that sum() works for the displayed single image, then explain how a batch
introduces multiple image rows and a global denominator mixes their scores.
Only after establishing the need for independent row totals introduce
sum_columns(). L06/L07 pass for this fragment; code and other checklist results
are unchanged. No new compile run needed. Critique: the extra explanation is
necessary because claiming sum() already fails for the one-row preview would
be false. Whole-script score remains provisional at 89.5/100 pending rehearsal.

## September 15: current directive, primitive composition only

Supersedes every native-loss, label-metadata and log-softmax proposal above.
Preserve the quoted prefix exactly. Rewrite the remainder with reusable exp,
sum_columns and log operations. TensorNode must remain byte-identical to the
baseline definition: no class labels, local derivatives or probability caches.
Softmax and cross_entropy_loss are free functions composed from operations;
the loss builds an ordinary one-hot target Tensor locally.

Plan: L01-L05 preserve the classifier promise, show exponentials and then
probabilities before loss; L06-L08 introduce one operation at its call site's
need, including backward before running, with exact sequential edits. No
maximum subtraction in the first pass. L09-L11 verify each primitive with
arbitrary upstream gradients and non-square shapes, then the complete model;
rewrite the remaining narration and flag runtime/numerical limitations.
L12-L14 retain trained/evaluated outcome and concise ending, without touching
live recording code. L15-L16 retain the researched keywords at their actual
introduction, distinguish historical comparison data from this new run, and
audit the final script rather than claiming perfection.

Current-version audit:

| Check | Status | Points | Evidence / remaining work |
| --- | --- | --- | --- |
| L01 | PASS | 10 | MNIST training/evaluation promise retained and delivered. |
| L02 | PASS | 10 | Approved main.cpp opening unchanged byte-for-byte. |
| L03 | PARTIAL | 4 | Existing first useful image action preserved; timing still unmeasured. |
| L04 | PARTIAL | 4 | Initial scores are verified; rehearse the one-minute target. |
| L05 | PASS | 8 | Separate exp and softmax runs show progress before log/loss/training. |
| L06 | PASS | 8 | Each primitive is introduced for the next calculation; no maximum-subtraction detour. |
| L07 | PASS | 8 | Column sums preserve image rows; one-hot selection and per-image averaging explained. |
| L08 | PASS | 10 | 19 exact edits replay; TensorNode identity enforced by verifier; live code unchanged. |
| L09 | PASS | 6 | 57 finite differences, target lifetime, shared inputs, scaling and parser checks pass. |
| L10 | PASS | 5 | Original scores remain beside exp/probability columns; total is printed. |
| L11 | PARTIAL | 2.5 | Entire remaining narration rewritten; 1,493 spoken words still need timing rehearsal. |
| L12 | PASS | 4 | Classifier completes and saving/loading weights follows naturally. |
| L13 | PASS | 4 | Recap updated for primitives; next steps, sign-off and end-screen tail preserved. |
| L14 | PASS | 2 | Script contains code, narration and cues only; audit kept here. |
| L15 | PASS | 2 | Keyword map reflects actual exp/softmax/log/loss introduction, not abandoned APIs. |
| L16 | PASS | 2 | Straightforward numerical limitations and historical comparison provenance disclosed. |

Verification: all eight stages pass, including exp-complete and softmax-complete.
The preview's probability total is 1.000; training remains 1764/2000 (88.2%).
Non-square 2x3 reduction returns [2,1] with totals 6 and 15. Arbitrary upstream
gradients test exp, log, column sum and composed softmax separately. TensorNode
is byte-identical to the baseline. Temporary label mutation/lifetime tests now
validate ordinary target Tensor ownership, not loss-specific node fields.
The final narration-only polish was replayed separately and produces C++
byte-identical to the compiled final.cpp referenced by verification-run.json.
The approved prefix remains byte-identical. No changes to recording main.cpp.

Critique: the first draft repeated the probability plan before coding. The
final opening was shortened and the primitive run now establishes positive
values before discussing a separate total for each image. Cross-entropy's
average explicitly divides by images, not all digit columns. Remaining risk:
1,493 words is about 9-11 minutes of speech, plus non-overlapping code/holds.
Estimate 12-16 minutes depending on delivery; rehearse against the 10-15-minute
target and trim the model-comparison discussion first if scope must shrink.
No claim that extreme-logit numerical stability matches the removed fused loss:
that stress case is now an explicit rejected input path at log, not a passed
2000-loss test. Stable formulations can follow after this first-pass lesson.
Score: 89.5/100. Decision: rework timing in rehearsal; technical checks pass.
