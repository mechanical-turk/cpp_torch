# Milestone 0.5 — Benchmarking and Profiling Baseline

## Motivation

Establish measurement discipline before performance-sensitive tensor and kernel
work. Learn how optimizers invalidate naive benchmarks, how to interpret noisy
timings, and how benchmarks differ from profilers and correctness tests.

## Dependencies and diagnostic

- Milestones 0.1–0.4 complete
- Google Benchmark v1.9.5 selected and pinned by release commit
- Begin with an isolated reduction loop rather than pretending trivial `add` is a
  meaningful performance target

## Learning objectives

- Distinguish correctness tests, microbenchmarks, macrobenchmarks, and profilers.
- Build and run benchmarks in an optimized configuration.
- Explain warm-up, repeated sampling, statistical variation, and environmental
  noise.
- Prevent dead-code elimination and invalid constant folding with benchmark
  barriers and runtime inputs.
- Report workload size and throughput alongside latency.
- Compare algorithms only under equivalent work and configuration.
- Use a macOS profiler to identify where time is spent rather than guessing.
- Keep benchmark dependencies and targets out of ordinary builds by default.

## Hands-on sequence

1. Write a local vector-sum benchmark with Google Benchmark.
2. Observe a naive benchmark vulnerable to optimization.
3. Add `DoNotOptimize`/appropriate barriers and runtime-sized inputs.
4. Run Release repetitions and export results.
5. Profile the benchmark process and identify the hot loop/library frames.
6. Record a reproducible baseline without optimizing the implementation yet.

## Implementation contract

- Add an opt-in `CPP_TORCH_BUILD_BENCHMARKS` CMake option.
- Embed pinned Google Benchmark v1.9.5 only when enabled.
- Disable Google Benchmark's own tests, GoogleTest tests, and install rules.
- Add a `cpp_torch_benchmarks` executable linked to
  `benchmark::benchmark_main`.
- Keep benchmark-only code outside the public library API.
- Build and run from a dedicated Release tree.

## Acceptance criteria

- Ordinary Debug configuration does not fetch/build the benchmark dependency.
- Release benchmark target builds and lists/runs registered cases.
- Benchmark results include repetitions and machine/context metadata.
- Learner explains why the measured work cannot be optimized away.
- One intentionally flawed benchmark demonstrates a misleading result.
- Profiler evidence identifies the actual hot path.
- Final tests remain passing and the benchmark baseline is recorded.

## Evidence, review, mastery, and retrospective

### Evidence

- Google Benchmark v1.9.5 is pinned by its exact release commit and enabled only
  through `CPP_TORCH_BUILD_BENCHMARKS`.
- Dependency tests and install rules are disabled when embedded.
- `cpp_torch_benchmarks` builds in a dedicated Release preset with `-O3` and
  `NDEBUG`, C++23, and project warnings.
- A complete `dev` compilation database includes library, example, tests, and
  benchmark sources for `clangd`, while actual measurements remain in the
  optimized benchmark tree.
- The valid reduction benchmark keeps allocation outside the timed loop, uses
  runtime-sized input, prevents result elimination, and reports processed items.
- Google Benchmark v1.9.5 deprecated the const-reference `DoNotOptimize`
  overload; changing the local result to non-const selected the supported barrier
  and restored warning-clean compilation.
- Three-repetition baseline:
  - 1,024 doubles: approximately 908 ns CPU and 1.128 billion items/second.
  - 1,048,576 doubles: approximately 1.009 ms CPU and 1.039 billion
    items/second.
  - observed CPU-time coefficient of variation below 0.2% in that run.
- An intentionally unobserved reduction reported `0.000 ns` for both sizes,
  including one million elements.
- Disassembly showed a load/`fadd` reduction loop in the valid benchmark and no
  reduction instructions between `StartKeepRunning` and `FinishKeepRunning` in
  the flawed benchmark.
- macOS `sample` collected 3,318 top-of-stack samples in
  `BM_VectorSum(benchmark::State&)` during a five-second profile of the large
  input. `std::accumulate` was inlined, consistent with the disassembly.
- A ten-second profiled run processed the large case at approximately 1.036
  billion items/second.

### Review and mastery

- A benchmark measures the optimized executable, not the apparent source text.
- Setup outside the state loop is excluded from the timed operation.
- `DoNotOptimize` makes the result observable to the optimizer; it is not a CPU
  timing instruction.
- Repetitions, mean, median, standard deviation, and coefficient of variation
  characterize sample stability but do not eliminate environmental bias.
- Wall time and CPU time answer different questions.
- Throughput requires explicit workload accounting.
- Near-linear scaling and stable throughput are consistent with an O(n)
  reduction but are not a proof of complexity or a full hardware diagnosis.
- A profiler attributes execution time; it does not replace controlled benchmark
  comparison. Assembly verifies what code was actually generated.

Milestone passed.

### Retrospective

The zero-nanosecond flawed benchmark was the critical observation: plausible
source code is not necessarily present in the executable. Measurement requires
an optimizer-aware harness, and performance claims require triangulation among
timings, generated code, and profiler evidence.

macOS could not provide Google Benchmark reliable frequency metadata or thread
affinity. Those warnings do not invalidate the timer readings, but they identify
environmental limitations and reinforce reporting variance rather than treating
one number as universal.

Hardware counters, Instruments Time Profiler, vectorization reports, cache
analysis, and cross-machine baselines are deferred until numerical kernels create
meaningful optimization questions.

