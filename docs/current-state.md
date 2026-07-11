# Current Learning State

This file is the concise recovery point for a fresh session. Detailed material
belongs in the active milestone file.

## Governing plan

- Plan: [`docs/learning-plan.md`](learning-plan.md)
- Active phase: Phase 0 — Engineering baseline
- Active milestone: Milestone 0.1 — Minimal C++23 Library Boundary
- Milestone file: not yet created
- Status: prerequisite diagnostic in progress

## Current gate

Prerequisite diagnostic is in progress. Compilation, separate translation units,
object files, symbol resolution, the ODR, `inline`, and basic linkage have been
probed. Teaching pace was deliberately reduced to one distinction at a time.

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

## Open questions and review findings

- The prerequisite diagnostic must determine the milestone's exact learning
  objectives and detours.
- The milestone contract and acceptance criteria must be written after the
  diagnostic, not assumed in advance.
- Revisit the distinction between static and shared-library update behavior.
- Later revisit namespace-scope `const` linkage; the topic was intentionally
  paused to establish the simpler model first.
- Diagnose declarations/definitions and the ODR more deeply before creating the
  milestone contract.

## Active detours or branches

- Completed short diagnostic detour: modern `inline` and ODR semantics.

## Exact next action

Continue slowly from the established linkage model. Diagnose the difference
between a declaration and a definition for functions and variables, then move
to ODR requirements without introducing multiple new qualifiers at once.

## Active learning artifacts

- [`docs/learning/phase-0/compilation-linking-and-inline.md`](learning/phase-0/compilation-linking-and-inline.md)

## Last updated

2026-07-10 — Compilation/linking diagnostic and `inline` detour recorded.
