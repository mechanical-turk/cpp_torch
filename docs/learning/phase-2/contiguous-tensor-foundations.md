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

The focused GoogleTest representation contract was also deferred in favor of
beginning tensor arithmetic. Manual strict and sanitizer evidence exists, but
the representation milestone cannot be marked complete until its automated
contract and skipped edge cases are revisited.

## First elementwise operation

The learner implemented equal-shape `Tensor::operator+` as a const operation
returning independently owned output. The design discussion established:

- a member binary operator is valid for `Tensor + Tensor`;
- a non-member becomes more useful when symmetric conversions or
  `scalar + Tensor` enter the API;
- constructor sink parameters accepted by value avoid repeated overloads;
- completed local shape/storage vectors should be moved into those parameters,
  eliminating a second deep copy while retaining cheap vector moves.

The known first output value was observed as `3` for `[2,3] + [1,4]` under
normal and ASan/UBSan builds. Full operation coverage remains part of the
deferred tensor test debt.

Elementwise multiplication was then implemented with the same ownership and
shape contract. After correcting operation-specific validation terminology and
actually exercising every output element, strict and sanitized builds observed:

```text
[2,3] + [1,4] = [3,7]
[2,3] * [1,4] = [2,12]
```

The two concrete implementations now provide evidence for analyzing a shared
internal elementwise traversal rather than abstracting from only one example.

The learner identified the varying part as a scalar
`(double,double) -> double` callable and chose a private member helper so it can
access both tensors' private storage directly. This is legal because class
members may access private fields on every instance of their class, not only
`this`. Addition and multiplication now pass lambdas into an abbreviated
function template while sharing validation, allocation, traversal, and result
construction.

The learner then established why this template may remain defined in
`tensor.cpp`: only the non-template operator bodies in that translation unit
instantiate it, and the full definition is visible there. If those callers were
moved into the public header while the helper definition remained hidden, a
consumer could not instantiate the required lambda specialization.

## Full reduction semantics

The learner chose a rank-0 `Tensor` rather than `double` as the result of a
full-tensor sum, preserving tensor composition and future autograd tracking.
The sum of empty storage was identified as `0`, the additive identity, with
scalar shape `[]` rather than singleton-vector shape `[1]`.

The first example supplied one index to the rank-0 result and terminated. Codex
later corrected the mechanical example while verifying dot composition; empty
reduction remains validation debt.

## Dot-product composition

The learner implemented rank-1 dot product as:

```text
dot(left,right) = sum(left * right)
```

This made the distinction between unambiguous vector dot product and
higher-rank axis contraction explicit. For `[2,3]` and `[1,4]`, strict and
sanitized builds produced a rank-0 tensor containing `14`.

## Automated contract closure

Codex added the routine GoogleTest harness under the standing example/harness
ownership rule. Seven tensor tests now cover metadata, checked access and
mutation, constructor/index failures, scalar/singleton/empty distinctions,
empty reduction, copy/move behavior, reference arithmetic, and invalid
operands. All 15 repository tests pass under warnings-as-errors and ASan/UBSan.

This closes mechanical validation debt only. The learner must still retrieve and
defend the ownership and representation model before Milestone 2.1 passes.

## Mastery retrieval

The learner subsequently retrieved the ownership, scalar/empty, overflow,
row-major indexing, and constructor-invariant models. Two corrections were
needed and accepted:

- destruction, as well as reassignment, is guaranteed for a moved-from tensor;
- scalar shape `[]` is not an exception to the shape-product/storage-size
  invariant because the empty product is one.

The learner also identified the current performance limitation that every
`at()` call reconstructs and allocates the row-major stride vector. Milestone
2.1 is complete; this observation motivates stored layout metadata in Phase 3.
