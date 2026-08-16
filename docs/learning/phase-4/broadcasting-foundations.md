# Broadcasting Foundations

## Purpose

Broadcasting lets elementwise operations reuse an operand logically across
dimensions without allocating repeated copies. The immediate model-training
case is adding a bias vector of shape `[features]` to an activation matrix of
shape `[batch, features]`.

## Demonstrated mental model

- Shapes are compared from the right.
- Missing leading operand dimensions behave as dimensions of size one.
- Two aligned dimensions are compatible when they are equal or either is one.
- The output extent is the non-one extent, or the common extent when equal.
  This must be expressed by cases rather than `max`: dimensions `0` and `1`
  are compatible and produce output extent `0`.
- A broadcast dimension uses effective stride zero. Changing that output
  coordinate therefore keeps reading the same operand element.
- Zero-stride reuse avoids the allocation and copying required to materialize
  repetitions.

## Reference implementation

The elementwise kernel:

1. right-aligns both shapes;
2. derives the compatible output shape;
3. derives output-rank effective strides for both operands;
4. traverses every logical output coordinate;
5. maps that coordinate to each operand using its offset and effective strides;
6. applies addition or multiplication; and
7. returns a new contiguous output tensor.

Missing leading axes and original size-one axes receive effective stride zero.
All other effective strides preserve the operand's stored strides, so
non-contiguous views remain valid inputs.

## Corrections and evidence

- The first stride draft advanced through a padded shape and an unpadded stored
  stride vector together. Rank-mismatched operands could therefore exhaust the
  stride vector. The corrected form computes the leading padding explicitly.
- The first traversal repeatedly produced the first output value because it
  never advanced the logical output coordinate. Existing equal-shape,
  transpose-view, and selected-view tests exposed the common cause.
- An old test treating shapes `[2]` and `[1,2]` as incompatible was corrected:
  they are compatible after right alignment.
- Output-size calculation preserves scalar size one, returns zero for any zero
  dimension, and checks multiplication overflow.

Strict and ASan/UBSan configurations each pass all 30 tests. Broadcasting
coverage includes trailing dimensions, size-one dimensions, scalars,
non-contiguous transpose views, empty dimensions, and incompatible shapes.

## Retrieval question

When an operand was broadcast along an axis during the forward pass, explain
why its backward gradient must sum contributions over that output axis rather
than retain one gradient entry per repeated logical use.
