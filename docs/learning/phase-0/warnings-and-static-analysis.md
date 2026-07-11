# Compiler Warnings and Static Analysis

## Milestone connection

- Phase 0 — Engineering baseline
- Milestone 0.4 — Compiler Warnings and Static Diagnostics
- Status: passed

## Diagnostic layers

```text
compiler errors
    reject invalid translation units

compiler warnings
    flag suspicious valid code during compilation

clang-tidy
    runs selected AST/dataflow-oriented checks with compilation context

sanitizers
    detect instrumented violations on executed runtime paths
```

No layer subsumes all others.

## Warning experiment

The same valid source produced:

| Policy | Findings |
|---|---|
| compiler defaults | none |
| `-Wall -Wextra -Wpedantic` | unused variable, signed/unsigned comparison |
| plus `-Wconversion -Wshadow` | float-to-int conversion, shadowing, previous findings |

An assignment used as an `if` condition was diagnosed with two intent-sensitive
alternatives: add explicit parentheses if assignment is intentional, or use
`==` if comparison was intended.

`-Wall` is a curated warning group rather than a literal request for every
warning. `-Weverything` was also observed to emit platform/toolchain noise,
including a poisoned system-directory diagnostic, illustrating why production
policies select and maintain warning groups.

## Target-scoped CMake model

`cpp_torch_warnings` is an interface target that emits no file. It packages
compiler-specific compile requirements. Project-owned targets link it privately,
so warnings apply to library, example, and test code but do not propagate into
consumers or fetched GoogleTest sources.

Generator expressions select flags by compiler identity. Warnings-as-errors is a
separate option rather than an unconditional property.

## Static analysis and formatting

Homebrew LLVM provides command-line `clang-tidy` and `clang-format` under its
keg-only prefix. `clang-tidy` reads the generated compilation database and a root
configuration enabling analyzer, bug-prone, and performance checks. Project
header filtering prevents third-party diagnostics from becoming owned findings.

The root formatter policy forbids single-line short functions. VS Code inserts a
final newline on save, and command-line formatting can be verified independently
of the editor.

## Retrieval topics

- Why does `-Wall` not mean all warnings?
- Why should warning policy avoid propagating to consumers and dependencies?
- What does an interface target contribute if it produces no artifact?
- How do compiler warnings, clang-tidy, and sanitizers differ?
- Why does static analysis require the compilation database?

