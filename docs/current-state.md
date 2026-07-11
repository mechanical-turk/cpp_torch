# Current Learning State

This file is the concise recovery point for a fresh session. Detailed material
belongs in the active milestone file.

## Governing plan

- Plan: [`docs/learning-plan.md`](learning-plan.md)
- Active phase: Phase 0 — Engineering baseline
- Active milestone: Milestone 0.4 — Compiler Warnings and Static Diagnostics
- Milestone file: [`docs/milestones/00-04-warnings-and-static-diagnostics.md`](milestones/00-04-warnings-and-static-diagnostics.md)
- Status: hands-on warning diagnostic ready to begin

## Current gate

Milestones 0.1 through 0.3 are complete. Apple Clang is available, while
command-line `clang-tidy` and `clang-format` are absent. Milestone 0.4 begins with
compiler warnings before adding external tooling.

Before implementation, run an adaptive diagnostic covering:

- translation units and the compilation pipeline;
- declarations, definitions, and the One Definition Rule;
- internal and external linkage;
- headers and public/private implementation boundaries;
- static and shared libraries;
- compiler versus linker responsibilities;
- CMake targets and usage requirements; and
- how `compile_commands.json` supports `clangd`.

## Completed work

- Established the dependency-ordered learning plan.
- Established persistent Codex instructions and progress-logging conventions.
- Chosen Milestone 0.1 as the next milestone.
- Began the Milestone 0.1 compilation/linking diagnostic.
- Completed a focused teaching detour on modern `inline` semantics.

## Evidence and demonstrated understanding

- Correctly explained textual header inclusion and separate compilation.
- Correctly predicted missing-symbol, missing-`main`, and successful link cases.
- Demonstrated why implementation files include their own public headers.
- Correctly reasoned about duplicate non-inline header definitions.
- After instruction, distinguished the `inline` keyword from optimization and
  identified build-time, visibility, and code-size tradeoffs.
- Distinguished a variable declaration from a variable definition in the basic
  namespace-scope case.
- Correctly predicted unresolved external references and duplicate external
  definitions.
- Correctly applied internal versus external linkage to both variables and
  functions.
- Correctly treated namespace-scope `static` and unnamed namespaces as ways to
  make functions translation-unit-local.
- Authored a working Ninja graph that separately compiles two translation units
  and links an executable.
- Diagnosed a missing final newline from Ninja's unexpected-EOF error.
- Correctly predicted and observed incremental rebuild propagation.
- Reproduced a stale build caused by missing header dependencies.
- Added Clang-generated GCC-style depfiles and verified Ninja's recorded header
  dependencies with `ninja -t deps`.
- Archived `math.o` into `libmath.a`, linked the consumer against it, and
  inspected archive membership.
- Confirmed with `nm -C` that the library object defines `add(int, int)` while
  the consumer object holds an unresolved reference before final linking.
- Defined the Milestone 0.1 implementation contract and mastery gate.
- Implemented and committed the minimal CMake library boundary with successful
  Debug and Release builds.
- Verified private-source (three-step) versus public-header (four-step)
  incremental rebuild propagation.
- Added `.clangd` pointing to `build/debug/compile_commands.json` and verified
  both translation units with direct `clangd --check` runs.
- Diagnosed deliberate compile-time type failure and link-time missing-symbol
  failure, then restored a clean green build.
- Completed the active mastery assessment with targeted correction and retrieval
  of translation-unit/object-file and CMake usage-requirement concepts.
- Passed Milestone 0.1 based on implementation, experiments, failure diagnosis,
  and live mastery evidence. A duplicative written retrospective was waived due
  to low marginal learning value.
- Established that testing concepts transfer from TypeScript/Python while C++
  framework and compiled-test workflow experience is new.
- Selected pinned GoogleTest v1.17.0 with CMake FetchContent and CTest discovery
  for the first production testing workflow.
- Integrated a compiled GoogleTest target, individual CTest discovery, structured
  failure diagnostics, and a verified `BUILD_TESTING=OFF` configuration.
- Added a narrow `.clang-format` rule after format-on-save collapsed short test
  bodies; command-line formatter installation remains deferred.
- Completed manual ASan/UBSan failures, an LLDB inspection, opt-in target-scoped
  sanitizer integration, and a real project-defect detection/restoration cycle.

## Open questions and review findings

- Revisit the distinction between static and shared-library update behavior.
- Later revisit namespace-scope `const` linkage; the topic was intentionally
  paused to establish the simpler model first.
- CMake syntax and generated behavior must now be learned through the real
  implementation rather than more abstract diagnostics.
- Compilation-database discovery should be retrieved again in later tooling
  work.
- Warning-group behavior and static-analysis experience have not yet been
  exercised.

## Active detours or branches

- Completed short diagnostic detour: modern `inline` and ODR semantics.

## Exact next action

Learner compiles one suspicious disposable program under progressively stronger
warning groups and explains the emitted diagnostics.

## Active learning artifacts

- [`docs/learning/phase-0/compilation-linking-and-inline.md`](learning/phase-0/compilation-linking-and-inline.md)
- [`docs/learning/phase-0/ninja-build-graph-lab.md`](learning/phase-0/ninja-build-graph-lab.md)
- [`docs/learning/phase-0/cpp-testing-workflow.md`](learning/phase-0/cpp-testing-workflow.md)
- [`docs/learning/phase-0/sanitizers-and-lldb.md`](learning/phase-0/sanitizers-and-lldb.md)

## Last updated

2026-07-10 — Compilation/linking diagnostic and `inline` detour recorded.
