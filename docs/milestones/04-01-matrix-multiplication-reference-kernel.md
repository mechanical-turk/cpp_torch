# Milestone 4.1 — Matrix Multiplication Reference Kernel

## Motivation

Matrix multiplication is the central forward operation in dense neural
networks, attention projections, and many future tensor workloads. The project
now has layout-aware tensors but lacks the operation needed to combine batches,
features, and learned weights.

## Dependencies

- Milestone 2.1 — Contiguous Tensor Representation
- Milestone 3.1 — Stored Strides, Offsets, and Views
- Milestone 3.2 — Tensor Traversal Cost and Memory Locality
- Basic dot products and summation notation

## Learning objectives

- Derive matrix multiplication from row/column dot products.
- State and defend rank and shape compatibility rules.
- Track output coordinates and reduction coordinates precisely.
- Implement a clear rank-two reference kernel that works for contiguous and
  non-contiguous input views.
- Design invalid-input behavior and numerical correctness tests.
- Connect loop order to layout and locality without prematurely optimizing.

## Initial orientation

This unit builds the first operation that directly unlocks dense-model forward
passes. The learner will derive the shape/value rules, implement the obvious
triple-loop reference kernel, test views and failures, and compare against
hand-computed examples.

Batched matrix multiplication, broadcasting, SIMD, tiling, BLAS, multiple
dtypes, and autograd are deferred. Skipping this unit would prevent meaningful
dense layers and delay the path to model training.

## Initial diagnostic

Given `A` of shape `[m,k]` and `B` of shape `[k,n]`, explain why the output has
shape `[m,n]` and identify which index is reduced to form output element
`C[i,j]`.

## Implementation artifact

A learner-authored rank-two matrix multiplication operation on `Tensor` using
the existing checked logical indexing path as the correctness reference.

## Gate

The learner must derive the operation and compatibility rule, implement and test
the reference kernel including non-contiguous inputs, explain its complexity and
memory-access patterns, and identify what future optimization would need to
measure.

## Evidence

- Derived `[m,k] × [k,n] → [m,n]` from row/column dot products and named the
  inner coordinate as a reduction index.
- Established that zero-length rows/columns have dot product zero through the
  empty-sum identity.
- Implemented a learner-authored public rank-two reference kernel using logical
  indexing for arbitrary input layouts and contiguous row-major output.
- Corrected public/private placement, output-row indexing, loop-variable role
  confusion, and pre-allocation output-size overflow validation during review.
- Mechanical tests cover known rectangular values, transpose-view operands,
  zero-sized dimensions, invalid ranks/shapes, and overflow.
- All 28 tests pass under strict warnings and ASan/UBSan.

The implementation gate is complete. The triple-loop implementation directly
establishes `O(mkn)` arithmetic and `O(mn)` output storage. A separate live
complexity quiz was waived at the learner's request because it had low marginal
value after the learner authored the loop structure and immediately completed
the dedicated locality milestone.

Loop-order benchmarking, matrix-specific locality analysis, tiling, SIMD, and
BLAS comparison remain explicitly deferred to the future kernel-optimization
branch. Milestone 4.1 passed on 2026-07-25.
