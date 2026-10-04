# MNIST model comparison: findings

September 15, 2026. [Measured tables](results.md) · [Protocol](README.md).

## What the measurements support

1. The current model was chosen for teaching simplicity, not optimal MNIST
   accuracy. Its validation accuracy improved from 91.65% at epoch 5 to
   94.15% at epoch 15 with seed 42 and unchanged architecture. The second seed
   improved from 91.70% to 93.25%. Five epochs is not a demonstrated stopping point.
2. Width alone did not provide a clear benefit in this budget: shuffled
   128-unit Tanh reached 93.85%, versus 94.00% for shuffled 32-unit Tanh.
   Treat the small difference as inconclusive rather than declaring smaller
   networks universally better. The lower learning rate remained behind after
   fifteen epochs; that does not rule out benefits with a longer schedule.
3. The strongest tested recipe was 784 -> 128 -> 64 -> 10, ReLU after both
   hidden layers, SGD learning rate 0.1, batch size 64 and shuffled epochs.
   Validation accuracy was 95.30% and 94.95% across two initialization seeds.
   Baseline results were 94.15% and 93.25%. Selection used seed-42 epoch-15
   validation loss; the second seed is a limited confirmation, not a confidence interval.
4. The deeper ReLU model had 98.83%/98.60% training accuracy, so its validation
   gap was 3.53/3.65 percentage points. Nevertheless, validation loss fell at
   every measured checkpoint. There is no observed validation-loss reversal
   through epoch 15. More capacity fits training data more closely, but this
   sweep does not establish the stopping point or prove harmful overtraining.
5. Increasing depth helped in the wider ReLU comparison while adding only
   about 7.5% more parameters (109,386 vs 101,770). It cost much more than the
   original 25,450-parameter baseline. Timings include evaluation and are
   local workflow measurements, not isolated benchmark rankings.

## Recommendation and boundaries

Use the deeper ReLU model as the leading candidate for further accuracy work.
Test a larger training split and longer training next, with fixed validation
data, rather than immediately adding more layers. Keep the official test set
for evaluating a frozen choice. This sweep did not tune dropout, weight decay,
initialization, Adam, momentum or augmentation and cannot claim best-known MLP.

For the current episode, training longer is the smallest potential change;
introducing another hidden layer and ReLU is a separate architecture decision.
No architecture, epoch count, training subset or learning-rate change was
silently applied to the recording script. It received only progress output.

Stack hidden transformations with nonlinearities and one final ten-class
output head. Chaining full classifier objects is possible, but narrowing to
ten intermediate digit scores is unnecessary for the depth experiment.

The previous 88.2% score was measured on a different, official test subset.
Do not present this sweep's 95.3% validation score as a like-for-like test gain.
No selected-model test score was collected by this comparison.
