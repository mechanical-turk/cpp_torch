# Milestone 2.1 — Contiguous Tensor Representation

## Motivation

Build the smallest reusable dense CPU tensor representation before arithmetic,
autograd, modules, or neural-network layers obscure its storage and shape
invariants.

The first tensor stores only `double` values in contiguous row-major order. It is
deliberately replaceable: strides, views, aliasing, devices, and dtype machinery
belong to later phases.

## Dependencies and diagnostic

- Milestone 1.2 complete
- `std::vector`, value semantics, and basic multidimensional indexing are assumed
  but must be assessed in the concrete tensor representation

Begin by deriving what information distinguishes a tensor from a flat vector and
what invariants must hold between logical shape and physical storage.

## Learning objectives

### Mathematics and ML

- Distinguish rank, shape, number of elements, and scalar storage.
- Convert row-major multidimensional indices to a flat offset.
- Explain why tensor shape is metadata while storage contains numerical values.

### C++ and systems

- Design a minimal value-semantic tensor owning contiguous `std::vector<double>`
  storage.
- Establish constructor invariants and exception guarantees.
- Detect overflow while computing the product of dimensions.
- Define scalar and zero-sized-dimension behavior deliberately.
- Compare checked and unchecked indexing boundaries.
- Observe copy and move behavior before adding shared storage or views.

## Hands-on sequence

1. Diagnose rank/shape/storage/offset concepts.
2. Specify scalar and empty-tensor semantics.
3. Implement shape validation and overflow-safe element-count calculation.
4. Implement construction from shape and values.
5. Add rank, shape, size, data, and checked indexing behavior.
6. Validate copies, moves, bounds failures, and sanitizer behavior.
7. Complete the representation mastery gate before numerical operations.

## Initial non-goals

- Elementwise arithmetic, reductions, matrix multiplication, or broadcasting
- Autograd
- Strides, offsets, views, non-contiguous tensors, or shared storage
- Dtypes other than `double`
- GPU or parallel execution

## Acceptance criteria

- Shape and storage-size invariants cannot be violated through the public API.
- Element-count multiplication detects overflow.
- Row-major offset derivation and implementation agree across ranks.
- Scalar and zero-sized shapes have explicit, tested semantics.
- Copy and move behavior is explained and observed.
- Strict and sanitized configurations pass.
- The learner can defend the representation's limitations and identify the later
  redesign pressure from views and non-contiguous layouts.

## Initial gate

Given shape `[2, 3, 4]`, explain what the three dimensions mean, how many values
storage contains, and what additional information is required to locate element
`[1, 2, 3]` in a flat row-major vector.

## Evidence log

- The learner derived `[12,4,1]` strides and offset `23` for `[1,2,3]`.
- Scalar `[]`, singleton `[1]`, and empty `[0]` semantics were distinguished.
- Shape/storage agreement and overflow-safe element counts were implemented.
- Checked row-major indexing returns the expected values for rank-3 examples.
- An unsigned reverse-loop underflow was reproduced and diagnosed with ASan,
  corrected, and then verified under strict warnings plus ASan/UBSan.
- Const and mutable element-access overloads share one checked offset helper;
  mutation through `double&` was observed and sanitized.
- The representation was promoted to `include/cpp_torch/tensor.hpp` and
  `src/tensor.cpp`. The obsolete production math scaffold was removed, the
  basic consumer now uses `Tensor`, and the complete `dev` build plus eight
  pre-existing tests pass.

The learner chose to defer direct scalar, rank-mismatch, per-axis bounds, and
zero-sized indexing demonstrations. These remain validation debt and do not
count as completed mastery evidence.

The copy/move observation is also incomplete: direct access to the moved-from
object terminated with `std::invalid_argument`, and the planned reassignment
demonstration was deferred.
