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
- A high-value arithmetic branch produced equal-shape elementwise addition,
  with normal and sanitized execution of a known output.
- Equal-shape elementwise multiplication followed; complete known addition and
  multiplication outputs now pass strict and sanitized builds.

The learner chose to defer direct scalar, rank-mismatch, per-axis bounds, and
zero-sized indexing demonstrations. These are now mechanically covered by the
Codex-authored test harness but still do not count as learner mastery evidence.

The copy/move observation is also incomplete: direct access to the moved-from
object terminated with `std::invalid_argument`, and the planned reassignment
demonstration was deferred. Automated coverage now passes, but conceptual
retrieval remains required.

The learner also deferred the focused tensor test file and chose to begin
elementwise arithmetic. This is allowed as a high-value branch for momentum,
but Milestone 2.1 remains open. Codex has since supplied the mechanical test
harness under the updated workflow agreement.

Full sum reduction was implemented with rank-0 output and additive-identity
empty semantics. Ordinary scalar access is now exercised through rank-1 dot
product: the known result `14` passes strict and sanitized execution. Empty
reduction remains open.

Seven tensor tests and all eight pre-existing tests pass under both strict and
sanitized presets. The remaining gate is learner explanation, not behavior.

## Mastery gate result

Passed on 2026-07-24. In live retrieval, the learner correctly explained:

- why tensor copies deeply own independent vector allocations while moves
  cheaply transfer vector ownership;
- destruction and reassignment guarantees for moved-from tensors, after
  correcting the overly strong claim that assignment was the only safe action;
- the rank/storage distinction among scalar `[]`, singleton `[1]`, and empty
  `[0]`;
- why overflowing nonzero shapes are rejected while any zero-dimensional shape
  has zero elements;
- row-major stride derivation and offset-as-dot-product;
- the single shape-product/storage-size invariant, after correcting the claim
  that scalars were an exception; and
- the per-access cost of recomputing and allocating strides.

Together with strict and sanitized contract coverage, this satisfies Milestone
2.1. Stored strides, offsets, views, shared storage, and non-contiguous layouts
now become Phase 3 redesign subjects rather than patches to this deliberately
limited first tensor.
