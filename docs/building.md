# Building cpp_torch

## Prerequisites

- CMake 3.26 or newer
- Ninja
- A C++23-capable compiler
- Git and network access during the first configuration, while pinned
  dependencies are fetched

Generated build trees live under `build/` and are intentionally ignored by Git.
Checked-in `CMakePresets.json` recreates them consistently.

List available presets:

```bash
cmake --list-presets
```

## Developer setup

Configure the complete developer tree used by `clangd`:

```bash
cmake --preset dev
cmake --build --preset dev
ctest --preset dev
```

This Debug tree contains library, example, test, and benchmark compilation
commands. `.clangd` reads `build/dev/compile_commands.json` so VS Code can resolve
all project translation units.

Do not use this Debug benchmark executable for performance conclusions.

## Focused configurations

Ordinary Debug development and tests:

```bash
cmake --preset debug
cmake --build --preset debug
ctest --preset debug
```

Warnings as errors:

```bash
cmake --preset strict
cmake --build --preset strict
ctest --preset strict
```

ASan and UBSan:

```bash
cmake --preset sanitized
cmake --build --preset sanitized
ctest --preset sanitized
```

Optimized library/example without tests:

```bash
cmake --preset release
cmake --build --preset release
```

Optimized benchmarks:

```bash
cmake --preset benchmark
cmake --build --preset benchmark
./build/benchmark/cpp_torch_benchmarks
```

Benchmark with repeated aggregate measurements:

```bash
./build/benchmark/cpp_torch_benchmarks \
  --benchmark_repetitions=5 \
  --benchmark_report_aggregates_only=true
```

Minimal Debug build without tests or benchmarks:

```bash
cmake --preset no-tests
cmake --build --preset no-tests
```

## Configuration roles

| Preset | Build type | Tests | Benchmarks | Special behavior |
|---|---|---:|---:|---|
| `dev` | Debug | yes | yes | Complete clangd database |
| `debug` | Debug | yes | no | Normal development |
| `strict` | Debug | yes | no | Warnings are errors |
| `sanitized` | Debug | yes | no | ASan and UBSan |
| `release` | Release | no | no | Optimized library/example |
| `benchmark` | Release | no | yes | Performance measurement |
| `no-tests` | Debug | no | no | Minimal dependency surface |

