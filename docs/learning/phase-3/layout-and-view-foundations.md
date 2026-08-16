# Layout and View Foundations

## Milestone connection

- Phase 3 — Memory, architecture, and general tensor layouts
- Milestone 3.1 — Stored Strides, Offsets, and Views
- Status: first explicit zero-copy view complete; layout-aware kernels next

## Shape, strides, and offset

Shape describes logical extents. Strides and a base offset map logical indices
into physical storage:

```text
physical offset = base offset + sum(index[i] * stride[i])
```

For a contiguous `[2,3]` tensor, strides are `[3,1]`. A zero-copy transpose has
shape `[3,2]` and strides `[1,3]`; using `[2,1]` would instead describe a newly
contiguous allocation with rearranged values.

The base offset is the physical position corresponding to the view's logical
all-zero index. It is not specific to rows or the first dimension:

- second row `[d,e,f]`: shape `[3]`, stride `[1]`, offset `3`;
- second column `[b,e]`: shape `[2]`, stride `[3]`, offset `1`.

## View bounds

For non-empty shapes with non-negative strides, the greatest reachable position
is:

```text
offset + sum((shape[i] - 1) * stride[i])
```

It must be smaller than the allocation size. Empty views have no reachable
element, so the maximum formula is undefined and unsigned `shape[i]-1` would
underflow. Their offset may range through one-past-the-end because it is never
dereferenced.

## Ownership decision

Explicit views require distinct metadata sharing one numerical allocation. A
C++ reference cannot substitute because it aliases the same tensor object and
cannot carry different shape/stride/offset metadata.

Decision 0004 preserves deep, independent ordinary copies while explicit view
operations share storage. Consequently, generated `shared_ptr` copy behavior is
insufficient and copy operations must be custom. Moves remain defaulted and
`noexcept`; the implicit destructor is sufficient.

## Implementation evidence

The learner added stored contiguous strides and base offset while retaining the
original owned vector temporarily. Contiguous-stride calculation is a
translation-unit-private construction helper, not a public method that could
misreport a future view's actual strides. All strict and sanitized tests pass.

## Shared storage and deep copies

Storage was migrated to `shared_ptr<vector<double>>`. Public `storage()` returns
a borrowed const vector reference rather than exposing the ownership handle.
The learner distinguished `shared_ptr::get()` (raw pointer) from dereference
(pointee reference) and understood that borrowed-reference lifetime remains the
caller's responsibility.

Logical materialization traverses exactly `numel()` coordinates with an
odometer-style index, treating scalars as one visit and empty tensors as zero.
Two implementation errors were corrected:

- unsigned reverse traversal cannot use `i >= 0`;
- traversal count must use logical `numel`, not backing-storage size.

Copy construction materializes into independent contiguous storage. Copy
assignment provides the strong exception guarantee by constructing a complete
temporary before committing with `std::swap`. Generic swap uses one move
construction and two move assignments; the learner's explicitly defaulted
`noexcept` moves make this non-throwing.

## Copying a view

After comparing a complete `[2,3]` backing tensor with a two-element strided
column view, the learner chose compact materialization for ordinary copies.
`Tensor copy = view` will copy only logically reachable values, retain the
logical shape, and reset layout to contiguous strides with offset zero.

This avoids copying unused backing values and makes cost proportional to
`numel()`. The accepted implementation cost is a general logical traversal of
shape, strides, and offset.

## First explicit view: rank-two transpose

The learner implemented `T()` by constructing new metadata with swapped shape
and stride axes while retaining the same allocation and base offset. For an
original `[2,3]` tensor with strides `[3,1]`, the view has shape `[3,2]` and
strides `[1,3]`.

Mechanical tests establish the distinct contracts:

- transpose coordinates map to the expected physical values;
- mutations through either tensor are observable through the other;
- ordinary copying of the transpose materializes independent logical values in
  contiguous order; and
- transpose currently rejects tensors whose rank is not two.

All 19 tests pass under strict warnings and ASan/UBSan. These results verify the
implementation but the learner still needs to retrieve the semantic distinction
between a view, a C++ reference, and an ordinary tensor copy during the mastery
gate.

## Next retrieval question

Existing `sum()` and elementwise kernels still loop directly over backing
storage. A full transpose happens to retain the same allocation and logical
element set, but this does not establish correctness for general views with
offsets, unused elements, or differing traversal orders. The next step is to
predict current behavior before redesigning those kernels around logical
traversal.

## Layout-aware kernel checkpoint

The learner identified that using `materialize()` inside `sum()` would be
correct but would allocate and copy `O(numel)` input values unnecessarily.
`sum()` now keeps only an `O(rank)` logical index and reads view coordinates
directly.

Elementwise kernels similarly read both operands at matching logical
coordinates and allocate only the required contiguous output. A review caught
one remaining backing-storage assumption: the first revision sized its loop
with `storage_->size()` rather than logical `numel()`. After correction,
transpose addition and multiplication produce logical transpose order.

All 20 strict and ASan/UBSan tests pass. A subset view remains necessary because
transpose alone cannot prove correct behavior when logical `numel` is smaller
than the backing allocation or the base offset is nonzero.

## Axis selection

`select(axis,index)` fixes one logical coordinate and removes that axis:

```text
new shape   = old shape with shape[axis] removed
new strides = old strides with strides[axis] removed
new offset  = old offset + index * old strides[axis]
```

The learner initially reached for `strides[axis+1]`, then corrected the model:
the displacement is determined by the stride of the axis whose coordinate is
being fixed. No hypothetical entry after the final axis is required. Selecting
the sole axis of a rank-one tensor produces a rank-zero scalar view.

The implementation shares storage and validates both `axis < rank` and
`index < shape[axis]`. Tests cover rank-three middle and final axes, nonzero
offsets, mutation aliasing, chained scalar selection, invalid input, subset
reduction, and elementwise subset computation. All 23 strict and ASan/UBSan
tests pass.

## Revision topics

- Retrieve why `axis < 0` is not a meaningful check when the public axis type is
  `std::size_t`.
- Retrieve why subset kernels must use logical `numel()` rather than backing
  allocation size.
- Derive contiguity from shape and strides; do not equate it with owning storage
  or offset zero.

## Contiguity

Contiguity means that logical row-major traversal maps to physical positions
`p, p+1, p+2, ...` for some starting offset `p`. Storage before or after that
sequence is irrelevant.

For a nonempty tensor with more than one element, scan axes right-to-left with
`expected_stride = 1`. A dimension larger than one must have its actual stride
equal to the expected stride; then the expected stride is multiplied by that
dimension size. Size-one dimensions impose no stride constraint because their
only valid coordinate is zero. Scalars and empty tensors are considered
contiguous because neither can contain an internal gap.

The learner first used an invalid coordinate of `1` on a size-one axis, then
correctly enumerated the traversal and explained why its stride contribution is
always zero. The first `is_contiguous()` implementation accidentally skipped
zero-sized rather than size-one dimensions; review identified that empty
tensors had already returned early, and the condition was corrected.

Tests distinguish base, transpose, row, and column layouts and include
`[1,3].T()`: its shape `[3,1]` has a noncanonical stride on the size-one axis but
is still contiguous. All 24 strict and ASan/UBSan tests pass.

## API consequence

The old public `storage()` accessor returned the full backing allocation. After
subset views, that result no longer represented the tensor's logical values.
The learner chose to remove the accessor: raw backing access has no current
public use, while a future logical export should explicitly communicate its copy
cost (for example, `to_vector()`). Interoperability-oriented raw access can be
designed later with explicit contiguity, lifetime, and mutation contracts.

## Mastery outcome

Milestone 3.1 passed. The learner demonstrated the ownership, mapping,
copy/materialization, subset traversal, and contiguity models through prediction
and design defense. Revision should revisit the exact empty-view offset policy
and the distinction between coordinate generation (`advance_index`) and
coordinate-to-storage mapping (`storage_idx`).
