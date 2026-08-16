# Milestone 3.1 — Stored Strides, Offsets, and Views

## Motivation

The first tensor assumes owned contiguous row-major storage and rebuilds strides
on every checked access. This milestone redesigns layout as explicit metadata so
indexing is cheap and transpose/slice operations can eventually describe
zero-copy views.

## Learning objectives

- Separate logical shape from physical layout.
- Derive offsets using stored strides and a storage offset.
- Explain contiguous and non-contiguous layouts.
- Design shared storage ownership and view lifetimes deliberately.
- Identify aliasing and mutation hazards before implementing views.
- Measure indexing and copy behavior before and after redesign.

## Initial diagnostic

Given a contiguous `[2,3]` tensor with strides `[3,1]`, predict what metadata
could describe its transpose as shape `[3,2]` without moving any numerical
values.

## Initial non-goals

- Broadcasting
- General tensor arithmetic optimization
- Autograd through views
- GPU or parallel execution
- Multiple dtypes

## Gate

The learner must derive view offsets, explain shared ownership and aliasing,
implement and validate stored layout metadata, and distinguish contiguous from
non-contiguous tensors before adding general view operations.

## Decisions

- [`Decision 0004 — Tensor Copy and View Semantics`](../decisions/0004-tensor-copy-and-view-semantics.md)

## Evidence

- Derived zero-copy transpose of `[2,3]` as shape `[3,2]`, strides `[1,3]`.
- Distinguished base offset from axis strides using row and column views.
- Derived the largest reachable non-empty offset and the separate empty-view
  rule permitting offsets through one-past-the-end.
- Implemented stored contiguous strides and a base offset in the learner-authored
  tensor. Checked indexing now uses stored metadata without per-access
  allocation.
- Strict warnings and all 15 tests pass under both normal and ASan/UBSan
  configurations.
- Numerical storage now uses shared ownership. Ordinary copy construction
  materializes logical values into independent contiguous storage; copy
  assignment uses a fully constructed temporary plus non-throwing generic swap.
- Sixteen tests pass under strict and sanitized presets, including independent
  copy assignment.
- Implemented rank-two `T()` by swapping shape and stride axes while retaining
  the source allocation and offset.
- Mechanical tests demonstrate correct transpose coordinates, mutations visible
  through both aliases, deep independent materialization when copying a view,
  and rejection of non-rank-two inputs. Nineteen tests pass under strict and
  ASan/UBSan presets.

## Current review finding

The first view exposed a latent assumption in existing kernels: `sum()` and
`elementwise_binary()` iterated the entire backing allocation directly. Both now
traverse logical coordinates; elementwise operations allocate only their
contiguous output. Transpose arithmetic is covered, and all 20 tests pass under
strict and ASan/UBSan presets.

The remaining limitation is evidentiary and functional: a full transpose still
uses every backing element and preserves offset zero. The next view must expose
only a subset of the allocation at a nonzero offset.

That subset view is now implemented as `select(axis,index)`. It removes the
fixed axis from shape and strides and advances the inherited offset by
`index * strides[axis]`. Tests cover middle and final axes, bidirectional
aliasing, chained scalar selection, invalid inputs, and layout-aware subset
computation. All 23 tests pass under strict and ASan/UBSan presets.

The remaining gate is a precise contiguity definition and learner defense of
the current ownership, aliasing, and layout behavior.

Contiguity is now defined as logical row-major traversal occupying consecutive
physical positions, independent of base offset. The learner derived the
right-to-left expected-stride algorithm, the size-one-axis exception, and the
scalar/empty conventions. Tests include a noncanonical ignored stride produced
by transposing a `[1,3]` tensor. All 24 tests pass under strict and ASan/UBSan
presets.

The implementation portion and mastery review are complete. The learner:

- distinguished ordinary deep copies, C++ references to the same object, and
  distinct view objects sharing numerical storage;
- derived transpose and chained-selection metadata, correcting one selected-row
  value error through the stride/offset mapping;
- explained copy-of-view materialization and corrected the attribution:
  `materialize()` orders values while the public constructor restores canonical
  strides;
- retrieved the non-empty maximum-reachable-index formula and the separate
  empty-view representation policy;
- derived contiguity, including offsets, size-one axes, scalars, and empty
  tensors; and
- synthesized the redesign as stored shape/stride/offset metadata mapping tensor
  coordinates into a shared contiguous backing allocation.

The obsolete public `storage()` accessor was removed after the learner
identified that returning the entire backing allocation is misleading for
views, while silently materializing would hide allocation and copy costs.

## Retrospective

The original representation conflated a tensor's row-major element sequence
with its entire owned allocation. The redesigned representation separates
tensor coordinates from physical storage mapping. This enabled zero-copy
transpose and selection views but forced every kernel and public API to confront
layout, aliasing, and hidden-allocation semantics explicitly.

Milestone 3.1 passed on 2026-07-25.

## Copy-of-view decision

An ordinary copy of a view materializes its logical values into a new contiguous
allocation. Copy work therefore scales with logical `numel`, but custom copy
logic must traverse arbitrary shape, stride, and offset metadata correctly.
