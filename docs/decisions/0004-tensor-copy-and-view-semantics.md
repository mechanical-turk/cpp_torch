# Decision 0004 — Tensor Copy and View Semantics

## Status

Accepted 2026-07-24.

## Context

Phase 3 introduces shared numerical storage so transpose and slice operations
can return distinct tensor objects without copying values. A generated copy
operation over `std::shared_ptr` would also share storage, changing the first
tensor's established value semantics.

## Decision

- Ordinary tensor copy construction and copy assignment produce independent
  numerical values.
- Explicit view-producing operations such as `transpose()` return distinct
  tensor metadata sharing the source allocation.
- Mutations through an explicit view are visible through all aliases of that
  allocation.
- A C++ reference aliases the same tensor object and is not a substitute for a
  view, because it cannot hold independent shape, stride, or offset metadata.
- Do not add `clone()` while ordinary copying already provides the same deep-copy
  capability.

## Consequences

- `Tensor b = a` retains value-like semantics but requires custom copy
  operations after storage becomes shared.
- View construction requires an internal path that deliberately shares storage.
- Copying a view produces an independent tensor rather than another alias.
- Copying a view materializes its logical values into a new compact contiguous
  allocation. The copy preserves logical shape and values but resets its offset
  and strides to the corresponding contiguous layout.
- Move operations should remain cheap ownership/metadata transfers.
- Future autograd design must distinguish explicit view aliasing from ordinary
  independent copies.

This choice makes ordinary copy cost scale with logical `numel` rather than the
potentially much larger hidden allocation. It requires correct arbitrary-layout
traversal during copying and does not preserve physical layout metadata.
