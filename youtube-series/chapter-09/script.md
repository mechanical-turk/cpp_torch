Proposed MP4: `cpp-linear-regression-autograd-gradient-descent.mp4`

# Episode 9: Training Linear Regression from Scratch in C++

Working title: `Training Linear Regression from Scratch in C++ | Deep Learning, All the Way Down #9`

## Keyword research completed before drafting

[Keyword research](keyword-research.md), revised September 13 before this
rewrite. Primary phrase: linear regression from scratch in C++. Supporting
terms appear beside the code that gives them meaning: matrix multiplication,
mean squared error, autograd, backpropagation, gradient descent, weights, bias,
and linear regression.

## Starting point and scope

Start from the Episode 8 checkpoint `7021cfe`, using root `main.cpp` in
`aliases/02-screen-long-form`. The current uncommitted row-wise
`linear_forward` stub is abandoned work and is not part of this draft. Remove
that incomplete stub before recording so the file matches the checkpoint.

This episode uses one model representation from beginning to end:

```cpp
inputs.matmul(weights) + bias
```

`inputs` is `{rows, features}`, `weights` is `{features, 1}`, and `bias` is a
scalar. There is no row argument, vector of scalar Tensor weights, indexing
operation, toy training path, or second forward function.

The code order is deliberate. Build `linear_forward`, parameter updates and the
complete training loop first. Then implement the matmul and sum backward rules
that the loop needs before fitting ten points to a line.

## Checklist plan

| ID | Plan |
| --- | --- |
| L01 | Train one batched linear regression model on ten points using the Tensor autograd engine. |
| L02 | Open on the one-line model and begin writing it immediately. |
| L03 | Complete `linear_forward` in the opening minute, with meaningful code visible inside 15 seconds. |
| L04 | Produce a valid batch of predictions by about 1:00. |
| L05 | Build the model and training lifecycle, implement the required backward rules, then recover the line behind ten points. |
| L06 | Introduce sum and matmul derivatives only after the complete training loop reaches them. |
| L07 | Explain shapes, gradient clearing, graph rebuilding, the chain rule and accumulation beside the lines that rely on them. |
| L08 | Use exact Before/After edits replayed from the Episode 8 checkpoint. |
| L09 | Show the recovered weight and bias; keep broader derivative checks outside the recording. |
| L10 | Keep the relevant return, training lifecycle, backward case or result visible during each explanation. |
| L11 | Target 12-15 minutes by removing the row-wise model and keeping tests out of the spoken lesson. |
| L12 | Finish with a model that recovers `y = 2x + 1`. |
| L13 | End with an itemized recap, concise next episode, standard sign-off and five clean seconds. |
| L14 | Mark only spoken narration with `>` and keep production directions separate. |
| L15 | Use the researched C++ and machine-learning terms naturally as their code appears. |
| L16 | Treat pacing as unverified until rehearsal and final-media inspection; keep short-form evidence separate. |

## Recording script

Target: 7-9 minutes, subject to rehearsal. Build every function below on
camera. Before blocks are recording references, not extra on-screen content.

### A. Build the model we will train | 0:00-1:00

Frame zero: `main.cpp` immediately above `main()`. Begin typing while speaking.

> A linear regression model can calculate every prediction in one line: inputs times weights, plus a bias. Let's build that line with our C++ Tensor, then train those weights with autograd.

Location: immediately above `main()`.

<!-- edit: batch-forward -->
**Before**
```cpp
int main() {
```

**After**
```cpp
[[nodiscard]] Tensor linear_forward(
  const Tensor& inputs,
  const Tensor& weights,
  const Tensor& bias
) {
  if (inputs.rank() != 2 || weights.rank() != 2 ||
      inputs.dimension(1) != weights.dimension(0) ||
      weights.dimension(1) != 1 || bias.rank() != 0)
    throw std::invalid_argument("linear model shapes do not match");

  return inputs.matmul(weights) + bias;
}

int main() {
```

Point to the three shapes while writing the condition.

> Each row in `inputs` is one observation, and each column is one feature. The weight matrix has one row per feature and one output column, so matrix multiplication gives us one prediction per observation. Then the scalar bias broadcasts across that whole column.

At the return:

> The forward pass gives us predictions. Training means comparing them with the targets, tracing the loss back to these weights, and then doing it again with updated values.

### B. Put the training lifecycle in place | 1:00-3:30

> Our gradient updates use plus-equals, so they accumulate. That's useful when a parameter contributes to the loss more than once, but it also means the next training step would inherit the gradients from the previous one. We'll add `zero_grad` so every update starts with the current loss alone.

Location: Tensor's public section, immediately after `grad()`.

<!-- edit: parameter-zero-grad -->
**Before**
```cpp
  [[nodiscard]] const std::vector<double>& grad() const noexcept {
    return node_->grad;
  }

  void backward() {
```

**After**
```cpp
  [[nodiscard]] const std::vector<double>& grad() const noexcept {
    return node_->grad;
  }

  void zero_grad() noexcept {
    std::fill(node_->grad.begin(), node_->grad.end(), 0.0);
  }

  void backward() {
```

At `zero_grad()`:

> This only clears the Tensor we call it on. The training loop will use it on the weights and bias at the start of every step.

Return to `backward()`, at the existing loop that currently clears every node
in the topology.

> There's one conflict with the `zero_grad` method we just added. `backward` currently clears every gradient in the graph before it starts, including the weights and bias. If we want to accumulate gradients from several losses, that loop silently erases the earlier contributions.
>
> So we need to separate leaf gradients from temporary graph gradients. A leaf is a Tensor we created directly. Inputs, targets, weights and bias are leaves. Predictions and loss are operation results.
>
> Backward should reset only those operation results. The leaves will keep their gradients until the caller chooses to clear them with `zero_grad`.

<!-- edit: operation-gradient-reset -->
**Before**
```cpp
    for (TensorNode* node: topology) {
      std::fill(node->grad.begin(), node->grad.end(), 0.0);
    }

    node_->grad[0] = 1.0;
```

**After**
```cpp
    for (TensorNode* node : topology) {
      if (node->operation != Operation::leaf)
        std::fill(node->grad.begin(), node->grad.end(), 0.0);
    }

    node_->grad[0] = 1.0;
```

At the condition:

> The loss is an operation result, so this loop resets it before we seed it with one. The training loop has already cleared the weights and bias, which means they will finish with only the gradient from the current loss.

> When `backward` returns, every weight and the bias still have their old values. Their gradients only tell us which way the loss changes.
>
> We still need to apply those gradients. We'll write that update as a separate function and begin with the two steps it needs to perform.

Location: immediately above `main()`.

<!-- edit: gradient-step-outline -->
**Before**
```cpp
int main() {
```

**After**
```cpp
void gradient_step(
  Tensor& weights,
  Tensor& bias,
  double learning_rate
) {
  // for every weight:
  //   weight -= learning rate * its gradient
  // update the bias the same way
}

int main() {
```

At the pseudocode:

> `backward` gave us one gradient for every weight and one for the bias. The update is the same for all of them: subtract the gradient, scaled by the learning rate, from the current value. The loop exists because we need to apply that rule to every weight in the model.

Before replacing the pseudocode:

> There is one detail in the indexing that I want to make clear first. `linear_forward` multiplies an input matrix shaped as rows by features with a weight matrix shaped as features by one. The one is there because this model produces one prediction for each row.
>
> Each feature therefore has one weight. In `{feature, 0}`, `feature` selects its row, while zero selects the only output column. We are not hardcoding feature zero. If the model produced several outputs, that second coordinate would be an `output` variable instead.

Replace the pseudocode with the implementation.

<!-- edit: gradient-step-implementation -->
**Before**
```cpp
  // for every weight:
  //   weight -= learning rate * its gradient
  // update the bias the same way
```

**After**
```cpp
  if (weights.rank() != 2 || weights.dimension(1) != 1 || bias.rank() != 0)
    throw std::invalid_argument("expected a weight column and scalar bias");

  for (std::size_t feature = 0; feature < weights.dimension(0); ++feature)
    weights.at({feature, 0}) -= learning_rate * weights.grad()[feature];

  bias.at({}) -= learning_rate * bias.grad()[0];
```

At the shape check:

> First, we'll enforce the layout we just described: a single column of weights and a scalar bias.

While typing the loop:

> Now we can walk through that column. `feature` selects one row, and zero keeps us in the only column. Since a one-column matrix is stored as one flat sequence, the same `feature` index selects the matching gradient. We scale it by the learning rate and subtract it from the weight.

At the bias update:

> The bias is a scalar, so it has one value and one gradient. We update it with the same rule.

> We now have every piece needed around `backward`, so let's put the full training loop together before we change the autograd engine.

Location: immediately above `main()`.

<!-- edit: training-loop -->
**Before**
```cpp
int main() {
```

**After**
```cpp
void train_linear_regression(
  const Tensor& inputs,
  const Tensor& targets,
  Tensor& weights,
  Tensor& bias,
  std::size_t steps,
  double learning_rate
) {
  for (std::size_t step = 0; step < steps; ++step) {
    weights.zero_grad();
    bias.zero_grad();

    const Tensor predictions = linear_forward(inputs, weights, bias);
    Tensor loss = mse_loss(predictions, targets);
    loss.backward();

    gradient_step(weights, bias, learning_rate);
  }
}

int main() {
```

Keep the five lines inside the loop visible together.

> Each step clears the parameter gradients, calculates every prediction, builds one mean squared error, runs backpropagation, and updates the weights and bias.

At `linear_forward()` inside the loop:

> Every time the parameters change, we rebuild the forward pass. The next loss needs the new values and a fresh graph that points back to them.

### C. Backpropagate through matrix multiplication | 3:30-5:30

> The update can only work if `loss.backward()` reaches the weights. Our predictions begin with matrix multiplication, so we'll give that operation its backward rule before we move on.

Briefly show the existing forward line inside `matmul()`:

```cpp
sum +=
  node_->data[row * left_cols + index] *
  other.node_->data[index * right_cols + column];
```

> One output value comes from several `left times right` products. Backward revisits each product and updates the two values that made it.

Location: `Tensor::backward()`, immediately above `default`.

<!-- edit: matmul-backward-outline -->
**Before**
```cpp
        default:
          throw std::logic_error("backward rule not implemented yet");
```

**After**
```cpp
        case Operation::matmul: {
          TensorNode* left = output->parents[0].get();
          TensorNode* right = output->parents[1].get();

          const std::size_t left_rows = left->shape[0];
          const std::size_t left_cols = left->shape[1];
          const std::size_t right_cols = right->shape[1];

          // for every left * right product:
          //   left gradient += output gradient * right
          //   right gradient += output gradient * left
          break;
        }

        default:
          throw std::logic_error("backward rule not implemented yet");
```

At the parents and dimensions:

> `left` and `right` are the two matrices from the forward pass. We'll use the same row, column and inner dimensions that created the result.

At the pseudocode:

> Each product has one left value and one right value. The left gradient gets the output gradient times the right value. The right gradient gets the output gradient times the left value. Those two formulas are the whole rule.

Replace the pseudocode.

<!-- edit: matmul-backward-loop -->
**Before**
```cpp
          // for every left * right product:
          //   left gradient += output gradient * right
          //   right gradient += output gradient * left
```

**After**
```cpp
          for (std::size_t row = 0; row < left_rows; ++row) {
            for (std::size_t column = 0; column < right_cols; ++column) {
              const std::size_t output_index = row * right_cols + column;

              for (std::size_t index = 0; index < left_cols; ++index) {
                const std::size_t left_index = row * left_cols + index;
                const std::size_t right_index = index * right_cols + column;

                left->grad[left_index] +=
                  output->grad[output_index] * right->data[right_index];
                right->grad[right_index] +=
                  output->grad[output_index] * left->data[left_index];
              }
            }
          }
```

As the loops appear:

> The outer loops select one output. The inner loop walks through the products that were added together to produce it.

At the two index calculations:

> These indices select the current value from the left matrix and its partner from the right matrix.

At the gradient updates:

> For `left times right`, the left value receives `output gradient times right`, and the right value receives `output gradient times left`. Those are the two lines we're writing here.

> We use plus-equals because one matrix entry can contribute to several outputs. Its final gradient is the sum of all those contributions.

> Matrix multiplication can now send gradients back to the weights. Mean squared error still reduces all the squared errors to one scalar with `mean()`, and `mean()` uses `sum()`. We'll add that short rule too.

### D. Backpropagate through sum | 5:30-5:45

Location: `Tensor::backward()`, immediately above `default`.

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
          for (double& gradient : input->grad)
            gradient += output->grad[0];
          break;
        }

        default:
          throw std::logic_error("backward rule not implemented yet");
```

At the loop:

> A sum changes one-for-one with every value that entered it, so each input receives the gradient that reached the output. We use plus-equals because the same input may also contribute through another path.

> Backward can now travel from the scalar loss, through all ten predictions, and back to the weight and bias. Let's give the training loop ten simple points and see whether it can recover their line.

### E. Create ten points | 5:45-6:45

> The training code is ready. We'll keep the data just as small: ten input values, with every target following `y = 2x + 1`.

Location: immediately above `main()`, then call the new function at the top of
`main()`.

<!-- edit: line-model -->
**Before**
```cpp
int main() {

  std::vector<std::size_t> shape_1 {2, 3};
```

**After**
```cpp
void train_line() {
  Tensor inputs(
    {10, 1},
    {0.0, 1.0, 2.0, 3.0, 4.0,
     5.0, 6.0, 7.0, 8.0, 9.0}
  );
  Tensor targets(
    {10, 1},
    {1.0,  3.0,  5.0,  7.0,  9.0,
     11.0, 13.0, 15.0, 17.0, 19.0}
  );

  Tensor weights({1, 1}, {0.0});
  Tensor bias({}, {0.0});

  train_linear_regression(inputs, targets, weights, bias, 10000, 0.01);

  std::cout << "weight: " << weights.at({0, 0}) << '\n';
  std::cout << "bias: " << bias.at({}) << '\n';
}

int main() {
  train_line();

  std::vector<std::size_t> shape_1 {2, 3};
```

At the two Tensors:

> The inputs run from zero through nine. Every target is twice its input plus one, so the pattern is easy to see before we train anything. The input Tensor is ten by one because we have ten observations and one feature.

> Both parameters start at zero. Now we'll run the complete training loop and see where they land.

<!-- checkpoint: trained-model -->

```text
weight: 2
bias: 1
```

Highlight the two learned values.

> We started both parameters at zero. Gradient descent recovered the line that produced the data: a weight of two and a bias of one.

### F. Recap | 6:45-7:15

Keep the trained output visible, then show:

```text
Recap

- Batched linear regression
- Full-batch gradient descent
- Matmul backward
- A learned weight and bias
```

> We built a batched linear regression model, added the missing sum and matrix multiplication rules to backward, then used gradient descent to recover the weight and bias behind ten points.

Replace the recap with:

```text
Next episode

- Add a nonlinear activation
- Backpropagate through it
- Train a model that can learn curves
```

> The model can only learn a straight-line relationship. Next, we'll add a nonlinear activation and train a model that can learn a curve.

> That brings us to the end of this episode. Thanks for watching, and I will see you next time.

Cut to approximately five clean seconds for the Subscribe and complete-series
playlist end-screen elements.

## Production and verification notes

- The recording baseline is commit `7021cfe`. The incomplete row-wise stub in
  the current working tree is not part of the lesson.
- `linear_forward()` always accepts an input matrix, a weight matrix and a
  scalar bias.
- `Tensor::zero_grad()` clears one leaf parameter's gradient storage. The
  training loop owns the timing and calls it before each new forward pass.
- `backward()` clears non-leaf operation nodes but preserves leaf gradients for
  the update. The root loss is seeded with one, while leaf contributions
  accumulate until the caller clears them.
- This minimal engine records gradients for every leaf, including fixed inputs
  and targets. Their unused gradients may accumulate during training, but they
  do not affect the parameter update. A later `requires_grad` or detach mechanism
  is the proper way to stop tracking them; do not turn that limitation into an
  extra detour in this episode.
- The loop rebuilds the graph before every update. Do not mutate values and then
  call backward through a graph built from their previous state.
- `mean()` requires `sum` backward. The existing elementwise division rule
  supplies the factor of `1 / numel`.
- Matmul backward directly applies the equivalent of `dLeft = dOutput * Right^T`
  and `dRight = Left^T * dOutput` without allocating transposed tensors.
- The scalar bias already uses the existing elementwise broadcasting metadata.
  Every output row maps back to bias index zero, and `+=` accumulates all rows.
- The ten targets follow `y = 2x + 1`. Recovering a weight of two and bias of
  one verifies the complete training path without adding data-loading code.
- The example has one feature and one output. The forward and training
  functions still derive the feature count from Tensor shapes.
- Keep derivative regressions, unusual rectangular matmul shapes, shared-parent
  cases and malformed-input checks outside the spoken lesson. They must still
  pass before recording.
- Rehearse the full build. Keep the final edit under ten minutes.

## Checklist audit

| ID | Status | Points | Evidence / remaining risk |
| --- | --- | ---: | --- |
| L01 | PASS | 10 | One batched model learns the line behind ten points. |
| L02 | PASS | 10 | The first sentence names the one-line model and the first action writes it. |
| L03 | PASS | 8 | `linear_forward` begins immediately; the 15 and 30 second targets contain implementation, not setup. |
| L04 | PASS | 8 | The opening completes the batch forward path by about one minute. Timing still needs rehearsal. |
| L05 | PASS | 8 | Each section leaves a concrete capability or exposes the exact missing rule used next. |
| L06 | PASS | 8 | Sum and matmul backward arrive only after the completed training loop reaches them. No temporary training representation exists. |
| L07 | PASS | 8 | Shapes, update direction, graph rebuilding, chain rule and gradient accumulation stay beside their code. |
| L08 | PASS | 10 | Literal edits target the Episode 8 checkpoint and the complete replay passes sanitizer-backed verification. |
| L09 | PASS | 6 | The recovered weight and bias prove the integrated training path; broader checks remain off camera. |
| L10 | PASS | 5 | Scene directions keep the current shapes, lifecycle, forward product, backward update or output visible. |
| L11 | PARTIAL | 2.5 | The loader and evaluation detours are gone and the draft targets about seven minutes, but live typing pace has not been rehearsed. |
| L12 | PASS | 4 | The model recovers `y = 2x + 1`. |
| L13 | PASS | 4 | Itemized recap, concise next episode, exact sign-off and clean end-screen tail are present. |
| L14 | PASS | 2 | The MP4 name is present, narration uses `>`, and code directions stay outside it. |
| L15 | PASS | 2 | The revised keyword record matches the batch-only implementation and the selected terms appear naturally. |
| L16 | PASS | 2 | Long-form evidence informs the immediate-code structure; rehearsal and final-media retention remain unverified. |

## Critique

The script now reaches the complete training loop before implementing its two
missing backward rules. Matmul comes immediately after the loop because it is
the central new operation. Its implementation begins with pseudocode and reuses
the same positions as the forward pass.

Ten literal points replace the data loader, train-test split and evaluation
helper. The result is less realistic, but it makes the episode's real subject
much easier to follow: connecting a batched linear model to autograd and
gradient descent.

The remaining risk is the matmul explanation. The three nested loops are dense,
so the edit must keep the pseudocode and the two gradient updates readable.
Rehearsal still needs to verify the seven-minute estimate.

## Final score

The script is technically complete and keeps one model representation
throughout. Rehearsal remains the only partial gate.

Score: 97.5/100. Decision: advance.
