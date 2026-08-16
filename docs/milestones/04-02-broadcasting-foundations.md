# Milestone 4.2 — Broadcasting Foundations

## Motivation

A dense layer produces a matrix of activations and adds one learned bias per
output feature. Requiring callers to manually copy the bias vector across every
batch row would obscure the mathematics and waste storage. Broadcasting
describes that repeated logical use without materializing repetitions.

## Dependencies

- Milestone 3.1 — Stored Strides, Offsets, and Views
- Milestone 4.1 — Matrix Multiplication Reference Kernel
- Equal-shape elementwise operations

## Learning objectives

- Derive dimension compatibility by right-aligning shapes.
- Distinguish missing, equal, and size-one dimensions.
- Compute broadcast output shapes and map output coordinates back to each input.
- Explain why broadcasting can be represented with zero strides.
- Implement a clear reference path before considering iterator or kernel
  optimization.
- Reject incompatible shapes precisely.

## Initial orientation

This unit implements the shape and coordinate rules needed for operations such
as `[batch,features] + [features]`. It directly unlocks bias addition after
matrix multiplication and is therefore the next shortest step toward dense
model training.

The first artifact will generalize elementwise addition and multiplication to
broadcast-compatible shapes. Full NumPy/PyTorch API parity, in-place broadcast
mutation, named axes, batched matrix multiplication, and broadcast autograd are
deferred.

Skipping broadcasting would force explicit bias replication and make later
gradient-reduction rules harder to motivate.

## Initial diagnostic

For shapes `[2,3]` and `[3]`, derive the output shape and map several output
coordinates to coordinates in both inputs.

## Implementation checkpoint

The learner derived and implemented:

- right alignment by prepending logical size-one dimensions;
- output extent selection using equal-or-one compatibility, including the fact
  that `max(a,b)` is wrong for the compatible pair `0` and `1`; and
- zero effective strides for logically repeated broadcast axes.

The first effective-stride draft exposed two implementation hazards:

1. padded aligned shapes have output rank, while stored operand strides retain
   operand rank, so advancing both reverse iterators together can exhaust the
   stride iterator on missing leading axes; and
2. each operand must derive effective strides from its own stored strides.

The next implementation step is to correct that mapping, then traverse the
output coordinates using each operand's offset and effective strides.

The corrected mapping passed compilation. The first full traversal then
demonstrated a classic iterator-state bug: it calculated indices from the
all-zero logical coordinate on every iteration because the coordinate was never
advanced. Existing equal-shape, transpose-view, and selected-view tests all
reported repeated first-element results, providing independent evidence of the
same cause. Output-size calculation also needs the established zero-dimension
and checked-multiplication semantics.

The traversal and output-size contracts are now corrected. Strict and
ASan/UBSan configurations each pass 30 tests, including matrix-plus-bias,
rank-three broadcasting, scalars, non-contiguous views, empty dimensions, and
invalid shapes. The implementation portion of the gate is complete; backward
gradient reduction remains as the conceptual mastery check.

The conceptual gate passed. For `[2,3,4] + [3,1]`, the learner identified the
missing leading axis and expanded final axis as the reduction axes. They also
distinguished reference identity from arithmetic accumulation: zero-stride
mapping makes repeated uses reach the same operand element, but the backward
rule must explicitly add all path contributions.

Status: completed 2026-07-26.

Learning artifact:
[`docs/learning/phase-4/broadcasting-foundations.md`](../learning/phase-4/broadcasting-foundations.md).

## Gate

The learner must derive right-aligned compatibility and coordinate mapping,
implement and test reference broadcasting including scalars, size-one axes,
views, empty dimensions, and invalid shapes, and explain which broadcasted axes
future backward propagation must reduce.
