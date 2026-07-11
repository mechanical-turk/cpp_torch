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

Pending implementation.

