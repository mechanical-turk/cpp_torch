# Milestone 0.2 — Testing Workflow and Test Design Foundations

## Motivation

Integrate a production C++ test framework and make testing a first-class build
workflow before numerical behavior grows complex. Existing testing experience in
TypeScript and Python transfers; the new focus is compiled test targets, linking,
CTest discovery, diagnostics, and C++-specific test design.

## Dependencies

- Milestone 0.1 complete
- Existing unit/integration testing experience outside C++

## Diagnostic findings

- Learner has used unit/integration testing concepts in TypeScript and Python.
- Learner has not used GoogleTest, Catch2, doctest, or another C++ framework.
- Long theory-first setup has low learning value; integration should be hands-on.

## Learning objectives

- Explain the distinction between a test source, test executable, framework, test
  discovery, and test runner.
- Integrate a pinned GoogleTest dependency through CMake `FetchContent`.
- Build a test target that consumes only the public `cpp_torch` interface.
- Register/discover tests through CTest and run them from both executable and
  CTest layers.
- Use assertions whose diagnostics expose expected versus actual behavior.
- Observe and explain passing, failing, and filtered test runs.
- Begin distinguishing unit-test cases from integration and build-contract tests.

## Implementation contract

- Add `tests/math_test.cpp`.
- Pin GoogleTest `v1.17.0` through CMake `FetchContent`.
- Make test construction conditional on CTest's `BUILD_TESTING` option.
- Link a dedicated `cpp_torch_tests` executable to `cpp_torch` and
  `GTest::gtest_main`.
- Use `gtest_discover_tests` so CTest knows individual GoogleTest cases.
- Test the public header only; do not include private sources.

## Acceptance criteria

- Debug configuration downloads/configures the pinned dependency reproducibly.
- The test executable builds and directly lists/runs its tests.
- `ctest --test-dir build/debug` discovers and runs the test suite.
- At least one intentional failure is observed and explained before restoration.
- `BUILD_TESTING=OFF` configures/builds without creating the test target.
- Learner can explain every added CMake relationship and the runner/discovery
  layers without relying on memorized syntax.
- Working tree returns to a clean, passing state.

## Evidence, review, mastery, and retrospective

Pending implementation.

