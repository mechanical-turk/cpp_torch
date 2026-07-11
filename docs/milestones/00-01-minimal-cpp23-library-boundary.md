# Milestone 0.1 — Minimal C++23 Library Boundary

## Motivation

Build the smallest production-shaped C++23 library and consumer while retaining
a concrete mental model of the compilation, archive, dependency, and link steps
generated underneath it.

This milestone deliberately excludes testing, warnings policy, sanitizers,
formatting, static analysis, benchmarks, installation, and CI. Those are later
Phase 0 milestones so each tool is learned through a focused problem.

## Dependencies

- Basic C++ source/header familiarity
- Completed compilation/linking diagnostic
- Completed disposable handwritten Ninja build-graph lab

## Diagnostic findings

Demonstrated foundations:

- textual inclusion and translation units;
- declarations versus definitions;
- separate compilation and relocatable object files;
- defined and unresolved symbols;
- linker responsibility and common missing/duplicate-symbol failures;
- internal and external linkage;
- basic ODR behavior and modern `inline` semantics;
- static and shared library conceptual differences;
- incremental build-graph propagation;
- compiler-generated header dependency discovery; and
- basic CMake target and usage-requirement concepts.

Gaps are now best addressed through implementation rather than further abstract
questioning. ABI details, deep CMake mechanics, and advanced linkage cases are
explicitly deferred.

## Learning objectives

### C++ and systems

- Create a clean public declaration/private definition boundary.
- Explain which translation unit defines each external symbol.
- Distinguish source, object, static archive, and executable artifacts.
- Predict rebuild propagation after changes to a source or public header.
- Explain why consumers require public headers but not private sources.

### Tooling and engineering

- Express a library and consumer as CMake targets.
- Require C++23 at the target level.
- Publish the library's public include directory as a usage requirement.
- Keep private sources and include paths from propagating unnecessarily.
- Configure and build separate Debug and Release build trees with Ninja.
- Generate and locate `compile_commands.json` for `clangd`.
- inspect generated commands and artifacts sufficiently to connect CMake back to
  the handwritten Ninja model.

## Socratic sequence log

See:

- `docs/learning/phase-0/compilation-linking-and-inline.md`
- `docs/learning/phase-0/ninja-build-graph-lab.md`

## Hands-on investigations

Completed disposable lab:

- hand-authored Ninja compile, archive, and link edges;
- observed incremental rebuilds;
- reproduced missing header dependency tracking;
- added Clang depfiles and inspected Ninja's stored dependency graph;
- created and inspected a static archive; and
- inspected defined and undefined symbols with `nm -C`.

## Implementation contract

The learner will create:

```text
CMakeLists.txt
include/
└── cpp_torch/
    └── math.hpp
src/
└── math.cpp
examples/
└── basic_usage.cpp
```

The implementation must provide:

- a `cpp_torch` library target;
- a namespaced public function declared in the public header and defined in the
  private source;
- a `basic_usage` executable target that consumes the library through its public
  interface;
- a public include usage requirement owned by `cpp_torch`;
- target-level C++23 requirements; and
- no manually written compiler or linker command strings in CMake.

The function may remain mathematically trivial. This milestone evaluates the
library boundary and build model, not numerical sophistication.

## Acceptance criteria

### Build behavior

- Fresh Debug configuration and build succeed with Ninja.
- Fresh Release configuration and build succeed with Ninja.
- The consumer runs and produces its documented result in both configurations.
- `compile_commands.json` is generated and contains entries for both project
  translation units with a C++23 compilation mode.
- Touching/changing the private implementation rebuilds only the affected object
  and downstream archive/link steps.
- Changing the public header rebuilds both translation units and downstream
  steps.

### Boundary evidence

- The consumer includes only `<cpp_torch/math.hpp>` and does not add source-tree
  private include paths itself.
- The library contains one external definition for the public function.
- Generated build artifacts include distinct library and executable outputs.
- Symbol inspection shows the definition in the library object/archive and an
  unresolved reference in the consumer object before final linking.

### Mastery gate

The learner can, without consulting notes:

- draw the source-to-executable dependency graph;
- explain what CMake, Ninja, Clang, the assembler, archiver, and linker each do;
- explain `PRIVATE`, `PUBLIC`, and `INTERFACE` usage requirements at the level
  exercised here;
- diagnose one deliberately introduced compile failure and one link failure;
- predict incremental rebuild behavior before running it; and
- defend the chosen public/private file boundary.

## Correctness evidence

Pending implementation.

## Performance evidence

No optimization is required. The learner should distinguish Debug and Release
configuration intent, but detailed flags and benchmarking are deferred.

## Design decisions and rejected alternatives

- A trivial function is intentional: build mechanics remain isolated from tensor
  design.
- Handwritten Ninja was used only as a diagnostic lab. CMake will own the real
  project graph.
- Static versus shared selection need not be permanently fixed here; the
  generated default will be observed and explained.

## Review findings

Pending implementation.

## Mastery assessment

Pending implementation and evidence collection.

## Retrospective

Pending.

## Follow-up milestones and backlog

- Testing framework and test-design foundations
- Compiler warnings and diagnostics policy
- Sanitizers and LLDB
- Formatting and static analysis
- Benchmarking and profiling baseline
- GitHub Actions acceptance checks
- Installation and external consumer packaging

