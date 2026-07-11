# Ninja Build Graph Lab

## Milestone connection

- Phase 0 — Engineering baseline
- Milestone 0.1 — Minimal C++23 Library Boundary
- Artifact: disposable hands-on diagnostic

## Learner-authored experiment

The learner created `experiments/phase-0/ninja-basics/` with:

- a public declaration in `math.hpp`;
- a definition in `math.cpp`;
- a calling program in `main.cpp`; and
- a handwritten `build.ninja` with separate compile and link rules.

The graph currently models:

```text
math.cpp ──compile──> math.o ──┐
                              ├──link──> app
main.cpp ──compile──> main.o ──┘
```

Clang-generated dependency information extends the graph so both object files
also depend on `math.hpp`.

## Observations and demonstrated understanding

### Ninja syntax and parsing

The initial graph used correct build-edge semantics but failed with:

```text
build.ninja:9: unexpected EOF
```

The learner inferred that the file ending was relevant. Adding the missing final
newline corrected the parse error.

### Object and executable formats

The successful build produced:

- `math.o`: Mach-O 64-bit ARM64 object;
- `main.o`: Mach-O 64-bit ARM64 object; and
- `app`: Mach-O 64-bit ARM64 executable.

The executable printed `5`.

### Incremental dependency propagation

With no changes, Ninja reported `no work to do`.

After `math.cpp` was touched, the learner predicted and observed:

1. rebuild `math.o`;
2. preserve `main.o`; and
3. relink `app` because it depends on the changed `math.o`.

### Reproduced stale-build defect

The first graph did not mention `math.hpp`. Touching the header therefore caused
Ninja to report `no work to do`, despite both translation units including it.
This demonstrated that Ninja follows its declared/discovered graph and does not
parse C++ includes itself.

Manually adding `math.hpp` as an implicit input to both compile edges correctly
rebuilt both objects and relinked the executable.

### Compiler-generated dependency discovery

The manual header edges were replaced with:

```ninja
rule compile
  command = clang++ -std=c++23 -MMD -MF $out.d -c $in -o $out
  depfile = $out.d
  deps = gcc
```

Here:

- `-MMD -MF $out.d` instructs Clang to write discovered user-header
  dependencies;
- `depfile = $out.d` tells Ninja where to read them; and
- `deps = gcc` selects the GCC/Make-compatible depfile format supported by
  Clang; it does not cause GCC to be invoked.

Ninja consumes the transient depfiles and stores dependency data in
`.ninja_deps`. Inspection with `ninja -t deps` showed that both objects depend on
their source file and `math.hpp`.

## Review prompts

1. Why did changing `math.cpp` rebuild `math.o` and `app`, but not `main.o`?
2. Why did changing `math.hpp` initially rebuild nothing?
3. Why should Ninja rely on compiler-generated header dependencies rather than
   parse includes itself?
4. What distinct roles do `-MMD -MF`, `depfile`, and `deps = gcc` play?
5. Why is `deps = gcc` valid when the compiler command uses `clang++`?
6. What does `ninja: no work to do` claim about the graph and filesystem state?

## Revision and next experiments

- Archive `math.o` into a static library and link `app` against it.
- Inspect archive members, object symbols, unresolved symbols, and relocations.
- Observe which steps rebuild after a source or public-header change.
- Later replace the handwritten graph with an equivalent CMake target graph and
  compare generated behavior.

## CMake and editor integration checkpoint

The real Milestone 0.1 CMake graph generated `build/debug/compile_commands.json`
with the correct public include path and C++23 mode for both translation units.
Because that database lives below the source tree rather than in an ancestor
directory of each source file, `clangd` did not discover it automatically and
reported a false missing-header error.

A repository `.clangd` now states:

```yaml
CompileFlags:
  CompilationDatabase: build/debug
```

Direct `clangd --check` validation succeeded for the library source and consumer.
This records a concrete distinction: a correct build does not automatically mean
editor tooling has recovered the same compilation context.
