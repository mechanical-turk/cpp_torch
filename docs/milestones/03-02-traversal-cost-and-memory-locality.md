# Milestone 3.2 — Tensor Traversal Cost and Memory Locality

## Motivation

Milestone 3.1 made arbitrary layouts correct but left performance reasoning at
the level of intuition. This milestone builds the systems model needed to
explain and measure why contiguous, strided, and permuted traversals behave
differently even when they perform the same arithmetic.

## Dependencies

- Milestone 3.1 — Stored Strides, Offsets, and Views
- Phase 0 benchmarking and profiling workflow

## Learning objectives

- Separate algorithmic work from memory-access cost.
- Explain cache lines, spatial locality, temporal locality, and hardware
  prefetching at the depth needed for CPU tensor kernels.
- Predict physical access sequences from shape/stride/offset metadata.
- Measure direct contiguous traversal against general logical-coordinate
  traversal and non-contiguous views.
- Identify the costs of checked indexing, coordinate odometers, and allocation.
- Design fast paths only after correctness-preserving reference behavior and
  measurements exist.

## Initial orientation

The unit connects the layout metadata just implemented to actual CPU behavior.
Its hands-on artifact will be a focused benchmark and profiler experiment over
equivalent contiguous and non-contiguous tensor traversals. It will not yet add
broadcasting, SIMD, tiling, BLAS, or general kernel optimization.

Skipping this unit would allow fast paths to be added mechanically but would
leave the learner unable to explain their benefit, recognize memory-bound
behavior, or evaluate future matrix-multiplication designs.

## Initial diagnostic

Compare summing the same number of `double` values through physical index
sequences `0,1,2,...` and `0,k,2k,...`. Predict which machine-level effects can
make their runtimes differ even though both perform one addition per value.

## Planned evidence

- Learner predictions recorded before measurement.
- A benchmark that prevents optimizer elimination and reports stable
  distributions.
- At least one controlled comparison separating traversal bookkeeping from
  memory-layout effects.
- Assembly or profiler evidence when it materially resolves an observed cost.

## Diagnostic evidence

- Predicted sequential traversal would outperform stride-16 traversal.
- Refined the initial register-focused explanation into cache-line utilization:
  100% versus 12.5% under a 64-byte-line/eight-byte-double model.
- Explained why prefetching may hide latency but cannot eliminate transferred
  bytes or poor line utilization.
- Distinguished latency from bandwidth and identified data delivery as the
  limiter in a bandwidth-bound sum.
- Distinguished main-memory costs from L1 bandwidth, arithmetic, and loop
  overhead when data is already cached.
- Explained warm-cache temporal reuse, correcting the idea that complete cache
  lines remain in registers.

## First benchmark evidence

A controlled 1024-by-1024 Release benchmark constructed the base tensor and
transpose view outside timing, called the same `sum()` path, and observed the
scalar result with `benchmark::DoNotOptimize`.

Across five repetitions:

```text
contiguous median: approximately 2.55 ms
transpose median:  approximately 4.38 ms
ratio:             approximately 1.72x
```

Contiguous CV was approximately 0.29%; transpose CV was approximately 8.26%.
The environment could not pin thread affinity, so the transpose result is
notably noisy. The result supports a layout/access-order cost on this machine;
it does not by itself attribute the entire difference to cache misses.

Two raw-vector cases now use one shared shape/stride traversal function to
compare contiguous and transposed physical order without Tensor access,
ownership, or scalar-result construction. They compile cleanly but have not yet
been measured. The learner changed the benchmark side to 16384, making each
allocation about 2 GiB; that scale must be confirmed before execution.

The experimental size was restored to 1024 after confirming 16384 was temporary
exploration. Five-repetition medians were:

```text
Tensor contiguous:  approximately 2.58 ms
Tensor transpose:   approximately 4.47 ms  (1.73x)
raw contiguous:     approximately 1.00 ms
raw transpose:      approximately 1.56 ms  (1.56x)
```

The raw comparison preserves a substantial layout penalty after removing
Tensor-specific checked access, ownership, and scalar-result construction. This
rules out Tensor abstraction as the sole cause and strengthens physical access
order as the causal input. It still does not decompose cache, prefetch, TLB,
address generation, or compiler effects.

## Working-set size sweep

The learner predicted that a small transposed allocation can retain partially
consumed lines nearby, while larger reuse distances and working sets increase
eviction pressure. Parameterized square benchmarks produced these median wall
time ratios:

```text
side   allocation   Tensor transpose/base   raw transpose/base
16       2 KiB              0.99x                  1.00x
64      32 KiB              0.98x                  1.00x
256    512 KiB              1.01x                  1.02x
1024     8 MiB              1.35x                  1.24x
2048    32 MiB              4.04x                  2.09x
```

The near-unity small-working-set ratios and sharp large-working-set penalties
match the qualitative cache-capacity/reuse-distance prediction. This is stronger
causal-pattern evidence than one size but still does not identify exact cache
boundaries or uniquely separate cache, TLB, prefetch, and compiler mechanisms.

## Gate

The learner must explain observed performance using access patterns and the
memory hierarchy, distinguish reference-path overhead from layout-induced
locality costs, and justify any fast path with reproducible evidence.

## Outcome and retrospective

The learner:

- explained sequential versus strided cache-line utilization;
- distinguished prefetch latency hiding from bandwidth demand;
- reasoned about cache-line reuse rather than incorrectly requiring scalar
  reuse;
- predicted that transpose penalties would grow with working set and eviction
  pressure;
- interpreted the raw-vector comparison as ruling out Tensor machinery as the
  sole cause;
- distinguished the measured access-order effect from an unproven specific
  cache-level mechanism; and
- corrected the interpretation of the size sweep from absolute `N²` runtime
  growth to a changing transpose/base ratio.

No fast path was added. The current general traversal remains the correctness
reference. Hardware-counter profiling, exact cache-level attribution, assembly
analysis, and contiguous fast paths are deferred to a future evidence-driven
optimization branch.

Milestone 3.2 passed on 2026-07-25.
