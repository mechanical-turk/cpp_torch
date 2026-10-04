# MNIST MLP comparison

This is a research harness, not additional code to type during Chapter 12.
It replays the lesson's exact edits into a temporary source file and uses the
same Tensor, Linear, cross-entropy, backward and gradient_step implementation.
The live recording main.cpp is never changed.

Run from Content HQ:

```sh
node youtube-series/chapter-12/experiments/run.mjs
```

Results stream to the terminal and persist after every checkpoint in
[results.json](results.json). A rerun replaces that generated result file.

After completion, generate the readable tables:

```sh
node youtube-series/chapter-12/experiments/summarize.mjs
```

Open [results.md](results.md) for final-state comparisons and every measured
learning checkpoint.

## Controls and split

- 10,000 training images: original training rows 0 through 9,999.
- 2,000 validation images: original training rows 10,000 through 11,999.
- Official test images are never opened by the comparison harness.
- All candidates see the same data, pixel/255 normalization, 64-image batches,
  existing Linear initialization and plain SGD. No disabled compiler
  optimization, fast math, framework substitution or data augmentation.
- Fifteen epochs; evaluate after epochs 1, 5, 10 and 15. Training and validation
  loss/accuracy are measured with the same fixed weights at each checkpoint.
  These losses differ from the lesson's online mean accumulated during updates.
- Shuffled candidates use the same order seed. Unshuffled baseline reproduces
  the lesson's order. All seven initial comparisons use initialization seed 42.
- Repeat the baseline and the lowest epoch-15 validation-loss candidate with
  seed 43. This is a sensitivity check, not a many-seed statistical study.
- Timing includes full training/validation evaluation, allocations and data
  gathering. It is a local workflow cost, not an isolated kernel benchmark.

## Comparisons

Compare 32 vs 128 hidden units, Tanh vs ReLU, one vs two hidden layers,
learning rates 0.1 vs 0.03, fixed order vs shuffling, and training duration.
The two-hidden-layer model is 784 -> 128 -> 64 -> 10, with an activation after
each hidden layer and no activation on the final logits.

### Stacking MLPs

Whole MLP objects can be composed when their dimensions match and the final
loss backpropagates through both. For this task, extending the hidden stack
before a single ten-class output head is clearer. Passing ten digit scores
into another classifier introduces a narrow intermediate representation; it
does not automatically provide the benefit of richer hidden features.

The current MLP ends with a Linear layer. If another MLP begins immediately
with Linear, those two adjacent affine maps can be combined into one affine
map. The nonlinearities create the useful extra depth. Our two-hidden-layer
experiment therefore uses Linear -> activation -> Linear -> activation -> Linear.

Keep limitations visible: only part of the training set, a fixed validation
split, seven candidates, limited initialization repeats, and no optimizer,
regularization or initialization search. ReLU candidates retain the existing
Linear initializer rather than introducing He initialization. These results
do not identify the best-known MNIST MLP or prove depth cannot help.

## How to interpret overfitting

A training/validation accuracy gap measures generalization on this split.
Stronger evidence of training too long is training loss continuing to fall
while validation loss rises. Validation accuracy can remain flat while loss
worsens as wrong predictions become more confident. A gap alone does not
establish the epoch at which overfitting started.

Select architecture and stopping point with validation results. Only then
evaluate a frozen selected setup on the official test set. The earlier 88.2%
test-subset result is historical baseline evidence, not a validation score.

## External context

The [TensorFlow beginner example](https://www.tensorflow.org/tutorials/quickstart/beginner)
uses a 128-unit ReLU hidden layer, dropout and Adam. It is a useful small-model
reference, not proof of an optimal setup or a like-for-like result against our
smaller training subset and plain SGD. The
[Keras training guide](https://keras.io/guides/training_with_built_in_methods/)
demonstrates validation data held out from weight updates. Sources checked
September 15, 2026. No state-of-the-art claim is made.
