# Matrix Multiplication Foundations

## Milestone connection

- Phase 4 — Tensor operations and numerical kernels
- Milestone 4.1 — Matrix Multiplication Reference Kernel
- Status: implementation gate passed; mastery review active

## Mathematical definition

For rank-two operands:

```text
A shape = [m,k]
B shape = [k,n]
C shape = [m,n]
```

Each output value is a row/column dot product:

\[
C_{ij}=\sum_{r=0}^{k-1} A_{ir}B_{rj}.
\]

The learner first wrote the expanded products, then learned the term reduction
index: the inner index is iterated and summed away, so it does not appear in the
output shape.

The inner dimensions must match because a row of `A` and a column of `B` must
have equal length. A zero-length inner dimension is valid; each output is an
empty sum and therefore zero.

## Reference kernel

The learner implemented a public rank-two `Tensor::matmul()` with `i → j → k`
loop nesting. Inputs are read through logical `at()` access, so contiguous and
non-contiguous views use the same correctness path. Output is newly allocated
contiguous row-major storage.

Review caught and corrected:

- accidental placement of the public operation under `private:`;
- use of the reduction width as the output row width;
- a failed correction that swapped loop bounds while retaining the original
  meanings of `i` and `j`; and
- output-size multiplication occurring before overflow validation.

The final output index is `i * n + j`. The inline overflow guard checks `m*n`
before allocation. Zero rows, columns, and reduction width are handled by the
ordinary loop bounds without special control flow.

## Correctness evidence

Mechanical tests cover:

- a known rectangular `[2,3] × [3,4]` result;
- two non-contiguous transpose-view inputs;
- zero reduction width producing a non-empty zero matrix;
- zero output rows and columns;
- invalid ranks and incompatible inner dimensions; and
- a constructible zero-input case whose output shape would overflow.

All 28 tests pass under strict warnings and ASan/UBSan.

## Revision topics

- Distinguish output width `n` from reduction width `k`.
- Explain why empty dot products equal zero.
- Retrieve why output-size overflow must be checked before constructing the
  vector.
- Derive arithmetic complexity and the physical access sequence of the
  `i → j → k` loop for contiguous operands.

## Outcome

The reference kernel has `m*n` outputs and performs `k` multiply-accumulate
steps per output, giving `O(mkn)` time and `O(mn)` newly allocated output
storage. The learner chose not to spend additional time on a standalone
complexity quiz. Matrix-specific profiling and optimization remain deferred;
the verified reference kernel is sufficient to unlock the next model-building
dependency.

Milestone 4.1 passed.
