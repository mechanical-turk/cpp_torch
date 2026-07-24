# Detour — C++20 Named Modules from First Principles

## Outcome

Closed and abandoned on 2026-07-23. All module experiment source code was
deleted at the learner's request.

The detour established the BMI/object/import pipeline and produced a behaviorally
equivalent single-file `Value` module, but the manual build, editor, and module
unit mechanics imposed more friction than their current learning value justified.
The learner chose to return to autograd and prioritize progress toward tensors.

This is a deferral, not a project-wide rejection of modules. Revisit only when
the compiler/build/editor ecosystem is itself the learning objective or when a
real project boundary creates enough benefit to justify the tooling cost.

## Motivation

The traditional header/source extraction of the scalar `Value` engine made a
reusable compilation boundary substantially harder to read than its standalone
definition. Investigate whether standard named modules improve that boundary,
while learning the compiler and build-system machinery they require.

## Scope and dependency

This is a bounded detour from Milestone 1.2. The extracted header/source scalar
engine remains the behavioral and organizational baseline. The detour does not
authorize migrating `cpp_torch` to modules before evidence is collected.

## Learning objectives

- Distinguish module interfaces, implementation units, imports, BMIs, object
  files, and final linking.
- Explain what modules replace in the textual-header model and what they do not.
- Build a minimal named module manually with Clang before using build automation.
- Compare readability, dependency ordering, incremental rebuilds, editor support,
  diagnostics, and distribution constraints against the header/source baseline.
- Evaluate CMake 3.28+ module support against the repository's installed CMake
  3.26.4 rather than treating language support as sufficient tooling support.

## Hands-on sequence

1. Run an adaptive diagnostic on the expected compile/link pipeline.
2. Build and import a minimal arithmetic module manually.
3. Inspect generated BMI and object artifacts and provoke ordering failures.
4. Express the scalar `Value` boundary as a named-module experiment.
5. Try supported CMake module integration with an appropriate CMake version.
6. Compare both boundaries and record a keep/defer/migrate decision.

## Acceptance criteria

- The learner can explain and manually execute the module build pipeline.
- Import dependencies rebuild predictably and observed artifacts are understood.
- The module version preserves the scalar engine's behavior.
- Tooling and portability limitations are demonstrated, not assumed.
- A written evidence-based decision determines whether the main project adopts,
  defers, or limits module use.

## Initial gate

Predict which artifacts must exist before a translation unit importing a named
module can be compiled and linked.

## Manual Clang pipeline evidence

The learner authored a primary module interface exporting `add(int, int)` and an
importing program. Apple Clang 21 rejected otherwise-valid module syntax until
the toolchain-specific `-fcxx-modules` flag was supplied; `-fmodules` enabled the
older Clang module system and did not fix the standard named-module compile.

The successful explicit pipeline was:

```text
math.cppm --precompile--> math.pcm
main.cpp + math.pcm -----> main.o
math.pcm ----------------> math.o
main.o + math.o ---------> app
```

Observed evidence:

- `math.pcm` was approximately 25 KiB and identified only as opaque `data` by
  the platform `file` utility.
- Compiling the importer without a BMI search path failed with `module 'math'
  not found`.
- `main.o` contained an undefined `add@math(int, int)` symbol.
- `math.o` defined the exact same module-owned symbol.
- Linking both objects produced an executable that printed `5`.

The learner corrected the initial misconception that the BMI satisfies the
linker: the PCM supplies compiler-visible interface information, while the
object file supplies machine code to the linker.

Editor diagnostics remain intentionally unresolved. The experiment is absent
from `build/dev/compile_commands.json`, so clangd has neither `-fcxx-modules` nor
the BMI mapping needed to parse the importer. This is retained as tooling-cost
evidence for the later comparison.

## Exact next gate

Build the scalar `Value` engine as a single-file named module interface and
compare its readability directly against the extracted header/source baseline.

The separate module-implementation-unit pipeline was introduced and its missing
BMI failure reproduced, but further arithmetic-module mechanics were stopped at
the learner's request because they had become repetitive. The remaining details
are deferred until the `Value` module creates a concrete need for them.

## Single-file `Value` module evidence

The learner authored `cpp_torch.autograd` as one primary module interface unit.
A global module fragment includes the required standard headers; operation tags,
nodes, and traversal machinery remain non-exported; the complete `Value` class is
co-located and exported. The importer contains no textual project header and uses
`import cpp_torch.autograd;`.

Two module-specific diagnostics were resolved:

- A valid module may precompile while exporting no API; the `Value` namespace
  initially lacked `export`.
- `import "cpp_torch.autograd";` requests a header unit, not a named module. The
  named-module import must not use quotes.

Apple Clang successfully produced the PCM, compiled it to `value.o`, compiled the
importer against the prebuilt-module path, linked both objects, and reproduced
the exact loss and gradients from the header/source implementation across two
cleared backward passes.

## Exact next gate

Compare the single-file module against the header/source baseline on readability,
implementation hiding, rebuild isolation, build complexity, and editor support;
then decide whether modules should be adopted, limited to experiments, or deferred.
