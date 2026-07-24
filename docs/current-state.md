# Current Learning State

This file is the concise recovery point for a fresh session. Detailed material
belongs in the active milestone file.

## Governing plan

- Plan: [`docs/learning-plan.md`](learning-plan.md)
- Active phase: Phase 2 — Contiguous tensor foundations
- Active milestone: Milestone 2.1 — Contiguous Tensor Representation
- Milestone file: [`docs/milestones/02-01-contiguous-tensor-representation.md`](milestones/02-01-contiguous-tensor-representation.md)
- Status: representation and checked-indexing implementation active

## Current gate

The active gate is the contiguous representation contract: demonstrate correct
row-major indexing and failure behavior across ordinary, scalar, and zero-sized
shapes before extracting the experiment into reusable project code.

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
- Authored a working Ninja graph that separately compiles two translation units
  and links an executable.
- Diagnosed a missing final newline from Ninja's unexpected-EOF error.
- Correctly predicted and observed incremental rebuild propagation.
- Reproduced a stale build caused by missing header dependencies.
- Added Clang-generated GCC-style depfiles and verified Ninja's recorded header
  dependencies with `ninja -t deps`.
- Archived `math.o` into `libmath.a`, linked the consumer against it, and
  inspected archive membership.
- Confirmed with `nm -C` that the library object defines `add(int, int)` while
  the consumer object holds an unresolved reference before final linking.
- Defined the Milestone 0.1 implementation contract and mastery gate.
- Implemented and committed the minimal CMake library boundary with successful
  Debug and Release builds.
- Verified private-source (three-step) versus public-header (four-step)
  incremental rebuild propagation.
- Added `.clangd` pointing to `build/debug/compile_commands.json` and verified
  both translation units with direct `clangd --check` runs.
- Diagnosed deliberate compile-time type failure and link-time missing-symbol
  failure, then restored a clean green build.
- Completed the active mastery assessment with targeted correction and retrieval
  of translation-unit/object-file and CMake usage-requirement concepts.
- Passed Milestone 0.1 based on implementation, experiments, failure diagnosis,
  and live mastery evidence. A duplicative written retrospective was waived due
  to low marginal learning value.
- Established that testing concepts transfer from TypeScript/Python while C++
  framework and compiled-test workflow experience is new.
- Selected pinned GoogleTest v1.17.0 with CMake FetchContent and CTest discovery
  for the first production testing workflow.
- Integrated a compiled GoogleTest target, individual CTest discovery, structured
  failure diagnostics, and a verified `BUILD_TESTING=OFF` configuration.
- Added a narrow `.clang-format` rule after format-on-save collapsed short test
  bodies; command-line formatter installation remains deferred.
- Completed manual ASan/UBSan failures, an LLDB inspection, opt-in target-scoped
  sanitizer integration, and a real project-defect detection/restoration cycle.
- Established target-scoped warnings, opt-in warnings-as-errors, project-filtered
  clang-tidy, reproducible formatting, and editor final-newline behavior.
- Established pinned, opt-in Release benchmarks, optimizer-elimination evidence,
  assembly inspection, profiler sampling, and reproducible CMake presets.
- Updated the Phase 0 formatting policy so reference ampersands bind visually to
  the referenced type and multiline function parameters use one parameter per
  line with the closing parenthesis on its own line, while preserving the
  learner's existing formatter rules.
- Established and remotely verified cross-platform/compiler GitHub Actions
  acceptance checks.
- Derived and retrieved per-observation and mean MSE gradients with respect to
  slope and intercept.
- Demonstrated gradient versus negative-gradient direction, learning-rate
  scaling, and first-order local loss-change reasoning through a quiz.
- Derived directional derivatives by restricting a two-variable loss to a path,
  and proved negative-gradient steepest descent using dot-product geometry.
- Implemented a learner-authored scalar linear-regression experiment with explicit
  prediction, residual, MSE, analytic gradient, and gradient-descent updates.
- Added central-difference numerical gradients and corrected a sum-versus-mean
  mismatch: both numerical and analytic gradients now describe mean loss.
- Verified at `(w,b)=(1,1)` that both gradient components agree to approximately
  `2e-11`, with a strictly warning-clean C++23 build.
- Extended the comparison to `(2,1)` and `(-1.5,3)`. The analytic and numerical
  gradients agree within approximately `1.3e-10`; the exact-fit point has zero
  analytic gradient and only floating-point-scale numerical residue.
- Extracted the regression behavior behind a reusable header/source boundary,
  replacing compile-time `std::array` dataset-size templates with a read-only
  `std::span<const Sample>` view.
- Added a GoogleTest that compares both analytic gradient components against
  central differences at three parameter points with `1e-8` tolerance.
- Added CMake library and example targets, connected the test target to the
  library's public C++23/include usage requirements, refreshed the `dev`
  compilation database, and verified both discovered tests pass.
- Separated a silent `gradient_descent_step` from orchestration and presentation,
  then added a strict automated convergence test. From `(w,b)=(1,1)`, learning
  rate `0.1` reaches the known `(2,1)` solution and near-zero loss within
  `1e-8` after 1000 epochs.
- Added deliberate instability evidence: with the same start and data, learning
  rate `1.0` increases loss from about `1.67` to `5.42e11` after 10 epochs.
- Derived the exact global learning-rate stability interval
  `0 < a < (4-sqrt(10))/2 ≈ 0.4189` by reducing two preserved error relationships
  to scalar recurrences, then independently proved the two directions form a
  basis and therefore cover every initial error vector.
- Added a CMake-built CSV experiment comparing rates `0.4`, the theoretical
  boundary, and `0.43`. At epoch 100, loss is approximately `9.97e-9`, `1.5712`,
  and `4.98e4` respectively, matching convergence, non-decaying boundary
  behavior, and divergence.
- Added a Python/Matplotlib loss visualization over 200 epochs. The stable run
  reaches floating-point-scale loss, the boundary remains at `1.5712`, and the
  unstable run grows to approximately `1.58e9`.
- Established public invalid-input contracts: dataset evaluation and numerical
  gradients reject empty datasets, and numerical gradients reject non-positive
  finite-difference steps with `std::invalid_argument`. Seven tests pass under
  both strict and ASan/UBSan configurations.
- Added explicit known-value prediction, MSE, and analytic-gradient tests. Nine
  tests now pass under both strict and ASan/UBSan configurations, completing the
  milestone's implementation-level correctness evidence.
- Passed the mastery review across derivation, stability, numerical checking,
  C++ boundaries, invalid-input policy, and optimization-versus-generalization.
- Implemented a value-semantic contiguous `double` tensor experiment with
  explicit scalar, singleton, empty, and overflow-safe shape semantics.
- Implemented row-major stride construction and checked multidimensional
  indexing. Observed correct values for several rank-3 coordinates.
- Diagnosed an unsigned reverse-loop underflow with ASan: `i >= 0` is always
  true for `std::size_t`, causing `result[i - 1]` to write before the vector.
  Replaced it with the terminating condition `i > 0`.
- Verified the current tensor experiment is warning-clean under the strict
  compiler flags and passes both ASan and UBSan.
- Added const and mutable `at()` overloads that share one checked offset helper.
  Spans are passed by value as lightweight non-owning views. Assigning through
  the mutable reference changed the selected stored value to `42`; strict and
  sanitized runs remained clean.
- Promoted `Tensor` into the public `cpp_torch` library boundary. Removed the
  obsolete production `math.cpp`, `math.hpp`, and `math_test.cpp`; CMake now
  builds `src/tensor.cpp`, and `basic_usage` consumes the tensor API. The `dev`
  build succeeds and all eight remaining tests pass.

## Open questions and review findings

- Revisit the distinction between static and shared-library update behavior.
- Later revisit namespace-scope `const` linkage; the topic was intentionally
  paused to establish the simpler model first.
- CMake syntax and generated behavior must now be learned through the real
  implementation rather than more abstract diagnostics.
- Compilation-database discovery should be retrieved again in later tooling
  work.
- Curvature, Hessians, convexity, and learning-rate stability are not yet
  sufficiently grounded.
- Additional sanitizers remain dependency-triggered: TSan for concurrency, MSan
  for specialized Linux uninitialized-read coverage, and vptr checks when
  polymorphism becomes real.
- Teaching protocol update: before every new subject, provide a named unit and
  purpose/scope/value explainer so the learner can decide whether to pursue it.
- Deferred at the learner's request: explicit observed evidence for rank
  mismatch, per-axis bounds failure, rank-0 scalar access, and zero-sized tensor
  access. The implementation contains the checks, but this portion of the
  indexing gate has not been demonstrated.
- Deferred at the learner's request: the copy/move experiment currently accesses
  a moved-from tensor before reassignment and terminates with
  `std::invalid_argument`. Independent-copy output and safe reuse after
  reassignment remain unverified.

## Active detours or branches

- Completed short diagnostic detour: modern `inline` and ODR semantics.
- Active required detour: rebuild CMake intuition from first principles in
  `/Users/keremkazan/Documents/Projects/cmake-tutorial`. The recent target and
  usage-requirement work was mechanically successful but not yet retained well
  enough to count as mastery.
- Completed 2026-07-13: CMake targets-from-first-principles detour. The learner
  explained compiled, interface, and executable targets; usage requirements;
  target linking; generated artifacts; and incremental rebuild propagation.
- Closed 2026-07-23: C++20 named-modules detour. The manual pipeline and a
  working single-file `Value` module were demonstrated, then all experiment code
  was deleted because further tooling mechanics had lower learning value than
  returning to autograd. Modules remain a future tooling topic.

## Exact next action

Add a focused tensor test target/file for the promoted public representation;
retain the explicitly deferred indexing and copy/move cases as milestone debt.

## Active learning artifacts

- [`docs/learning/phase-0/compilation-linking-and-inline.md`](learning/phase-0/compilation-linking-and-inline.md)
- [`docs/learning/phase-0/ninja-build-graph-lab.md`](learning/phase-0/ninja-build-graph-lab.md)
- [`docs/learning/phase-0/cpp-testing-workflow.md`](learning/phase-0/cpp-testing-workflow.md)
- [`docs/learning/phase-0/sanitizers-and-lldb.md`](learning/phase-0/sanitizers-and-lldb.md)
- [`docs/learning/phase-0/warnings-and-static-analysis.md`](learning/phase-0/warnings-and-static-analysis.md)
- [`docs/learning/phase-0/benchmarking-and-profiling.md`](learning/phase-0/benchmarking-and-profiling.md)
- [`docs/learning/phase-1/gradient-descent-foundations.md`](learning/phase-1/gradient-descent-foundations.md)
- [`docs/learning/phase-1/scalar-autograd-foundations.md`](learning/phase-1/scalar-autograd-foundations.md)
- [`docs/learning/phase-2/contiguous-tensor-foundations.md`](learning/phase-2/contiguous-tensor-foundations.md)
- [`docs/learning/detours/cmake-targets-from-first-principles.md`](learning/detours/cmake-targets-from-first-principles.md)

## Last updated

2026-07-24 — Recorded checked row-major indexing, mutable access, library
promotion, removal of the obsolete math scaffold, and successful build/test
verification.
