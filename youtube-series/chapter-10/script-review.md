# Episode 10: script preparation and review

Recording document: [script.md](script.md).

Working title: `Building ReLU, Sigmoid and Tanh in C++ | Deep Learning, All the Way Down #10`

## Keyword and SEO analysis completed before drafting

[Keyword research](keyword-research.md), prepared September 14, 2026. Primary
phrase: `ReLU, sigmoid and tanh in C++`. Supporting terms appear only when the
code gives them meaning: activation functions, nonlinear activation, neural
networks, autograd, backpropagation, local derivative, gradient, elementwise
operation, and nonlinear regression.

## Starting point and scope

Start from the current Episode 9 `main.cpp` in
`aliases/02-screen-long-form`. Baseline SHA-256:
`9884bdafa86a39e330fa8581879001fcd226a25396f4112e919f8576d995a125`.

Episode 10 adds three elementwise Tensor operations and their backward rules:
ReLU, sigmoid, and tanh. It then changes the existing regression model from

```cpp
inputs.matmul(weights) + bias
```

to

```cpp
(inputs.matmul(weights) + bias).tanh()
```

The final example learns values sampled from `y = tanh(2x + 1)`. It is one
nonlinear unit, not a multilayer perceptron. Module composition, a first MLP,
and MNIST remain later steps.

## Checklist plan

| ID | Plan |
| --- | --- |
| L01 | Add three nonlinear activation functions, give autograd their backward rules, and use tanh to learn an S-shaped target. |
| L02 | Name a neural network before describing its limitation. Show two labeled linear layers collapsing into one, connect depth to the need for nonlinear activations, then introduce ReLU. |
| L03 | At 0:15, finish the linear-layer equivalence and begin ReLU; at 0:20, move to its code; by 0:30, start the public method. |
| L04 | Show `[-2, -1, 0, 1, 2]` becoming `[0, 0, 0, 1, 2]` in the opening visual and verify it in the first run. |
| L05 | Produce four capabilities: shared unary forward operations, unary backward propagation, three working activation functions, and nonlinear training. |
| L06 | Show the ReLU call before its helper. Preview each substantive edit in spoken narration, explain decisions while typing, and finish forward and backward before running each activation. |
| L07 | Preserve why shape stays fixed, why the graph records one parent, why backward multiplies gradients, and why sigmoid/tanh reuse their outputs. |
| L08 | Apply literal Before/After edits to the exact Episode 9 source and verify the resulting program plus numerical gradient checks. |
| L09 | Use the activation table and trained curve as on-screen proof; keep broader gradient checks outside the recording. |
| L10 | Keep the current formula, lambda, output column, or learned curve visible while explaining it. |
| L11 | Target 12-15 minutes. Read the spoken track across section boundaries, check every preview against its code, and budget time for typing instead of speeding through explanations. |
| L12 | Finish with a nonlinear model that recovers weight 2 and bias 1 and matches three sampled targets. |
| L13 | End with an itemized recap, concise module-system preview, standard sign-off, and five clean seconds. |
| L14 | Keep only recording material in script.md, including its MP4 filename and exact edits. Store the complete preparation and review here. |
| L15 | Use the researched activation and autograd terms naturally beside their implementation. |
| L16 | Treat runtime and rendered visual quality as unverified until rehearsal and final-media review. |

## Production and verification notes

- [Verification report](verification-run.json): all 20 literal edits replayed
  against the starting source. The baseline, four completed-feature checkpoints
  and activation-gradient checks passed under ASan/UBSan. Reproduce with
  `node youtube-series/chapter-10/verify-script.mjs` from the Content HQ root.
- The script starts from the current Episode 9 `main.cpp` SHA-256 shown above.
  Preserve unrelated `.gitignore` and `.vscode/settings.json` changes.
- The opening equation includes biases, so it demonstrates equivalence between
  affine layers using the standard deep-learning name `linear layer`.
- The opening visual is explanatory, not a title card. Begin narration on frame
  zero, move to code around 0:20 and start the ReLU method by about 0:30.
- `elementwise_unary()` preserves shape, allocates new data, records one
  operation, and keeps one parent node.
- `backward_unary()` multiplies the incoming gradient by the local derivative
  and uses `+=` so shared paths still accumulate.
- ReLU uses a derivative of zero at exactly zero. State that convention once.
- Sigmoid backward reuses `y(1-y)`. Tanh backward reuses `1-y²`.
- The direct sigmoid formula is sufficient for the demonstrated values. A
  numerically specialized extreme-input implementation is outside this lesson.
- The final model is `tanh(wx+b)`. It learns one S-shaped family, not an
  arbitrary curve and not an MLP.
- Keep softmax out of this episode. It couples values across a vector and belongs
  with classification loss.
- The final training output was measured from the mechanically transformed
  Episode 9 source. Do not promise exact printed values after changing the data,
  learning rate, formatting, or iteration count without rerunning verification.
- Sanitizer-backed checks cover ReLU at negative, zero, and positive inputs;
  sigmoid at zero; tanh at zero; and finite-difference comparisons for sigmoid
  and tanh at four nonzero values.
- Rehearse before recording. If the draft exceeds 15 minutes, shorten the table
  narration and keep only one full explanation of the shared unary helpers. Do
  not remove the chain-rule explanation or the final nonlinear fit.

## Checklist audit

| ID | Status | Points | Evidence and remaining risk |
| --- | --- | ---: | --- |
| L01 | PASS | 10/10 | The opening promises nonlinear Tensor operations and the script implements three forward and backward paths plus a trained tanh curve. |
| L02 | PASS | 10/10 | The opening names a neural network and explains what its linear layers do before stating why nonlinear activations are needed. The labeled layer diagram supplies the referent immediately. No prior model or episode is assumed. |
| L03 | PASS | 8/8 | The opening moves to code around 0:20 and starts the ReLU method by 0:30. Its actual call precedes the helper. These are rehearsal targets, not measured timing. |
| L04 | PASS | 8/8 | The opening works through ReLU on five values, and the first live run reproduces the same result. Final timing still needs rehearsal. |
| L05 | PASS | 8/8 | ReLU forward, unary backward, sigmoid, tanh, the comparison table, and nonlinear training each leave a visible capability. |
| L06 | PASS | 8/8 | The ReLU method calls the helper before we implement it. Each substantive edit has a spoken preview and specific while-typing narration. Both directions of each activation are complete at its first run. |
| L07 | PASS | 8/8 | Shape preservation, graph history, the chain-rule multiplication, gradient accumulation, and output reuse remain beside the responsible lines. |
| L08 | PASS | 10/10 | The exact edit sequence was applied to the current Episode 9 source; the resulting program compiles and all activation-gradient checks pass under ASan/UBSan. |
| L09 | PASS | 6/6 | The activation table proves forward behavior and the final fit proves tanh backward in training. Broader derivatives have separate numerical checks. |
| L10 | PASS | 5/5 | Directions identify the exact equation, formula, derivative, output columns, and final prediction rows to keep visible. Rendered visual quality remains unverified. |
| L11 | PARTIAL | 2.5/5 | The spoken track connects each activation to a concrete need before implementation. The revised draft has roughly 1,550 spoken words plus code holds; presenter rehearsal must establish natural delivery and keep the final cut within 15 minutes. |
| L12 | PASS | 4/4 | The final model recovers weight 2 and bias 1 and matches three points from the nonlinear target. |
| L13 | PASS | 4/4 | The ending contains an itemized recap, three-item next episode, exact sign-off, and five-second tail. |
| L14 | PASS | 2/2 | script.md contains the filename, canonical narration and recording directions. Research, rationale, audit and score are in companion files. |
| L15 | PASS | 2/2 | Dated research remains relevant to the unchanged subject. C++, nonlinear activation, ReLU, sigmoid, tanh, autograd, gradient and nonlinear regression appear in the spoken track beside their use. |
| L16 | PASS | 2/2 | The audit separates verified code from unverified rehearsal, opening render, final pacing, and media quality. |

## Critique

The opening now anchors a new viewer in a neural network and its linear layers
before discussing the limitation. Depth alone failing to add expressive power
provides the hook; building nonlinear activations provides the lesson's promise.
The diagram begins with labeled layers before introducing the equation.

The previous draft relied on unspoken notes to explain why we moved between
functions. This revision puts the editing decisions into the narration: the
ReLU call creates the need for the unary helper; its saved parent leads into
gradient propagation; and the derivative callback leads directly into the
ReLU switch case. Each change gets a brief preview followed by narration tied
to the lines being typed.

The ReLU-to-sigmoid transition now gives a concrete reason to bound the output:
a probability must stay between zero and one. This motivates sigmoid without
adding a classification example or claiming its outputs are automatically
calibrated probabilities. The existing helper then supplies the connection to
the code. The fragment preserves the completed ReLU section and its output;
only the two transition passages changed, so no code replay is required.

The sigmoid-to-tanh transition now connects the observed positive outputs to
their intended meaning. A probability uses nonnegative values; steering can use
negative for left, positive for right, and zero for straight ahead. This introduces tanh
without pretending sigmoid failed. Steering is a brief motivation, not a
new application we promise to build. The table then leads to a new question:
can training fit a curve when tanh acts on a weighted input instead of a fixed
number? The forward edit, training caller, replacement data, and final run each
follow from that question.

The revised narration has roughly 1,550 words, about 9.4-11.1 minutes
at 140-165 words per minute. Allowing another 3-5 minutes for code entry and
screen holds beyond the concurrent narration gives an estimated 12.4-16.1 minutes.
This is a planning estimate. The main risk remains repeated explanations or
typing holds pushing the recording over 15 minutes. The opening through sigmoid
is already recorded, so use its actual edited duration when budgeting the
remaining sections. Keep the remaining table walkthrough brief and avoid
reading unchanged code aloud; preserve the reasons for moving between subjects.

The opening visual is planned but not rendered. Its equation and five-value
ReLU result are technically specified, yet actual legibility and timing remain
production checks.

## Final score

The code replay and gradient checks establish technical consistency. They do
not establish whether the presenter will find the new language natural. The
score follows the weighted checklist; it is not an independent assessment of
voice quality or an audience prediction. Presenter rehearsal remains partial.

Score: 97.5/100. Decision: advance.

## Post-sigmoid transition revision

Scope: preserve the recorded material through `sigmoid-complete`; revise only
subsequent narration and recording cues. The whole-episode audit above retains
earlier evidence, not a fresh approval of recorded delivery.

Plan: motivate tanh with the need for signed outputs; connect its forward method
to its backward case; use the completed table to motivate training; follow the
forward caller into the loop and its data; interpret the fit before introducing
the need for more units. Keep every code edit and output unchanged.

| Check | Fragment audit | Points |
| --- | --- | ---: |
| L01-L04 | UNVERIFIED in this fragment: recorded opening and first payoff are outside this revision. | 0/36 |
| L05 | PASS: tanh implementation, comparison, and trained nonlinear fit each produce a capability. | 8/8 |
| L06 | PASS: the need and next edit are spoken before code. | 8/8 |
| L07 | PASS: derivative meaning and the training path remain explicit. | 8/8 |
| L08 | PASS: compared every fenced block with the pre-edit script; code and expected output are identical. Prior code verification still applies. | 10/10 |
| L09 | PASS: the existing table and measured training output remain the proof. | 6/6 |
| L10 | PASS: cues point to the current lambda, columns, training call, and results. Rendered footage remains unchecked. | 5/5 |
| L11 | PARTIAL: subject changes have a reason, but actual delivery and the upper runtime estimate remain risks. | 2.5/5 |
| L12 | PASS: interpret the learned parameters and sampled predictions before the continuation. | 4/4 |
| L13 | PASS: recap, module preview, sign-off, and tail remain. | 4/4 |
| L14 | PASS: recorded prefix preserved exactly; review stays outside script.md. | 2/2 |
| L15 | PASS: existing research covers the unchanged scope; activation names, backward, gradients, and regression remain spoken naturally. | 2/2 |
| L16 | PASS: unchanged code is distinguished from unverified spoken delivery and timing. | 2/2 |

Critique: a range comparison alone did not explain why the viewer should care
about another activation. The revision supplies that reason and avoids starting
the training section as an unrelated demonstration. The steering
example should remain brief; expanding it would introduce a second lesson.
Actual pacing is still the main unresolved check. No code rerun was needed for
this narration-only revision.

Provisional fragment score: 61.5/100. Decision: advance within the revised
fragment only. The opening's 36 points are unverified here, not editorial
failures; this fragment score does not establish whole-episode readiness.

## Immediate fitted-curve reveal

This revision supersedes the prediction-table references in the earlier audit.
Plan: end `train_curve()` after printing weight and bias, run it, then immediately
substitute the learned values into `y = tanh(weight * x + bias)` on screen.
Keep the earlier recorded explanation and training code intact.

The extra forward call and three-row print loop were diagnostic output, not
part of training. Removing them gives the parameter-to-curve explanation its
payoff without another coding detour. The nine-point fit remains a controlled
demonstration, not evidence of generalization to arbitrary curves.

Affected checks: L06, L07, L09, L10 and L12 pass editorial review through the
direct parameter substitution; L11 remains partial pending recorded timing.
L08 is currently UNVERIFIED for a fresh replay: the recording source has changed
from the Episode 9 baseline, so the verifier correctly stopped at its source
hash guard. No recording code was modified. The training arithmetic is unchanged;
only the final diagnostic call/loop and their output expectations were removed.
All other fragment statuses remain as above. Earlier verification-run.json is
historical evidence, not a successful run of this latest script.

Critique: the reveal clearly identifies the fitted function, but it does not
display pointwise errors anymore. Parameter recovery is sufficient for this
narrow example; broader correctness checks remain a separate workflow.

Provisional fragment score: 51.5/100. Decision: hold on fresh mechanical replay;
the requested editorial revision is complete. Replay against the preserved
Episode 9 baseline before claiming renewed whole-script verification.
