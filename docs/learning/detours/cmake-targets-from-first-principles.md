# CMake Targets from First Principles

## Reason for the detour

Milestone 1.1 required a library, example executable, and test consumer. The
resulting CMake graph worked, but include-directory propagation, language-feature
propagation, target creation, linking, and compilation-database refresh were
introduced too quickly to become intuitive.

This is a required prerequisite detour under the project's durable-learning
north star. Work will occur in the disposable repository:

`/Users/keremkazan/Documents/Projects/cmake-tutorial`

## Learning objective

The learner should be able to construct and explain, from a blank directory:

- the difference between directly invoking the compiler and describing a build;
- configure, generate, build, and run stages;
- source files, object files, executable targets, and library targets;
- target dependencies versus plain textual ordering;
- include directories and compile features as target usage requirements;
- `PRIVATE`, `PUBLIC`, and `INTERFACE` through observed compiler commands;
- why `target_link_libraries` can change consumer compilation as well as linking;
- how CMake generates Ninja rules and `compile_commands.json`; and
- how a developer build directory supports `clangd`.

## Teaching constraints

- Begin from a single source file and a manual compiler command.
- Introduce one CMake command or target relationship at a time.
- Predict generated compiler/linker behavior before running each build.
- Inspect verbose commands and generated artifacts after each change.
- Use break/fix experiments rather than importing the `cpp_torch` graph.
- Do not return to the active ML implementation merely because the tutorial
  builds; require unaided reconstruction and explanation.

## Current state

The learner manually compiled a single `main.cpp`, then authored the minimal
CMake description:

- `cmake_minimum_required(VERSION 3.26)`;
- `project(cmake_tutorial LANGUAGES CXX)`;
- `add_executable(app main.cpp)`; and
- a private `cxx_std_23` compile-feature requirement.

The learner correctly distinguished generating a build system from building the
application, identified the compile and link commands in verbose Ninja output,
and recognized that the first generated command lacked the manually requested
C++23 mode. After a `CMakeLists.txt` edit, the learner initially predicted no
regeneration, then observed Ninja invoke CMake automatically because the
generated build graph depends on its CMake inputs. The changed compile command
used Apple Clang's `-std=gnu++2b` spelling for CMake's `cxx_std_23` feature and
caused recompilation followed by relinking.

The tutorial then added `greeting.cpp` and `greeting.hpp`. With only `main.cpp`
listed on the executable, the learner correctly predicted a link-time undefined
symbol: the declaration permitted compilation, but no `greeting.cpp.o` appeared
in the linker command. Adding `greeting.cpp` as a second target source created a
second compile edge and resolved the symbol.

For incremental header dependencies, the learner proposed that compiler-emitted
dependency data lets Ninja propagate header changes to affected translation
units and then to link consumers. The essential model was correct. Two details
were refined: Ninja ordinarily uses timestamps rather than content hashing, and
the source file itself is not changed; instead, the object-producing edge becomes
dirty because an input is newer than its output. Touching the shared header
recompiled both objects and relinked the executable, as predicted after the
correction.

The completed tutorial graph then separated greeting into a compiled library,
represented header-only arithmetic as an `INTERFACE` library, and linked both
privately into `app`. The learner correctly explained the produced object and
static archive, why an interface target produces no artifact, how a linked
target supplies both compile requirements and linker input, and the meanings of
`PRIVATE`, `PUBLIC`, and `INTERFACE`.

Incremental behavior was also predicted and verified: changing the arithmetic
header rebuilt only `main.cpp.o` and `app`; changing the greeting header included
by both translation units rebuilt both objects, the archive, and the executable.
The learner distinguished an include directory that enables header discovery
from compiler-recorded exact header dependencies that dirty build edges.

## Detour outcome

Completed 2026-07-13. The CMake concepts directly required by Milestone 1.1 are
sufficiently recovered. Packaging and installation remain future topics.

## Exact next action

Return to `cpp_torch` and resume Milestone 1.1 at convergence testing.
