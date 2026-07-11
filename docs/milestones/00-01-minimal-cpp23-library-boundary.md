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

- Debug and Release configure/build succeeded with Ninja.
- `basic_usage` produced the documented result (`5`) in both configurations.
- Both compilation databases contain the library and consumer translation units
  with the public include directory and C++23 mode.
- Direct `clangd --check` validation succeeded after repository configuration
  pointed at the Debug compilation database.
- A private-source change rebuilt the library object, archive, and final link
  while preserving the consumer object.
- A public-header change rebuilt both objects, the archive, and final link.
- Symbol inspection showed `cpp_torch::add(int, int)` defined in the library
  object/archive, unresolved in the consumer object, and resolved in the final
  executable.
- A deliberate incompatible call failed during consumer compilation with a
  precise type diagnostic.
- A deliberate wrong-arity implementation compiled as a distinct overload but
  failed linking because the requested two-argument symbol remained undefined.
- The final Debug build ran successfully and the worktree was clean.

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

- The first `CMakeLists.txt` copied schematic placeholders literally, creating a
  target named `TARGET`; this exposed that CMake command examples must be read as
  target construction, not shell-like templates.
- Initial editor redlines came from missing compilation-database discovery, not
  an invalid build graph.
- Generated Ninja and binary artifacts were initially committed in a WIP commit;
  `.gitignore` plus index removal corrected repository hygiene.
- Final-newline discipline was corrected in authored text files after the first
  Ninja parser failure made the issue observable.
- The first mastery explanation conflated a translation unit with an object
  file; this was corrected and successfully retrieved in the completed pipeline.
- `PUBLIC`/`PRIVATE` usage requirements initially lacked intuition and required
  a concrete A→B consumer example. The learner then correctly classified private
  implementation dependencies, public header dependencies, public language
  requirements, and the terminal consumer relationship.
- The compilation-database explanation remains less fluent than the core build
  graph and should be retrieved again in a later milestone.

## Mastery assessment

Implementation behavior and primary build-system concepts have been
demonstrated. The learner can:

- distinguish the roles of CMake and Ninja;
- complete the preprocessing/compilation/assembly/archive/link pipeline;
- explain defined versus unresolved library/consumer symbols;
- classify concrete `PRIVATE` and `PUBLIC` requirements;
- explain public header versus private implementation rebuild consequences; and
- diagnose compile-time type failure versus link-time missing definition.

Final completion awaits a short learner-authored retrospective. Compilation-
database discovery should be scheduled for later retrieval rather than blocking
the milestone, because the practical configuration is verified and the gap is
terminological rather than architectural.

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
