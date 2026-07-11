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

### Evidence

- A disposable program compiled silently with default warnings.
- `-Wall -Wextra -Wpedantic` surfaced unused state and signed/unsigned
  comparison.
- `-Wconversion -Wshadow` additionally surfaced float-to-int narrowing and local
  shadowing.
- Assignment in a condition produced `-Wparentheses` diagnostics with distinct
  suggestions for intentional assignment versus intended equality.
- A target-scoped `cpp_torch_warnings` interface target packages Clang/GCC and
  MSVC-specific warning policies through generator expressions.
- A separate `CPP_TORCH_WARNINGS_AS_ERRORS` option adds `-Werror`/`/WX` only when
  requested.
- Strict compilation commands contained the full warning policy for the library,
  example, and test source, while GoogleTest's own sources did not.
- Strict build and CTest passed.
- Homebrew LLVM 20.1.3 was found already installed outside the shell `PATH`.
- Root `.clang-tidy` checks enabled analyzer, bug-prone, and performance families
  with project-header filtering.
- Focused static analysis identified assignment-in-condition and narrowing as
  bug-prone patterns in the disposable source.
- Project translation units produced no surfaced clang-tidy findings.
- Command-line clang-format validation exposed pre-existing short functions;
  the project configuration reformatted them into the desired multiline style.
- VS Code workspace configuration now inserts a final newline on save.

### Review and mastery

- Compiler acceptance, warning policy, sanitizer detection, and static analysis
  are distinct layers with overlapping but non-identical findings.
- `-Wall` is a curated set, not every available warning.
- Focused warning groups increase coverage but also require conscious noise and
  portability management.
- Warnings-as-errors is opt-in so strict/CI workflows can enforce it without
  making every exploratory build brittle.
- Warning requirements are private to project-owned targets and must not leak
  into consumers or third-party dependency compilation.
- CMake interface targets can package non-artifact usage requirements such as
  warning flags.
- `clang-tidy` relies on the real compilation database for accurate language,
  macro, and include context.

Apple `clangd --check` reported an internal Extract Function tweak conflict on
the GoogleTest macro expansion. This was not a compile, test, or clang-tidy
failure; direct strict build and analysis remained clean.

Milestone passed.

### Retrospective

The disposable source showed why a production warning policy must be empirical:
valid code compiled silently by default, increasingly focused groups exposed
different risks, and `-Weverything` produced unrelated platform noise. The final
policy is intentionally strong but scoped to code owned by this project.

More opinionated readability, modernization, include-cleanliness, and naming
checks are deferred until the codebase contains enough real design to evaluate
their signal-to-noise ratio.

