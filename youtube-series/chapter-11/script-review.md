# Chapter 11 preparation and review

Recording script: [script.md](script.md). Research: [keyword-research.md](keyword-research.md).

## Scope and checklist plan

Continue in the actual recorded Chapter 10 main.cpp. Leave its existing examples
and Tensor engine intact except for one mutable data accessor used by the
general parameter update. Build concrete composable modules, not an abstract
registry, ownership framework or new autograd engine. One hidden layer, XOR,
mean squared error and full-batch gradient descent keep the lesson contained.
MNIST is the next dataset milestone, not part of this episode.

| ID | Intended treatment |
| --- | --- |
| L01 | Build reusable Linear/Tanh modules, compose one MLP and learn the four XOR cases. |
| L02 | Anchor on two inputs differing/matching; explain the need for a hidden layer without a series recap. |
| L03 | Start Linear's actual code by 0:30. |
| L04 | Within about one minute, show how one matrix column becomes several learned outputs in the module's forward method. Exact elapsed time needs rehearsal. |
| L05 | Linear forward, nonlinear composition, parameter collection and trained XOR each add a capability. |
| L06 | Introduce construction, random weights, parameter access and updates only at their use; no abstract Module base first. |
| L07 | Explain weight layout, per-output bias broadcasting, initialization symmetry, shared parameter handles and backward reuse. |
| L08 | Replay literal edits against a frozen snapshot of actual Chapter 10 code and compile/run meaningful checkpoints. |
| L09 | Walk through the actual forward dimensions and show final XOR predictions. Keep executable shape/gradient checks in verification. |
| L10 | Start with four cases and show the 4x2 -> 4x4 -> 4x1 shapes beside their calls. |
| L11 | Aim for 10-15 minutes, 1,100-1,350 spoken words, with connected narration and stable code holds. |
| L12 | End with all four XOR cases fitted; distinguish this small training exercise from generalization. |
| L13 | Itemized recap, next-step list, exact sign-off, clean tail. No Q&A. |
| L14 | Only narration, exact edits and scene/output directions in script.md. |
| L15 | Complete research first; use standard module/MLP/gradient terminology beside its code. |
| L16 | Separate tests, editorial judgment, rehearsal estimates and final-media evidence. No analytics refresh or publication. |

## Starting point and verification

- Frozen source: [recorded Episode 10 baseline](verification/episode-10-baseline.cpp), SHA-256 `d265c7d5f3fd59e1c1e695c87fd0f8db82b57c696f65e5cb46d16de6b183687d`.
- This is the actual uncommitted recording source above public HEAD `2c1b9f9`, not the hypothetical endpoint of Chapter 10's old script. It preserves the recorded 100,000-step tanh example and its 0.01 learning rate.
- Replay with `node youtube-series/chapter-11/verify-script.mjs` from the Content HQ root.
- [Verification report](verification-run.json): all 15 literal edits replay; baseline and four completed-code checkpoints pass with ASan/UBSan. The final optimized build reproduces the shown output.
- Supplementary tests cover all 17 parameter gradients with central finite differences, shared parameter-handle identity, update visibility through the model, multi-output shapes, bias broadcasting gradients and rejected invalid layer sizes.
- XOR fits pass for seeds 0 through 9, each with 5,000 steps at learning rate 0.1. Observed MSE is below 0.001 and all four thresholded outputs are correct for each seed. This is a robustness check on this toolchain, not a guarantee for every seed/library/problem.
- Seed 42 produces the script's loss display `0.779 -> 0.000` and predictions rounding to `0, 1, 1, 0`. Three-decimal rounding is not exact zero loss.
- The verifier generates and runs programs in a temporary directory and checks that the live recording source was not modified. The checked-in snapshot is only a verification baseline; the presenter continues in the existing main.cpp, not in a replacement Tensor implementation.

## Architecture and scope decisions

1. Concrete modules expose `forward`; trainable modules also expose `parameters`. No abstract Module base, virtual dispatch, registration system or Sequential container is needed for this fixed composition. These classes remain usable when a wider model arrives.
2. Weight layout remains `[in_features, out_features]`. Bias shape `[out_features]` broadcasts over batch rows. Do not copy PyTorch's transposed storage convention into this Tensor.
3. The constructor uses a shared generator and fan-in-scaled uniform weights. Biases start at zero. Explain identical hidden-unit updates as the reason for distinct weights, without an initialization theory detour.
4. Returning `vector<Tensor>` copies handles, not numerical storage. The list contains exactly four distinct nodes for this architecture. Reusing/tying one layer more than once would require deduplicating parameters before updating; this episode does not implement tied weights.
5. The mutable data accessor exposes the existing flat storage. Only change entries; resizing would violate Tensor shape/gradient invariants. A size-preserving view is a reasonable future API refinement, not required lesson machinery here. Never mutate parameters between a forward pass and its backward pass.
6. Autograd already handles the composed graph. Do not add a backward method to MLP or invent scalar-cell nodes. Clear trainable leaf gradients explicitly; existing backward clears intermediate gradients.
7. The final output is linear and targets are numeric 0/1 values. MSE keeps the loss from the existing implementation. We do not call the outputs calibrated probabilities or claim MSE is the usual classification-loss choice. Thresholding is only result interpretation.
8. All four XOR cases are training data. No held-out generalization claim or elaborate dataset loader. MNIST and its classification/data requirements are the next milestone.

## Checklist audit

| ID | Status | Points | Evidence and remaining risk |
| --- | --- | ---: | --- |
| L01 | PASS | 10/10 | The opening promises reusable layers and a trained XOR network; the final 2-4-1 model delivers both. Matches Chapter 10's module/MLP ending. |
| L02 | PASS | 10/10 | Four visible input-target rows anchor XOR before the neural-network promise. No series introduction or unexplained old-model reference. |
| L03 | PASS | 8/8 | The first code edit builds the Linear forward method and its parameter members, with a planned transition at about 0:20. Timing is an editorial target. |
| L04 | PASS | 8/8 | The early return expression and shape diagram show how columns produce multiple outputs within the first-minute plan. This is a worked forward-pass payoff, not a claim that training runs by one minute. |
| L05 | PASS | 8/8 | Linear owns parameters; MLP composes operations; parameter collection supports one update routine; final training fits all cases. |
| L06 | PASS | 8/8 | Constructor immediately uses random helper; parameter access immediately supports the update. No abstract module framework or staged missing-backward failure. |
| L07 | PASS | 8/8 | Weight/bias shapes, initialization symmetry, shared handles, flat updates and graph reuse are explained beside their code. |
| L08 | PASS | 10/10 | Fifteen literal edits replay against the recorded baseline and pass compiler, sanitizer, numerical-gradient and training checks. |
| L09 | PASS | 6/6 | Final table displays all four XOR cases and loss change; mechanical shape/gradient checks remain outside the recording. |
| L10 | PASS | 5/5 | Directions keep the active return expression, layer sizes, parameter list and original XOR cases visible. Actual opening artwork/render remains a production check. |
| L11 | PARTIAL | 2.5/5 | About 1,200 spoken words plus 3-5 minutes of additional code/visual holds estimates roughly 10.3-13.6 minutes. Actual naturalness and pacing require presenter rehearsal. |
| L12 | PASS | 4/4 | Interpret all four outputs, rounded loss and training-set limitation before the MNIST continuation. |
| L13 | PASS | 4/4 | Itemized recap, three next-episode items, exact sign-off and clean tail. No Q&A. |
| L14 | PASS | 2/2 | Descriptive filename, canonical > narration and literal edits only in script; research and critique separate. |
| L15 | PASS | 2/2 | Dated keyword research precedes the draft; neural network in C++, XOR, MLP, modules, gradients and backpropagation appear naturally in narration. |
| L16 | PASS | 2/2 | Long-form evidence kept separate from Shorts; no new reach claims, media approval or publication inferred from tests. |

## Critique and repairs

The main risk was turning a first-network episode into a framework-design
episode. The draft avoids a base class and registry, and connects two concrete
Linear modules through Tanh. Parameter collection now follows the need to reach
the weights and biases owned by both layers; the update's shape limitation is
introduced afterward, when we use the collected list. Every new helper is fully built on
camera, including initialization and the training example.

The first pass gave random initialization a reason without explaining it.
The final narration now says why identical hidden units receive identical
updates. It also explains the shared Tensor handles before the update relies
on them. Both repairs address likely confusion without adding a theory segment.

Literal replay caught two whitespace mismatches between consecutive Before/After
blocks. Those are repaired. The constructor insertion now shows its complete
neighboring forward method rather than ending at a partial method name.

Compared with the Chapter 10 ending, the final predictions here earn their
screen time: there is no single learned weight/bias pair that reveals XOR.
The viewer needs all four outputs to see whether the network learned it.
No intermediate disposable prediction table or deliberately failed run is added.

The main remaining editorial risk is the initialization segment expanding while
recording. Keep the size guard and random-engine syntax brief; preserve the
weight layout and symmetry explanation. If the edited recording trends over
15 minutes, cut repeated syntax narration rather than rushing the composition
or the parameter-sharing explanation.

The code is verified on Apple Clang/libc++; std::uniform_real_distribution need
not yield identical samples on every standard library. Re-run the local verifier
if the toolchain or starting source changes. The frozen baseline keeps the
test reproducible without reverting the user's ongoing code.

## Final score

97.5 / 100. Decision: advance to presenter rehearsal. The remaining 2.5 points
concern actual delivery and timing, which written review cannot establish.
This is sequential self-review, not independent audience validation. No
thumbnail, final media or release is approved by this script score.

## Focused revision: MLP forward to parameter updates

Scope: preserve everything through the supplied constructor/member narration.
Rewrite the following forward explanation, Section C and the bridge into D.
No implementation or expected-output changes; no new subject requiring new
keyword research. The existing keyword record still applies.

Plan: finish following one input through the network; explain that training
must change both layers' weights/biases; locate those values inside Linear;
introduce one layer's list before combining two lists; only then explain why
the old one-column update needs a general flat-array loop. Keep the need for
write access immediately beside the accessor edit.

The earlier draft mixed private-member access, multi-layer parameter collection
and shape-general updates in one transition. Each individual fact was correct,
but the viewer had to supply the reasoning between them. The revised narration
separates those decisions and names weights/biases as parameters before naming
the method. While typing MLP::parameters, explain the two lists and their join.

| IDs | Fragment assessment | Points |
| --- | --- | ---: |
| L01-L04 | UNVERIFIED here: opening and first payoff are outside this revision. | 0/36 |
| L05-L08 | PASS: ownership need, one-layer list, combined list and general update form a connected progression. Every cpp block matches the pre-revision script; existing mechanical verification applies to unchanged code. | 34/34 |
| L09 | UNVERIFIED here: final proof/output is outside this revision. | 0/6 |
| L10 | PASS: point to MLP members, Linear's private parameters and the old update before changing the relevant API. | 5/5 |
| L11 | PARTIAL: causal gaps repaired; natural delivery and actual timing still need presenter review. | 2.5/5 |
| L12-L13 | UNVERIFIED here: payoff and ending are outside this revision. | 0/8 |
| L14-L16 | PASS within scope: prefix and code preserved, researched terminology remains natural, and text review is distinguished from spoken rehearsal. | 6/6 |

Critique: the revision spends more words on the reason for parameters() rather
than adding more concepts. Keep the return-vector and insert explanations tied
to the code; do not repeat them again at the training call. The general update
still needs an accessor change, but its purpose is now established before we
leave gradient_step to make it. No new full compiler run was necessary for
this prose/direction-only revision; verification-run.json retains the prior
script hash and its successful code results.

Provisional fragment score: 47.5/100. Decision: advance within this fragment
to presenter review. The unassessed opening, proof and ending contribute zero
here; this is not a replacement whole-episode score or measured voice quality.

### Shape-walkthrough follow-up

The shape table previously appeared without a spoken reason for switching to
dimensions. The revised bridge returns to the four XOR pairs, establishes one
case per row and two inputs per case, and states the chosen hidden/output sizes
before showing labels. Each subsequent label follows its actual forward call.
The narration explains that the batch retains four rows while the number of
values per row changes. It ends on predictions, preserving the connection to
the next passage about improving them through training.

Affected checks L07 and L10 pass this text-level review; L11 remains partial
until spoken delivery is tested. Code and scope are unchanged, so the focused
audit and provisional 47.5/100 score above remain unchanged. No new compiler
run or whole-episode readiness claim accompanies this narration-only edit.

### Parameter-list purpose follow-up

Plan: distinguish the working forward/backward graph from the training code's
explicit reset and update responsibilities before introducing parameters().
Name zero_grad and gradient_step as its two consumers, then build the layer
list and model list in the existing order. Preserve code and recorded material.

The previous transition explained where the parameters live, but not why the
existing graph could not complete the training lifecycle by itself. The revised
passage states that backward already reaches the parameters through the graph;
the list selects the Tensors the caller will reset and update. This matches the
later train_xor reset loop and gradient_step call. parameters() itself neither
clears gradients nor changes values and is not required by autograd.

Affected checks L05-L07 and L10 pass the focused text review: the new API now
has two explicit consumers and no implied role in graph traversal. L11 remains
partial pending presenter delivery. The existing keyword map and exact code
edits are unchanged. Other fragment statuses and the provisional 47.5/100
score remain unchanged; this is not a new whole-episode or compiler audit.
Critique: keep the two training responsibilities visible while introducing the
list, without previewing the full training-loop implementation a second time.
Decision: advance this passage to presenter review.

## Focused rewrite: parameter updates through the ending

Scope: preserve the approved script through the direction to open the existing
gradient_step. Rewrite all following narration and split the code edits where
the viewer needs a smaller step. Existing keyword research remains applicable;
no subject, numerical result, or implementation capability was added.

Checklist plan: leave the opening untouched (L01-L04); show the old update,
introduce a list argument and outer loop, explain updating the entries of one
Tensor, then introduce writable data access at that use (L05-L07). Replay every
literal edit and test checkpoints (L08-L09). Tie narration to the visible loop,
accessor, inputs and outputs (L10-L11). Preserve the XOR payoff and concise
recap/MNIST ending (L12-L13), recording format (L14), researched terminology
(L15), and the distinction between text review and delivery evidence (L16).

The earlier passage asked the viewer to connect collection, shapes, flat
storage and const access before changing any code. The new sequence writes the
list loop first. Its empty body is an explicitly unfinished live-coding step,
not a staged failing demonstration. The inner update follows once the data
accessor allows writes. XOR data and model construction now have separate edit
pairs; reset, prediction/loss, backward and update have separate typing cues.

| IDs | Audit of this continuation | Points |
| --- | --- | ---: |
| L01-L04 | UNVERIFIED in this scope: approved opening remains unchanged. | 0/36 |
| L05-L07 | PASS: visible old function motivates the list; individual-entry updates motivate writable data access; setup leads into training and inspection. | 24/24 |
| L08-L09 | PASS: all 17 edit pairs replay; baseline and four checkpoints pass sanitizers; optimized output and module/gradient/training checks pass. | 16/16 |
| L10 | PASS at script level: each new explanation identifies the actual argument, loop, accessor or output being discussed. | 5/5 |
| L11 | PARTIAL: smaller teaching steps improve orientation; 1,652 spoken words across the whole script plus coding holds still require timed rehearsal against the 10-15-minute target. | 2.5/5 |
| L12-L13 | PASS: all four XOR results, rounded-loss interpretation, training/test distinction, recap, next steps and standard sign-off remain. | 8/8 |
| L14-L16 | PASS within scope: exact prefix preserved, review outside script, existing keyword map retained, no performance prediction or release approval. | 6/6 |

Verification: node verify-script.mjs completed successfully. Replaying the old
and revised edit sequences produces byte-identical final C++. The real recording
source remains unchanged. verification-run.json records the new script hash.

Critique: the extra guidance adds spoken time. The next check is a timed spoken
pass through the loop/accessor detour, not more explanation of parameters().
Shorten repetition if needed without removing why we move between functions.
No final-media pacing or audience comprehension has been measured here.

Provisional continuation score: 61.5/100. Decision: advance the revised
continuation to presenter review. Opening checks contribute zero because they
are outside this revision; this is not a replacement whole-episode score.

### Concrete outer-loop walkthrough

The next text pass replaces the abstract list/reference explanation with the
first actual item: the hidden layer's weight matrix. It explicitly distinguishes
updating every weight inside that Tensor from moving to the next Tensor.
Pointing to the existing two assignments then motivates the shared inner loop;
flat storage leads to opening data(), where the const return explains the
overload. This is the focused plan and repair for L06, L07 and L10. Those checks
pass text review; L11 remains partial until delivery is tested. Other audit
statuses and the 61.5/100 provisional continuation score remain unchanged.

Critique: do not repeat the full parameter order when typing the inner loop.
The new passage supplies it once to establish what the outer loop visits.
Only three narration paragraphs changed; implementation and edit order remain
unchanged. No compiler rerun or new whole-episode readiness claim is made.
Decision: advance this passage to presenter review.
