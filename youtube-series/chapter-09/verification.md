# Episode 9 verification: batch-only linear regression

Verified September 13, 2026. This supersedes the row-wise scalar-weight draft.
It checks the script and completed episode implementation, not the full Tensor
library.

## Reproduce

From Content HQ:

```sh
node youtube-series/chapter-09/verify-script.mjs --export
```

The verifier replays all 10 literal Before/After edits from Episode 8 checkpoint
`7021cfe`. The baseline, trained model, gradient regression and feature-count
regression programs pass under Clang C++23 with AddressSanitizer and
UndefinedBehaviorSanitizer.

The working `main.cpp` remains unchanged. `--export` writes the completed preview
to `scratch/examples/linear-regression/episode09.cpp` in the long-form source
repository.

- Working-source SHA-256 at verification time: `687fdf712891a36ac9020f09ff106fc520121e05bb4a483fc0440e0c279e4598`
- Script SHA-256: `1dc7ce9d53bde6a3ab25cadb0e50cf8fea02d317ffb95833ddcd4a52c190f21d`
- Replayed-source SHA-256: `91df6cb31938f2f7ebbad414e09ef2ecac514753308fa8eba91bcbcdb46a0f83`

[verification-run.json](verification-run.json) contains the full saved output.

## Implementation checked

The episode has one forward API:

```cpp
inputs.matmul(weights) + bias
```

`inputs` has shape `{rows, features}`, `weights` has shape `{features, 1}` and
`bias` is scalar. The script does not create a row-wise forward path or a vector
of scalar Tensor weights.

The training loop clears the weight and bias gradients, rebuilds the complete
forward graph, calculates mean squared error, calls backward and updates both
parameters. Sum backward distributes the incoming scalar gradient to every
input. Matmul backward computes contributions for both parents using the same
row, column and inner positions as the forward pass.

## Data and measured output

The example contains ten observations with one feature. Their targets follow
`y = 2x + 1`. Both trainable parameters start at zero.

```text
weight: 2
bias: 1
```

## Regression coverage

[gradient-checks.cpp](gradient-checks.cpp) performs 195 finite-difference
comparisons covering arithmetic broadcasting, rectangular and multi-column
matmul, reused operands, shared paths, repeated backward, lifetime, dot
composition, empty reductions, zero-inner matmul and validation.

[generalization-checks.cpp](generalization-checks.cpp) trains the batch-only
model with one, three and five input features, checks every recovered weight and
prediction, and rejects a mismatched weight shape.

## Remaining limits

- The example supports one output column.
- The inherited zero/singleton broadcasting defect remains outside this data.
- Sanitizer and finite-difference checks do not prove natural delivery, code
  legibility or a 7-9 minute final edit. Rehearsal is still required.
