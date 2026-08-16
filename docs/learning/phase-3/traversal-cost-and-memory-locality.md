# Traversal Cost and Memory Locality

## Milestone connection

- Phase 3 — Memory, architecture, and general tensor layouts
- Milestone 3.2 — Tensor Traversal Cost and Memory Locality
- Status: prerequisite diagnostic complete; controlled benchmark design next

## Cache-line utilization

The learner initially predicted sequential traversal would be faster because
values could enter registers more efficiently. The refined model separates
register use from cache-line movement: both patterns ultimately load useful
values into registers, but memory is transferred through caches in fixed-size
lines.

Under the teaching model of 64-byte cache lines and 8-byte doubles, one line
contains eight consecutive doubles:

- sequential traversal can use all eight values, giving 100% line utilization;
- stride-16 traversal uses one value from each fetched line, giving 12.5%
  utilization.

The strided loop therefore transfers roughly eight times as many bytes per
useful value in the simplified model. It does not load only one double; it
fetches a complete line and ignores seven neighboring doubles.

## Prefetching, latency, and bandwidth

Hardware prefetching may recognize predictable access and request future lines
early. The learner correctly explained that this does not compact scattered
values: the transfer granularity remains a cache line. Prefetching can hide
latency but cannot remove wasted traffic.

Two distinct costs were established:

- latency is the delay before requested data arrives;
- bandwidth is the maximum transfer rate.

A bandwidth-bound sum is limited by value delivery rather than addition
throughput. Making arithmetic faster does not help when the arithmetic units
are waiting for operands.

## Hierarchy and reuse

The working model is:

```text
registers → L1 → L2 → shared cache → main memory
```

Data already resident in L1 removes main-memory latency and bandwidth from the
timed path, but the loop can still be limited by L1 load bandwidth, arithmetic,
dependency chains, or indexing/control overhead. Bandwidth-bound claims should
name the relevant hierarchy level.

Temporal locality means reusing an address while its line remains in a nearby
cache. Repeated benchmark iterations over a small tensor therefore tend to
measure warm-cache behavior. The learner briefly suggested a cache line might
remain in a register; this was corrected: registers retain selected scalar or
vector values, while cache-line residency belongs to cache levels.

## Next experiment-design question

Design a comparison between contiguous and transposed traversal that keeps
tensor values, operation count, and arithmetic constant while excluding view
construction and unrelated allocation from the timed region as far as the
current public API permits.

## Initial measurement and causal limits

At 1024-by-1024, the contiguous `Tensor::sum()` median was approximately
2.55 ms and transpose-view sum approximately 4.38 ms, a 1.72x ratio. The
learner first treated layout as sufficient proof of cache causation. The refined
conclusion is narrower: the controlled metadata/access-order change causes the
observed performance difference, but the measurement does not decompose cache,
prefetch, TLB, address-generation, compiler, and noise contributions.

The next experiment removes Tensor-specific machinery. Raw contiguous and
transpose traversals share the same coordinate-advance and physical-index code,
differing only in strides. If the transpose remains slower, Tensor abstraction
cannot be the sole explanation and physical access order becomes a stronger
mechanistic hypothesis.

At 1024-by-1024, the raw-vector experiment measured approximately 1.00 ms
contiguous and 1.56 ms transposed. The corresponding Tensor medians in the same
run were approximately 2.58 ms and 4.47 ms. Thus:

- layout/access order remains costly without the Tensor abstraction;
- the current Tensor reference path adds substantial overhead in both layouts;
- the raw experiment strengthens but does not uniquely prove a cache-miss
  mechanism.

## Working-set sweep

The learner challenged the role of temporal locality because every scalar is
summed once. The correction operates at cache-line granularity: a transposed
traversal consumes different scalars from the same line at widely separated
times. A small working set can retain that partially consumed line; a large
working set may evict it before the remaining scalars are used.

Measured transpose/base median ratios stayed approximately 1.0 for 2 KiB,
32 KiB, and 512 KiB square allocations. They rose to approximately 1.35
(Tensor) and 1.24 (raw) at 8 MiB, then 4.04 (Tensor) and 2.09 (raw) at 32 MiB.
The curve matches the predicted working-set/reuse-distance effect and is
stronger evidence for hierarchy-sensitive locality than a single benchmark
size.

## Deferred profiling branch

Elapsed time cannot identify the exact mechanism because allocation size,
physical stride, cache-line reuse distance, page count, TLB pressure, and
prefetch behavior all change with the square side. Hardware counters or more
independently controlled experiments would be required to attribute transitions
to particular cache levels or mechanisms.

The learner chose to stop profiling here so the project can progress toward
trainable models. This does not weaken the performance objective: the benchmark
and questions are preserved for a later kernel-optimization branch, when
profiling evidence will act on more representative operations such as matrix
multiplication.

Milestone 3.2 passed without adding a fast path.
