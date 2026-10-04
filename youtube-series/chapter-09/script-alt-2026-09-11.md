Proposed MP4: `cpp-linear-regression-autograd-gradient-descent.mp4`

# Episode 9: Training Linear Regression from Scratch in C++ (alternative draft)

Working YouTube title: `Training Linear Regression from Scratch in C++ | Deep Learning, All the Way Down #9`

Alternative draft for comparison with [script.md](script.md), written September 11,
2026. Same episode scope, same code checkpoint, same measured results. Different
editorial structure.

## How this draft differs from script.md

- Failure-first cold open on real data: the batch loss is computed, then
  `loss.backward()` demonstrably stops on the two missing rules. The parallel
  draft opens with a four-row toy dataset instead.
- One dataset and one training loop. The scalar toy stage is removed; its
  known-answer sanity role stays in the off-camera suite (the retained synthetic
  regression converges across 100 full-batch steps). On camera, every section
  serves the single real-data arc.
- Matmul backward is written as one complete helper with both parent updates,
  derived from a single forward product. No half-implemented intermediate stage
  needs a do-not-test label.
- Nine literal edits instead of twelve, one model build instead of two and six
  checkpoints instead of eight. Spoken length is comparable (about 1,300 words);
  the savings come from typed lines and runs. Projected 11.5-13.5 minutes
  instead of 13-15. Runtime remains an estimate until rehearsed.

## Keyword research completed before drafting

Read [keyword-research.md](keyword-research.md). Research completed September 10,
2026, and revised September 11, 2026. This draft uses the same primary phrase
(linear regression from scratch in C++) and the same spoken-keyword map, since
the episode scope is unchanged. The opening names linear regression, C++ and
autograd. Supporting terms arrive with their code: backpropagation, mean squared
error, matrix multiplication, broadcasting, gradient checking, gradient descent,
learning rate, mean absolute error. No keyword roll call and no spoken series
intro.

Starting code: public Episode 8 checkpoint
`7021cfe0eb1704a31e9f429c9684d5ff66af78bd`, `main.cpp`, through README-only HEAD
`f24101e`. The recording workspace is `aliases/02-screen-long-form`. All live
edits below target `main.cpp`. Keep its existing tests. The prepared helper and
attributed dataset live in `examples/auto-mpg/` in the recording repository. Read
that folder's README before recording; file parsing is not a live-coding section.

Episode 8's recorded captions promise sum and matrix-multiplication backward,
gradient tests, and a linear regression loop that learns from data. This draft
delivers exactly that promise and nothing beyond it.

## Checklist plan

| ID | This episode's plan |
| --- | --- |
| L01 | Promise: make our own autograd train a real linear regression on 392 real cars and evaluate it on held-out cars. Limitation named in the first minute: backward stops at sum and matmul. Scope boundary: two features, a linear model, a fixed systematic split, prepared data plumbing. Matches Episode 8's recorded promise. |
| L02 | First frame is the editor at the insertion point before main(); first sentence states we are training linear regression in C++ on real car data. No greeting, recap, roadmap or series premise. |
| L03 | Paste the include and data plumbing during the first sentences; type the model expression live. Targets: prediction line by 0:15, initial loss measured on screen by 0:30. |
| L04 | First payoff by about 0:55: a real, computed training loss (609.119) immediately followed by backward stopping on our own `backward rule not implemented yet` error. The gap is demonstrated, not described. |
| L05 | Capabilities per section: A measures the training loss and names the exact gap; B differentiates any reduction; C differentiates matrix products and produces real gradients; D verifies a gradient independently; E trains the model; F scores it against a baseline on held-out cars. Six observable checkpoints, no single delayed reveal. |
| L06 | Sum backward arrives only when backward reaches it; matmul backward only when it is the remaining gap; the learning rate arrives with the first update; mean absolute error arrives at evaluation. No theory primer. |
| L07 | Derivations kept beside the code: one forward product gives both local derivatives; += exists because entries feed many outputs; updates follow backward so gradients match the current weights; the final loss is recomputed because the loop's print predates the last update; the bias gradient is checked by hand against the average MPG. |
| L08 | Nine literal Before/After edits replayed mechanically against the checkpoint today; every quoted output measured. The one intentional non-running stage (the pre-rules backward call) is the cold-open demonstration and is labeled as such. |
| L09 | Every on-screen run establishes something new: loss is measurable, backward stops, gradients flow, a finite difference agrees, loss falls, held-out error beats the baseline. The 195-comparison gradient suite, split/scaling checks and the least-squares comparison stay off camera and are cited, not inventoried. |
| L10 | Highlights name exact lines and values: the sum node in the backward switch, the forward product's two factors, the += pair, the step prints, the two MAE lines and the Ford row. |
| L11 | About 1,300 spoken words (measured on this draft) plus one model build and six checkpoints project to roughly 11.5-13.5 minutes. Rehearsal required; if over 15, move the live finite-difference check to the off-camera suite first. |
| L12 | The promised capability is demonstrated end to end and its limits are stated (two features, old cars, fixed split, associations rather than causation). Continuation arises from the linear-model limit: nonlinear activation next. |
| L13 | Itemized recap, three-item next list, exact standard sign-off, five clean end-screen seconds. No Q&A. |
| L14 | Only `>` paragraphs are spoken; edits, checkpoints and timing stay outside narration. |
| L15 | September 10-11 keyword research precedes this draft; the spoken-keyword map is audited against actual `>` lines below. |
| L16 | The failure-first opening applies the Episodes 1-6 retention report (Episode 5's contradiction-style opening was the strongest); it is a transfer hypothesis to measure at 0:15-2:00, not a proven ranking factor. |

## Recording script

Target: 11.5-13.5 minutes. Section windows are estimates, not measured
timestamps. The parallel draft's verification measured 1,248 spoken words at
about eight to ten narration minutes; this draft speaks about 1,300, types one
model build instead of two and holds six checkpoints instead of eight, which is
the basis of the projection. Paste the include and the data plumbing as setup
while speaking; live-type the model, the loss, the backward call and every
update. Before locates each edit; After shows exactly what to build. Do not
read both. Narration accompanies typing; do not count that time twice. Rehearse
the complete sequence.

### A. Compute the loss, then hit the wall | 0:00-1:30

Frame zero: editor at the insertion point immediately before main(). Paste the
include and the function shell with its data loading during the first sentences,
then type the model and loss live. No completed training output is pre-recorded.

> Let's train linear regression from scratch in C++, on real measurements: 392 cars, predicting miles per gallon from horsepower and weight, using the autograd engine we've been building.

While the include and data loading appear:

> Six cars have no horsepower measurement, so they're left out. Every fifth car goes into a held-out set that training never touches, and both features are standardized with training-only statistics, because horsepower and weight measure very different things.

<!-- edit: data-include -->
**Before**
```cpp
#include <unordered_set>
```

**After**
```cpp
#include <unordered_set>
#include "examples/auto-mpg/auto_mpg.hpp"
```

Location: immediately before main(). Insert the function and its call. Keep all
existing tests below the call.

<!-- edit: batch-forward -->
**Before**
```cpp
int main() {
```

**After**
```cpp
void train_linear_regression() {
  const auto data = load_auto_mpg("examples/auto-mpg/data/auto-mpg.data");
  const Tensor inputs({data.train.size(), 2}, data.train_inputs);
  const Tensor targets({data.train.size(), 1}, data.train_targets);
  Tensor weights({2, 1}, {0.0, 0.0});
  Tensor bias({}, {0.0});

  const Tensor predictions = inputs.matmul(weights) + bias;
  Tensor loss = mse_loss(predictions, targets);
  std::cout << "Training cars: " << data.train.size()
            << ", held out: " << data.test.size() << '\n';
  std::cout << "Initial MSE: " << loss.at({}) << '\n';
}

int main() {
  train_linear_regression();
```

While typing the model and loss:

> With both weights at zero, every prediction starts at zero. Matrix multiplication produces one prediction per car, broadcasting adds the single bias to every row, and mean squared error folds all 313 misses into one number we can train from.

<!-- checkpoint: initial-loss -->
Run it. Measured output:

```text
Training cars: 313, held out: 79
Initial MSE: 609.119
```

> Six hundred and nine is the average squared miss we start with, and we can already compute it, because the forward pass works. What we can't do yet is train, because training needs gradients. Let's ask autograd for them.

Location: end of train_linear_regression().

<!-- edit: loss-backward -->
**Before**
```cpp
  std::cout << "Initial MSE: " << loss.at({}) << '\n';
}
```

**After**
```cpp
  std::cout << "Initial MSE: " << loss.at({}) << '\n';
  loss.backward();
  std::cout << "Weight gradients: "
            << weights.grad()[0] << ' ' << weights.grad()[1] << '\n';
  std::cout << "Bias gradient: " << bias.grad()[0] << '\n';
}
```

<!-- checkpoint: backward-missing -->
Run it again. This stage is expected to stop; that stop is the opening's point.
The run prints the two lines above, then terminates on our own uncaught
`std::logic_error` with the message `backward rule not implemented yet`. Verified
behavior of the checkpoint code (exit 134). On a terminal the status lines flush
before the stop; a fully buffered capture may interleave them, so record in the
normal run terminal.

> There's the wall. Backpropagation walks the graph from the loss backward. It gets through the division inside our mean, because division already has a rule. Then it reaches the sum, finds no rule, and stops. Right behind it sits the matrix multiplication that made the predictions, also missing its rule. Those two gaps are the episode: implement both, verify the gradients, then train.

### B. Send the loss gradient through sum | 1:30-3:15

Show mse_loss's mean call and mean's sum call briefly on screen, then go to the
default branch in Tensor::backward().

> Look at the loss on screen. Mean squared error squares each residual, sums the squares, and divides by the count. Backward already handles the division: the incoming gradient gets scaled by one over the count. Then it reaches the sum and stops.
>
> A sum has the simplest derivative there is. Nudge any one element and the total moves by exactly that nudge, so each element's slope is one. Hand the incoming gradient, unchanged, to every element. And notice the plus-equals: every rule in this engine adds into the gradient array, because backward zeroes the arrays up front, and one element can collect contributions from several paths.

<!-- edit: sum-backward -->
**Before**
```cpp
        default:
          throw std::logic_error("backward rule not implemented yet");
```

**After**
```cpp
        case Operation::sum: {
          TensorNode* input = output->parents[0].get();
          for (double& gradient : input->grad) {
            gradient += output->grad[0];
          }
          break;
        }

        default:
          throw std::logic_error("backward rule not implemented yet");
```

> Sum can now relay the gradient into the squared residuals, and the existing arithmetic rules carry it onward to the predictions. Except the predictions come from a matrix multiplication, and that node still stops us.

### C. Send gradients through matrix multiplication | 3:15-7:15

Show the existing forward product, unchanged. Highlight the left factor, then
the right factor.

```cpp
          sum +=
            node_->data[row * left_cols + index] *
            other.node_->data[index * right_cols + col];
```

> Here is the forward pass. Each output element is a sum of products: a left entry times a right entry, accumulated over the inner dimension. Take one of those products apart. If the left entry moves, the product moves by the right entry's value. If the right entry moves, the product moves by the left entry's value. Those are the two local derivatives, and the chain rule multiplies each by the output's incoming gradient.
>
> One left entry feeds every column of its row. One right entry feeds every row of its column. So each input entry collects a contribution from every product it participated in. That is the entire backward rule, and the loops that visit those products already exist in the forward pass.

Location: Tensor private section, directly above build_topology(). Write the
complete helper in one edit; both parents get their update together.

<!-- edit: matmul-helper -->
**Before**
```cpp
  static void build_topology(
    TensorNode* node,
```

**After**
```cpp
  static void backward_matmul(TensorNode* output) {
    TensorNode* left = output->parents[0].get();
    TensorNode* right = output->parents[1].get();

    const std::size_t rows = left->shape[0];
    const std::size_t inner = left->shape[1];
    const std::size_t columns = right->shape[1];

    for (std::size_t row = 0; row < rows; ++row) {
      for (std::size_t column = 0; column < columns; ++column) {
        const double gradient = output->grad[row * columns + column];

        for (std::size_t index = 0; index < inner; ++index) {
          const std::size_t left_index = row * inner + index;
          const std::size_t right_index = index * columns + column;

          left->grad[left_index] += gradient * right->data[right_index];
          right->grad[right_index] += gradient * left->data[left_index];
        }
      }
    }
  }

  static void build_topology(
    TensorNode* node,
```

Explain while typing the loops, not as a second walkthrough:

> Rows and columns locate the output whose gradient we're reading. The inner loop walks the same pairs the forward pass multiplied. Both updates are plus-equals, because each matrix entry serves many outputs, and overwriting would keep only the last contribution.

Location: Tensor::backward(), after the sum case. Add the dispatch.

<!-- edit: matmul-dispatch -->
**Before**
```cpp
        default:
          throw std::logic_error("backward rule not implemented yet");
```

**After**
```cpp
        case Operation::matmul:
          backward_matmul(output);
          break;

        default:
          throw std::logic_error("backward rule not implemented yet");
```

> The dispatch is just a case that calls the helper. And with both rules in place, the same program that stopped at the loss should now differentiate the entire batch. Let's run it.

<!-- checkpoint: gradients-flow -->
Measured output (the training counts and Initial MSE print again first):

```text
Weight gradients: 12.2981 13.1542
Bias gradient: -46.8313
```

> Gradients. The bias slope is the largest in magnitude, which makes sense: the bias participates in every one of the 313 predictions, and right now every prediction is off by that car's full MPG. The weight slopes summarize how each standardized feature moves with MPG across the training set, and checking an aggregate like that by hand would be tedious. So let's make the computer check it.

### D. Verify a gradient without autograd | 7:15-8:45

> Before these gradients drive a thousand updates, let's measure one of them without autograd at all. Take the first weight, move it up by a tiny epsilon and down by the same epsilon, recompute the loss both times, and divide the change by the distance. That's a central finite difference: the derivative from its definition, no graph involved. Comparing it against the engine's answer is called gradient checking.

Location: end of train_linear_regression(), immediately after the bias-gradient
print. This code stays as a one-time check before training; the analytic
backward pass above has already finished.

<!-- edit: numerical-check -->
**Before**
```cpp
  std::cout << "Bias gradient: " << bias.grad()[0] << '\n';
}
```

**After**
```cpp
  std::cout << "Bias gradient: " << bias.grad()[0] << '\n';

  const double epsilon = 1e-5;
  const double original = weights.at({0, 0});

  weights.at({0, 0}) = original + epsilon;
  const double upper = mse_loss(inputs.matmul(weights) + bias, targets).at({});
  weights.at({0, 0}) = original - epsilon;
  const double lower = mse_loss(inputs.matmul(weights) + bias, targets).at({});
  weights.at({0, 0}) = original;

  const double numerical_gradient = (upper - lower) / (2.0 * epsilon);
  std::cout << "Gradient check: " << weights.grad()[0]
            << " vs " << numerical_gradient << '\n';
}
```

While typing the probes:

> Each evaluation builds a fresh graph around the moved weight, and afterward we restore the original zero, so training still starts at zero.

<!-- checkpoint: gradient-check -->
Run it. Measured output:

```text
Gradient check: 12.2981 vs 12.2981
```

The verifier compares them numerically; a matching rounded print alone is not proof.

> Twelve point two nine eight one, twice. The engine and the measurement agree to every digit shown. The full test suite repeats this comparison a hundred and ninety-five times, across both matmul inputs, rectangular shapes, broadcasting and shared storage.

### E. Train the model | 8:45-11:45

> Verified gradients are finally useful for the thing we came for. The update rule is gradient descent: subtract from each parameter its gradient, scaled by a learning rate. Ours is zero point zero five, and we'll take a thousand steps.

Location: end of train_linear_regression(), after the numerical-gradient print.

<!-- edit: training-loop -->
**Before**
```cpp
  std::cout << "Gradient check: " << weights.grad()[0]
            << " vs " << numerical_gradient << '\n';
}
```

**After**
```cpp
  std::cout << "Gradient check: " << weights.grad()[0]
            << " vs " << numerical_gradient << '\n';

  const double learning_rate = 0.05;
  for (std::size_t step = 0; step < 1000; ++step) {
    const Tensor predictions = inputs.matmul(weights) + bias;
    Tensor loss = mse_loss(predictions, targets);
    loss.backward();

    if (step % 250 == 0) {
      std::cout << "Step " << step << ": " << loss.at({}) << '\n';
    }

    for (std::size_t feature = 0; feature < weights.numel(); ++feature) {
      weights.at({feature, 0}) -= learning_rate * weights.grad()[feature];
    }
    bias.at({}) -= learning_rate * bias.grad()[0];
  }

  const Tensor final_predictions = inputs.matmul(weights) + bias;
  const Tensor final_loss = mse_loss(final_predictions, targets);
  std::cout << "Final MSE: " << final_loss.at({}) << '\n';
  std::cout << "Standardized-feature weights: "
            << weights.at({0, 0}) << ' ' << weights.at({1, 0}) << '\n';
  std::cout << "Learned bias: " << bias.at({}) << '\n';
}
```

While typing the forward and backward lines:

> Each step rebuilds the predictions and the loss from the current weights, so every step gets a fresh graph. Backward fills the gradients first, and only then do we move the parameters, because those gradients must describe the weights we actually have. The two weights live in one vector, so the update loops over its entries; the bias is still a scalar.

Point to the final evaluation:

> One subtlety at the end: the loss printed inside the loop belongs to the weights before that step's update. So after the final update, we rebuild the loss once more and report the model we actually finished with.

> This is full-batch gradient descent: every step sees all 313 cars. Let's run it.

<!-- checkpoint: training-complete -->
Measured output:

```text
Step 0: 609.119
Step 250: 16.7918
Step 500: 16.7909
Step 750: 16.7909
Final MSE: 16.7909
Standardized-feature weights: -1.77778 -5.0331
Learned bias: 23.4157
```

These are measured results. Real measurements do not fit a two-feature linear
model to zero loss.

> Six hundred and nine down to sixteen point eight, and flat by step five hundred. Both weights are negative: in this data, more horsepower and more weight go with lower miles per gallon. They multiply standardized features, so read them as associations in this dataset rather than MPG-per-horsepower conversions or causal effects. And the bias lands at twenty-three point four, which the test suite confirms is the average training MPG. That also explains the bias gradient we measured at the start: at zero weights every residual is minus the true MPG, so the bias slope works out to minus twice that average. Minus forty-six point eight.

### F. Score the cars it never saw | 11:45-13:15

> All of that is training loss, and a model can look good on cars it has already seen. The seventy-nine we kept aside answer the honest question. A small report helper runs the model on them in plain doubles and compares against the simplest honest baseline: predict the average training MPG for every car.

Location: end of train_linear_regression(). The report helper never updates
weights; it averages abs(prediction - actual MPG) over the held-out cars and
does the same for the baseline.

<!-- edit: held-out-evaluation -->
**Before**
```cpp
  std::cout << "Learned bias: " << bias.at({}) << '\n';
}
```

**After**
```cpp
  std::cout << "Learned bias: " << bias.at({}) << '\n';
  report_test_mpg(data, weights.data(), bias.at({}));
}
```

> We report mean absolute error here, so the answer is in miles per gallon rather than MPG squared. Training still uses mean squared error. Let's run the comparison.

<!-- checkpoint: held-out-complete -->
Measured output:

```text
Held-out cars: 79
Mean baseline test MAE: 6.48873 MPG
Model test MAE: 3.55954 MPG
chevrolet chevelle malibu: predicted 19.1129, actual 18 MPG
ford galaxie 500: predicted 11.0726, actual 15 MPG
dodge challenger se: predicted 16.9213, actual 15 MPG
plymouth duster: predicted 24.658, actual 22 MPG
peugeot 504: predicted 25.9701, actual 25 MPG
```

The five examples are fixed in file order, not selected for looking good. The
reported average includes all 79 held-out cars. Highlight the two MAE lines,
then the Ford row; do not read every prediction aloud.

> Guessing the average misses by six and a half MPG. The trained model misses by three and a half, about forty-five percent better, on cars it never trained on. The five rows are the first five held-out cars in file order, not a highlight reel.
>
> Still, look at the Ford: predicted eleven, actual fifteen. Two features and a straight line capture real signal about fuel economy, but they leave real error behind. And the setting matters: these cars are from the seventies and early eighties, the split is every fifth row rather than a random draw, and nothing here rates any modern car.

Do not call this modern-car validation, a random split, or causal evidence that
changing one feature produces the coefficient's effect. Both coefficients refer
to standardized features. The test set evaluates this fixed experiment; do not
adjust features, learning rate or step count in response to its results.

### G. Recap and next step | 13:15-14:00

Show a short itemized recap on screen:

- Backward rules for sum and matrix multiplication
- A finite-difference gradient check
- Full-batch training and a held-out MPG comparison

> We started with a loss we could compute but couldn't differentiate. Two backward rules, one for the sum inside the mean and one for the matrix multiplication, opened the path. A finite-difference check verified the new gradients, and a thousand steps of gradient descent trained a linear regression that beats the average-MPG baseline on cars it never saw.

Proposed follow-up scope, not a recorded or completed next episode. Keep the
on-screen list short:

- Nonlinear activation
- Its backward rule
- Fit a nonlinear relationship

> This model can only draw a straight line through the data, and plenty of real relationships are not straight lines. Next we'll add a nonlinear activation, write its backward rule, and fit a pattern a linear model can't reach.

> That brings us to the end of this episode. Thanks for watching, and I will see you next time.

Hold five clean seconds after speech for Subscribe and the complete-series
playlist. No code, recap text or Q&A under those elements.

## Production and verification notes

- Existing tensor data/grad access and shared-node semantics remain unchanged.
  The model uses two-dimensional weights and a scalar bias; no general
  optimizer, detach(), clone(), requires_grad or no_grad is added.
- Do not backpropagate through a graph after mutating values it needs. The
  finite-difference probes build a fresh graph per evaluation, and the training
  loop's temporary graphs leave scope each iteration.
- The data helper is transparent prepared source with attribution, reviewed off
  camera. Fixed systematic holdout: every fifth complete row, 313 training and
  79 test. Training-only feature standardization, targets in MPG. Learning rate
  0.05 and 1,000 steps are chosen for training convergence, not tuned to test
  MAE. No claim of universal defaults.
- Every edited stage compiles. The single intentional non-running stage is the
  pre-rules backward call in section A, which is the cold-open demonstration,
  verified against the checkpoint (exit 134 on the uncaught std::logic_error).
  Record that run in a normal terminal so the two status lines flush before the
  stop; fully buffered capture can interleave them.
- No transpose API or auxiliary autograd graph is needed for matmul backward.
  The explicit loops implement the same first derivatives as G times
  B-transpose and A-transpose times G. Leave those identities in this note;
  no separate algebra primer.
- Existing empty-versus-singleton broadcasting is a known baseline defect at
  7021cfe; this episode does not touch or claim to fix it.
- Verification of this draft, September 11, 2026: all nine literal edits were
  applied mechanically to the checkpoint main.cpp in temporary files (each
  Before matched its evolving source exactly once), compiled with Apple Clang
  in C++23 mode at -O1, and run from the repository root. The section A stage
  stops with the expected uncaught logic_error after printing the two status
  lines. The complete draft reproduces every measured line shown above,
  including Test 1-24 and Success afterward, and is clean under
  AddressSanitizer and UndefinedBehaviorSanitizer. These match the
  corresponding lines in [verification.md](verification.md) and
  verification-run.json, which remain the chapter's canonical record; rerun the
  chapter verifier against this edit sequence if any block changes. The
  off-camera 195-comparison gradient suite, split/scaling checks and the
  independent least-squares comparison described there apply unchanged.
- First-stage data plumbing pastes as one block; the meaningful typed lines are
  the model expression, the loss and the backward call. No dot() is used
  anywhere in the training path.
- Primary production risk: the matmul helper concentrates the episode's hardest
  reasoning into one section. Explain the single-product derivatives once,
  beside the forward loop, and keep the index explanation to one pass while
  typing. Rehearse the whole episode; if it exceeds 15 minutes, move the live
  finite-difference check to the off-camera suite before cutting derivative
  reasoning or held-out evaluation.

## Checklist audit

Written-script assessment, September 11, 2026. Per the playbook rubric, PASS
awards full weight; shortfalls are marked PARTIAL with a named repair. This
draft's nine-edit sequence was replayed today as described in the verification
notes. Recording timing remains an estimate.

| ID | Status | Points | Evidence / remaining risk |
| --- | --- | ---: | --- |
| L01 | PASS | 10 | Opening states the deliverable (train linear regression on real cars with our own autograd), the concrete limitation (backward stops at sum and matmul, demonstrated by 0:55) and the scope boundary (two features, linear model, fixed split). Matches Episode 8's recorded caption promise. |
| L02 | PASS | 10 | First sentence and first frame both point at training on real car data. No greeting, series premise, roadmap, recap or setup commands. |
| L03 | PASS | 8 | Data plumbing pastes during the first sentences; the prediction line is typed by 0:15 and the initial loss is measured by 0:30 as explicit rehearsal targets. |
| L04 | PASS | 8 | Payoff by about 0:55: a real computed loss (609.119) and the demonstrated backward stop on our own error. The gap is shown running, not described. Verified against the checkpoint. |
| L05 | PASS | 8 | A measures the loss and names the gap; B differentiates reductions; C differentiates matrix products and produces real gradients; D verifies one independently; E trains; F scores held-out cars. Six checkpoints spread across the runtime. |
| L06 | PASS | 8 | Sum rule appears when backward reaches it; matmul rule when it is the remaining gap; learning rate with the first update; mean absolute error at evaluation. No standalone theory primer. |
| L07 | PASS | 8 | Both local derivatives derived from one forward product; += justified by multiple outputs per entry; update order justified by current-weight gradients; final-loss recompute explained; bias slope hand-checked against the average MPG in E. |
| L08 | PASS | 10 | Nine literal Before/After edits, each matched exactly once against the evolving checkpoint and replayed today. All quoted outputs measured. The one intentional throw stage is labeled and verified. |
| L09 | PASS | 6 | Every on-screen run establishes new behavior. The 195-comparison suite, split/scaling checks and least-squares comparison stay off camera and are cited from verification.md. |
| L10 | PASS | 5 | Highlight plan names the sum case, the forward product's factors, the += pair, step prints, MAE lines and the Ford row. |
| L11 | PARTIAL | 2.5 | 1,307 spoken words measured on this draft, comparable to the parallel draft's 1,248; the runtime saving comes from one model build and six checkpoints instead of two builds and eight. Projected 11.5-13.5 minutes but unrehearsed. Named repair: if rehearsal exceeds 15 minutes, move the live finite-difference check off camera. |
| L12 | PASS | 4 | The promised capability is demonstrated and its limits stated. The next capability (nonlinear activation, its backward rule, fitting what a line cannot) arises from the demonstrated limitation, with no fabricated release promise. |
| L13 | PASS | 4 | Itemized recap, three-item follow-up list, exact standard sign-off, five clean seconds, no Q&A. |
| L14 | PASS | 2 | MP4 filename at top; only `>` paragraphs are spoken; edits and checkpoints stay outside narration. |
| L15 | PASS | 2 | September 10-11 keyword research precedes drafting. Spoken terms audited against `>` lines: linear regression from scratch in C++ and autograd (A opening), mean squared error and broadcasting (A, B), backpropagation (A wall), matrix multiplication (A, C), gradient checking (D), gradient descent and learning rate (E), mean absolute error and held-out data (F). |
| L16 | PASS | 2 | The failure-first opening applies the Episodes 1-6 retention report (Episode 5's contradiction opening was the strongest) as a transfer hypothesis; measure retention at 0:15, 0:30, 0:45, 1:00 and 2:00 after publication. Observation, explanation and creator direction kept separate. Remaining checks: rehearsal pacing, final-media review, caption recheck. |

## Critique

The failure-first opening is this draft's biggest bet. Viewers who clicked
"training" watch about a minute in which training cannot start. The retention
report supports a concrete failure as the entry point, and the loss is computed
first so the minute still contains real forward progress, but the bet should be
measured at 0:15-1:00 rather than assumed. If the opening sags, the repair is a
shorter path to the wall, not a return to explaining.

Removing the scalar toy loop removes the one moment where training succeeds
with zero new machinery. The off-camera suite retains a synthetic convergence
check, so rigor is preserved, but on camera the first successful training is
the real-data run near minute nine. The draft compensates with five earlier
payoffs (measurable loss, the wall, real gradients, the gradient check), yet if
rehearsal feels like a long road to the first win, a sixty-second scalar
warm-up is the fallback addition, not more narration.

The single-edit matmul helper concentrates the hardest reasoning. The
one-product derivation and the plus-equals justification must survive the edit;
if the presenter finds the double update confusing in rehearsal, split the
helper at the two += lines, not the chain-rule reasoning.

A measurement note for comparison: the parallel draft's audit table marks L08
and L09 PASS while awarding 8 of 10 and 8 of 6 points. This audit applies the
rubric's PASS-equals-full-weight rule uniformly, which is why the same total
here rests on consistent arithmetic.

## Final score

Most important remaining weakness: pacing is unrehearsed, and the matmul
section is the runtime risk inside an 11.5-13.5 minute projection.

Score: **97.5/100. Decision: advance to recording rehearsal.**
Code verification for this exact edit sequence passes, including the
intentional cold-open stop. L11 retains half credit until rehearsal. This is a
sequential self-review, not an independent review or measured retention, and
neither the score nor advancement authorizes release.
