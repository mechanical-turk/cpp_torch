# Contiguous Tensor Foundations

## Milestone connection

- Phase 2 — Contiguous tensor foundations
- Milestone 2.1 — Contiguous Tensor Representation
- Status: representation checkpoint complete; checked indexing in progress

## Shape, rank, and scalar semantics

The learner established the recursive shape model:

- `[2,3,4]` contains two `[3,4]` subtensors;
- each `[3,4]` contains three `[4]` subtensors;
- flat storage therefore contains `2*3*4 = 24` scalar values.

For row-major shape `[2,3,4]`, the learner derived strides `[12,4,1]` and flat
offset `23` for index `[1,2,3]`.

Rank is the number of axes, not the number of stored values. The accepted scalar
and empty conventions are:

```text
shape []  → rank 0 scalar, one value
shape [1] → rank 1 singleton vector, one value
shape [0] → rank 1 empty vector, zero values
```

The learner connected `numel([])=1` to the recursive equation
`numel([4]) = 4 * numel([])`, identifying one as the multiplicative identity.

## Initial representation evidence

The learner authored a single-file value-semantic `Tensor` owning:

- `std::vector<std::size_t>` shape metadata;
- contiguous `std::vector<double>` storage.

Construction rejects storage whose size disagrees with the shape product.
Read-only accessors expose shape, storage, rank, and element count. Removing
redundant const `rank` and `numel` data members restored generated copy
assignment and eliminated duplicate sources of truth.

A concrete constructor bug demonstrated parameter shadowing and moved-from
state: validation accidentally read the moved-from `storage` parameter rather
than the owned member. Renaming members with trailing underscores corrected the
boundary.

## Overflow-safe element counts

Unsigned dimension multiplication is guarded before multiplication. For nonzero
dimensions, overflow is detected using the equivalent condition:

```text
dimension > max_size_t / current_product
```

Zero dimensions are pre-scanned so a mathematically zero-sized shape such as
`[max_size_t,2,0]` returns zero instead of overflowing before reaching the zero.
Observed evidence:

- `[max_size_t,2]` throws `std::overflow_error`;
- `[max_size_t,2,0]` with empty storage constructs and reports zero elements.

## Checked row-major indexing

The learner implemented a checked `at(indices)` boundary:

- the number of supplied indices must equal the tensor rank;
- every axis index must be strictly smaller than its corresponding extent;
- the flat offset is the dot product of indices and row-major strides.

For shape `[2,3,2]`, the implementation produced strides `[6,2,1]` and observed:

```text
[0,0,0] -> 1
[0,0,1] -> 2
[0,1,1] -> 4
[1,1,1] -> 10
```

The reverse stride loop also exposed an important unsigned-integer failure.
With `std::size_t i`, the condition `i >= 0` never becomes false. At `i == 0`,
`i - 1` wraps to the largest representable unsigned value and indexes before
the vector. ASan identified this as a heap-buffer-overflow. The safe loop keeps
`i > 0` as its invariant and writes position `i - 1`.

The corrected program compiles without warnings under `-Wall -Wextra
-Wpedantic -Wconversion -Wshadow` and runs cleanly with ASan and UBSan.

## Const and mutable element access

The learner separated access by object constness:

- mutable `Tensor::at(...)` returns `double&`;
- const `Tensor::at(...) const` returns `const double&`;
- both delegate validation and offset calculation to one const private helper.

`std::span` is passed by value because it is a lightweight pointer-and-length
view. This also permits convenient temporary spans created from compatible
contiguous index collections. Mutation through the returned reference was
observed to change the selected value from `10` to `42`, with strict and
sanitized configurations still clean.

## Exact next question

Observe generated copy and move behavior for the vector-owning value type.
Explicit runtime demonstrations of scalar access, rank mismatch, per-axis
bounds failure, and zero-sized indexing remain deferred retrieval debt.

The first move experiment incorrectly accessed the moved-from tensor without
reassignment and terminated because its observed rank was zero. The learner
chose to move on; safe post-move reassignment and independent-copy evidence
remain open.
