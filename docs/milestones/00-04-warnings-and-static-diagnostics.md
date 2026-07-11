# Milestone 0.4 — Compiler Warnings and Static Diagnostics

## Motivation

Turn suspicious-but-valid C++ into early, actionable diagnostics and establish a
target-scoped warning policy. Then add static analysis that reasons beyond a
single compiler invocation.

## Dependencies and diagnostic

- Milestones 0.1–0.3 complete
- Apple Clang 21 available
- No command-line `clang-tidy` or `clang-format` currently on `PATH`
- Begin with compiler diagnostics; install/configure LLVM tooling only after the
  distinction is concrete

## Learning objectives

- Distinguish errors, warnings, undefined behavior, and suspicious valid code.
- Observe what `-Wall`, `-Wextra`, `-Wpedantic`, and focused warning groups add.
- Understand why `-Wall` does not mean every warning.
- Decide when warnings should become errors and when external/dependency code
  must be excluded from project policy.
- Package warnings as target-scoped CMake usage requirements without leaking them
  into GoogleTest.
- Install and run `clang-tidy` using `compile_commands.json`.
- Distinguish compiler warnings from AST-based static-analysis checks.
- Preserve a clean Debug, sanitized, and test workflow.

## Hands-on sequence

1. Compile a disposable suspicious program with progressively stronger warnings.
2. Explain each diagnostic and correct the underlying intent.
3. Add a project warning interface target and opt-in warnings-as-errors switch.
4. Verify project targets receive policy while fetched dependencies do not.
5. Install/configure command-line LLVM tooling.
6. Run focused `clang-tidy` checks through the compilation database.

## Acceptance criteria

- Learner predicts or explains diagnostics for assignment-in-condition, unused
  state, signed/unsigned comparison, conversion, and shadowing examples.
- Project targets compile under the selected warning policy without warnings.
- A temporary warning fails only the warnings-as-errors configuration and is
  restored.
- GoogleTest is not forced to satisfy project-owned warning policy.
- `clang-tidy` analyzes project translation units using the real compilation
  database.
- Final ordinary, sanitized, and test builds pass.

## Evidence, review, mastery, and retrospective

Pending implementation.

