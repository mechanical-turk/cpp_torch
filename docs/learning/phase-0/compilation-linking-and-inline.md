# Compilation, Linking, the ODR, and `inline`

## Milestone connection

- Phase 0 — Engineering baseline
- Milestone 0.1 — Minimal C++23 Library Boundary
- Status: prerequisite diagnostic in progress

## Demonstrated understanding

The learner independently demonstrated that:

- `#include` performs textual inclusion during preprocessing;
- `.cpp` files are compiled separately as translation units;
- a caller needs a declaration but not the definition during ordinary separate
  compilation;
- omitting the object that defines a referenced function causes link failure;
- the linker does not implicitly consume all object files in the working
  directory;
- inconsistent parameter types can compile independently and fail symbol
  resolution during linking;
- including the public header from the implementation checks the implementation
  against the same contract used by callers;
- multiple non-inline external definitions produced by a header normally violate
  the One Definition Rule; and
- `inline` does not guarantee optimization.

## Misconceptions discovered and corrected

### Object files versus executables

Initial model: an object file containing `main` was considered a complete,
runnable executable.

Correction: `.o` files are relocatable object files. They contain sections,
symbols, unresolved references, and relocation information. Linking supplies
layout, symbol resolution, runtime/startup dependencies, and executable-format
metadata. `main` is also not normally the operating system's literal entry
point; runtime startup code eventually calls it.

### `clangd` versus the compiler driver

Initial model: `clangd` was described as compiling the selected source files.

Correction: `clangd` is the editor language server. `clang++`, normally invoked
through the build system, drives preprocessing, compilation, assembly, and
linking.

### Header declarations do not locate object files

A declaration supplies the type contract needed to check a call and generate a
calling sequence. The resulting object contains a symbolic unresolved reference.
The linker matches that reference against definitions explicitly supplied in
objects or libraries; the declaration does not encode a path to an object file.

### Modern meaning of `inline`

Initial model: `inline` meant that the function body would necessarily replace
each call.

Correction: substitution is an optimization decision and is not guaranteed by
the keyword. The important language-level effect is permitting equivalent
definitions across translation units under the ODR. Compilers may inline
functions lacking the keyword and may retain calls to functions bearing it.

## Presented concepts

### Separate compilation model

For:

```cpp
// math.hpp
int add(int, int);
```

```cpp
// math.cpp
int add(int a, int b) { return a + b; }
```

```cpp
// main.cpp
int main() { return add(2, 3); }
```

compilation produces separate relocatable objects. The caller's object can refer
to an unresolved `add` symbol because it also carries relocation information.
The linker resolves the reference against the definition and produces the final
image.

### Header-defined functions and the ODR

A non-inline external definition included into multiple translation units
normally produces duplicate definitions. Include guards and `#pragma once`
prevent repeated inclusion only within one translation unit.

An inline definition may appear equivalently in multiple translation units:

```cpp
inline int add(int a, int b) {
    return a + b;
}
```

An inline declaration without a reachable definition is not the normal solution.
The definition must be reachable in each translation unit where the function is
odr-used.

### Header visibility tradeoffs

Visible bodies enable optimization chains such as constant propagation, common-
subexpression elimination, loop-invariant code motion, dead-code elimination,
branch simplification, and sometimes vectorization. The benefit is not limited
to avoiding call overhead.

Costs include repeated parsing and compilation, wider rebuild dependencies,
implementation exposure, and possible machine-code growth or instruction-cache
pressure.

Out-of-line `.cpp` definitions provide stronger implementation and dependency
boundaries. With an unchanged ABI, a shared-library implementation may be
updated without rebuilding consumers. Static-library consumers must be relinked
to incorporate updated object code, though their source need not be recompiled.

LTO may recover some cross-translation-unit optimization opportunities.

## Review prompts

Answer these later without consulting the notes:

1. Why can `main.cpp` compile a call without seeing the function definition?
2. What do symbols and relocations contribute to an object file?
3. Why does `#pragma once` not solve duplicate definitions across translation
   units?
4. What does `inline` guarantee, and what does it merely permit an optimizer to
   consider?
5. Why can inlining make runtime performance worse?
6. How do implementation-only changes differ for inline headers, static
   libraries, and shared libraries?
7. Why should an implementation `.cpp` include its own public header?

## Revision topics

- Retrieve the difference between an object file, executable, static archive,
  and shared library after those formats are studied hands-on.
- Revisit symbol mangling, especially the fact that parameter types generally
  distinguish overloads while return types generally do not.
- Inspect real object symbols and relocations using macOS command-line tools in
  Milestone 0.1.
- Re-test `inline` semantics after learning templates, `constexpr`, LTO, and ABI
  boundaries.

## Next diagnostic question

Continue from the basic linkage model into declaration/definition and ODR rules,
one distinction at a time.

## Linkage checkpoint

### Demonstrated

The learner now independently applies this basic model:

- `int x = 32;` at namespace scope is a definition with external linkage.
- Two such definitions in separate translation units normally cause a duplicate
  external-symbol failure at link time.
- `static int x = 32;` is a definition with internal linkage; separate
  translation units may each own a distinct `x`.
- `extern int x;` is a non-defining declaration that may refer to an external
  definition in another translation unit.
- An internal-linkage definition cannot fulfill another translation unit's
  external declaration.
- Ordinary namespace-scope functions have external linkage by default.
- Namespace-scope `static` functions and functions in unnamed namespaces are
  translation-unit-local.

### Important distinction

Two independent questions must be asked about a namespace-scope declaration:

1. Is it a definition—does it provide the entity or storage?
2. What linkage does the name have—can declarations in other translation units
   denote the same entity?

### Teaching calibration

The learner requested a slower pace after too many interacting cases were
introduced together. Continue with one new rule or qualifier at a time, confirm
the base model, and only then compose cases. `const` and inline variables remain
revision topics rather than current diagnostic material.
