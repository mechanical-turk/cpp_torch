# Benchmarking and Profiling Baseline

## Milestone connection

- Phase 0 — Engineering baseline
- Milestone 0.5 — Benchmarking and Profiling Baseline
- Status: passed

## Measurement stack

```text
correctness tests
    establish expected behavior

microbenchmark
    measures a controlled operation repeatedly

generated assembly
    proves which optimized instructions remain

profiler
    samples where a running process spends time
```

Each supplies different evidence.

## Valid benchmark structure

```text
runtime size from benchmark argument
    ↓
vector allocation and initialization outside timer loop
    ↓
framework-controlled repeated timed loop
    ↓
std::accumulate reduction
    ↓
DoNotOptimize(result)
    ↓
items-processed accounting for throughput
```

The framework chooses sufficient internal iterations for a measurable run.
Requested repetitions produce independent samples whose aggregate rows report
mean, median, standard deviation, and coefficient of variation.

## Optimizer-elimination experiment

The valid benchmark measured roughly one billion doubles per second for both
1,024 and 1,048,576-element inputs. A source-identical reduction whose result was
discarded measured `0.000 ns`.

Disassembly explained the result:

- valid function: repeated load and floating-point add instructions;
- unobserved function: setup followed by `StartKeepRunning` and immediately
  `FinishKeepRunning`, with no reduction loop.

The lesson is not merely "always call `DoNotOptimize`." The broader rule is to
verify that the optimized executable performs the work claimed by the benchmark.

## Profiler evidence

macOS `sample` observed the large valid case for five seconds at one-millisecond
intervals. 3,318 collapsed top-of-stack samples landed in
`BM_VectorSum(benchmark::State&)`. The standard reduction was inlined, so it did
not appear as a separate call frame; assembly located the actual hot loop.

## Reproducible configurations

- `dev`: complete Debug compilation database for editor syntax only.
- `benchmark`: Release measurement executable.

The Debug benchmark target must not be used for performance conclusions.
Checked-in CMake presets recreate ignored build trees for fresh clones.

## Retrieval topics

- Why can a benchmark report zero time for apparently substantial source code?
- What exactly does `DoNotOptimize` protect?
- Why is allocation outside the timed loop?
- How do wall time, CPU time, throughput, standard deviation, and CV differ?
- Why do profiler and assembly evidence complement benchmark timing?

