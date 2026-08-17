# Current Learning State

This file is the concise recovery point for a fresh session. Detailed material
belongs in the active milestone file.

## Governing plan

- Plan: [`docs/learning-plan.md`](learning-plan.md)
- Active phase: Phase 5 — Automatic differentiation
- Active milestone: Milestone 5.1 — Tensor Reverse-Mode Autograd Core
- Milestone file: [`docs/milestones/05-01-tensor-autograd-core.md`](milestones/05-01-tensor-autograd-core.md)
- Status: initial architecture and mathematics diagnostic

## Current gate

Begin the tensor-autograd prerequisite diagnostic by transferring the established
scalar reverse-mode model to a tensor-valued matrix-multiplication node.

## Active review findings

- The output-shape derivation correctly handles equal dimensions, size-one
  expansion, and the important `0` versus `1` case.
- Effective-stride construction now correctly maps missing leading axes and
  size-one axes to zero and preserves each operand's own stored strides.
- The first complete traversal builds successfully but never advances
  `output_logical_idx`, so every output element repeats the value computed at
  the all-zero coordinate. Existing view and equal-shape tests exposed this.
- Output element-count multiplication is currently unchecked and must preserve
  the tensor's overflow contract.
- An old test expecting `[2]` and `[1,2]` to be incompatible is obsolete:
  right alignment makes them compatible. Codex will update this mechanical
  verification after the kernel is corrected.
- The logical-coordinate advancement bug and output-size overflow handling are
  fixed.
- Added broadcasting coverage for matrix-plus-bias, rank-three plus `[3,1]`,
  scalars, non-contiguous transpose views, empty dimensions, and incompatible
  shapes.
- All 30 tests pass under strict warnings-as-errors and ASan/UBSan.
- Learning artifact:
  [`docs/learning/phase-4/broadcasting-foundations.md`](learning/phase-4/broadcasting-foundations.md).
- Mastery gate passed: for `[2,3,4] + [3,1]`, the learner identified axes `i`
  and `k` as the reduction axes and explained that references preserve shared
  identity while explicit accumulation performs the required summation.
- Milestone 4.2 is complete.
- Exact next action: orient and begin Milestone 5.1 with the backward contract
  for `C = A.matmul(B)` under a scalar downstream loss.
- Active high-value branch: production of the public video series *Deep
  Learning, All the Way Down*. Long-form episodes optimize for coherent 16:9
  teaching, while Shorts are scripted and recorded separately under
  [Decision 0006](decisions/0006-record-shorts-separately.md).
- X analytics read-only authorization and bounded collection are operational
  for `@mechaturka`. The first snapshot retrieved seven posts from the permanent
  boundary of August 13, 2026 at 9:10 AM ET onward; the earliest result was the
  Episode 1 announcement at 9:14 AM. Full account history must never be pulled
  without explicit learner approval. Next gate: inspect the actual API charge
  before choosing any recurring snapshot schedule.
- Instagram Login analytics are operational for the new `@mechaturka` Creator
  account without a Facebook Page. At approximately 6:29 PM ET, the first Reel
  had 118 plays, reached 109 accounts, averaged 5.44 seconds of watch time, and
  had no interactions. This suggests an initial cold sample with shallow
  consumption, but remains an early baseline. Reassess at 24 and 72 hours.
- The initial X analysis found nearly identical reach for the Episode 1 and 2
  announcements (798 versus 800 impressions), but Episode 1 generated 102
  engagements and 20 link clicks versus Episode 2's 19 and four. Current
  working priority: improve announcement conversion and avoid inferring causes
  from the seven-post sample. Report:
  [`youtube-series/analytics/reports/2026-08-16-x-initial-analysis.md`](../youtube-series/analytics/reports/2026-08-16-x-initial-analysis.md).
- Cross-channel branding refresh is complete. X, LinkedIn, and YouTube now use
  the approved positioning and coordinated banner system. LinkedIn features the
  YouTube playlist and GitHub repository; X retains GitHub as its professional
  destination and keeps the high-performing Episode 1 announcement pinned.
- Chapter 2 recording has reached the overflow unit. Its script now resolves
  both Chapter 1 overflow TODOs: checked shape-product construction, including
  later zero dimensions, and two-pass coordinate validation that makes
  subsequent flat-index arithmetic safe by invariant.
- Chapter 2 is complete. The public `cpp_ml` README now treats `main.cpp` as the
  evolving series implementation, records the capabilities added in Episodes 1
  and 2, and uses episode-neutral build instructions.
- The native-Short backlog now contains 62 standalone ideas derived from
  Episodes 1-4 at
  [`youtube-series/shorts/episodes-01-04-ideas.md`](../youtube-series/shorts/episodes-01-04-ideas.md).
  This single file is both the idea ledger and the evidence-informed priority
  order. Its current leaders are the unsigned reverse-loop failure, the
  linear-versus-affine naming surprise, why dot product returns one number, and
  matrix multiplication as repeated dot products. Each targets an 18-24 second
  causal explanation with progressive disclosure and no CTA.
- Native Short 1 now has a complete recording script and quality gate at
  [`youtube-series/shorts/short-01-scalar-shapes/script.md`](../youtube-series/shorts/short-01-scalar-shapes/script.md).
  Its narration has been reduced to one 35-42 second causal chain with an
  immediate paradox hook and a single post-payoff CTA. Its exact next production
  action is to stage the four visual states and record two versions of the hook.
- Short 1's three-way comparison visual is complete at
  [`youtube-series/shorts/short-01-scalar-shapes/assets/tensor-shape-comparison.png`](../youtube-series/shorts/short-01-scalar-shapes/assets/tensor-shape-comparison.png).
  It is an opaque 1080x1176 PNG intended to fill the complete OBS canvas below
  the 1080x744 webcam region. Its comparison rows have been recomposed to use
  approximately the full vertical allowance rather than padding the previous
  wide-card design.
  Series-wide visual generation rules are recorded at
  [`youtube-series/production/visual-asset-guidelines.md`](../youtube-series/production/visual-asset-guidelines.md).
- A reusable transparent southeast attention arrow is available at
  [`youtube-series/assets/attention-arrow-southeast.png`](../youtube-series/assets/attention-arrow-southeast.png),
  with an editable SVG source beside it.
- Chapter 2 now has a project-local 16:9 thumbnail and publishing package with
  the recommended title, description, provisional chapters, pinned comment,
  and tags under `youtube-series/chapter-02/`.
- Episode 3 has been rebuilt from a blank page as a complete recording script.
  Its dependency chain is equal-shape arithmetic, shared traversal,
  tensor-valued reduction, dot product, and a forward linear prediction. The
  proposed final API was independently compiled and exercised under strict
  warnings. Exact next course-production action: learner review of the episode
  arc before implementation and recording.
- Episode 3 intentionally retains the compositional dot-product reference
  implementation, `(*this * other).sum()`. Its size-`n` intermediate allocation
  is documented as a performance hypothesis and TODO; fused multiply-accumulate
  will be compared only after reliable benchmarking is introduced.
- Episode 3 is scheduled for August 17 at 11:00 AM ET. Its HD processing,
  custom thumbnail, main-playlist membership, final description, and 19 tags
  are API-verified. Manual chapters are intentionally deferred. The remaining
  release checks are comments, end screen, and brief desktop/mobile playback;
  captions are not yet available.
- The first processed retention curve is now available for Episode 1. Audience
  watch ratio is 51.58% near 0:22, 18.95% near 0:45, and 13.68% near 1:07;
  relative retention also falls sharply. Episode 1 does not reach its
  tensor-specific lesson until approximately 2:10 or live coding until roughly
  7:35. Episode 2 still returns no retention rows; its three processed views
  predate public release and must not be treated as public watch behavior.
  Detailed report:
  [`youtube-series/analytics/reports/2026-08-16-retention-and-episode-04-strategy.md`](../youtube-series/analytics/reports/2026-08-16-retention-and-episode-04-strategy.md).
- Episode 4's first draft was rejected after the full YouTube audit. Although it
  displayed `inputs.matmul(weights) + bias` immediately, it delayed live code
  until 8:15 and the promised computation until 38:15, preserving the measured
  structural problem. The rewritten script targets 23-27 minutes, resolves one
  row-column dot product immediately, surfaces the real rank failure inside the
  first minute, begins implementation around minute two, produces matrix
  multiplication around minute five, makes the layer work with an intentionally
  expanded bias, and then derives broadcasting from that waste. The exact final
  expression works before edge-case hardening.
  The final reference implementation passed strict warning checks and
  ASan/UBSan in isolation; a second integration audit reconciled the obsolete
  Episode 3 shape-mismatch test, variable names, deliberate failure, and final
  output with the inherited single-file harness.
  Exact next production action: learner review of the replacement causal arc
  before recording.
- Episode 4's opening no longer previews finished code or a completed output
  before recording begins. Narration now starts immediately with the required
  series sentence while a one-observation dot product expands visually into
  `[m,n] @ [n,p] -> [m,p]`. The first live action constructs the batch and
  triggers the current rank error; unrelated header and exception cleanup has
  been removed from the opening path.
- Episode 4 now has a matched 1920x1080 opening visual pair under
  `youtube-series/chapter-04/assets/`. The first depicts a visually horizontal
  rank-one observation dotted with the same weights plus a scalar bias to
  produce one scalar prediction. The second preserves the composition while
  adding input rows, broadcasting the same bias, and producing one prediction
  per observation. Editable SVG sources and rendered PNGs are both retained.
  The opening script now discusses the first image while recapping the scalar
  prediction, switches to the second precisely when observations are stacked,
  and uses that transition to introduce matmul and scalar-bias broadcasting.
- Future episodes end with at most five retrieval questions and normally about
  three; Episode 3 now closes with three questions covering its central
  dependency chain.
- Beginning with Episode 3's publishing package, every episode answers its own
  closing retrieval questions in its first pinned comment. Episode openings now
  move directly from the required series sentence and economical recap into the
  new problem. Episode 4 therefore contains no spoken answer segment. See
  [Decision 0007](decisions/0007-move-retrieval-answers-to-first-comment.md).
- Episode openings are now standalone by default and no longer lead with "last
  episode" or "last time." Required prior ideas are restated directly, and
  publication continuity is mentioned only when indispensable. Episode 4's
  visual opening now begins with the single-observation computation itself.
  See [Decision 0008](decisions/0008-standalone-episode-openings.md).
- Episode 4's opening language and visual workflow are locked. Narration is
  written for natural speech rather than symmetrical explanatory prose; it
  begins immediately, discusses each visual while shown, does not preview
  nonexistent finished code, and moves from the established scalar computation
  into the real matrix limitation. These rules now govern future scripts in
  `AGENTS.md`.
- The opening itself begins with "Welcome back to Deep Learning, All the Way
  Down, where we...". There is no separate pre-introduction hook before that
  sentence; Episode 3's deleted preview block has been fully reconciled.
- Every future episode now requires a complete `publishing.md`, including
  platform-ready X and LinkedIn posts with timing and rollout strategy. Episode
  2's package now schedules X for roughly one hour after launch and LinkedIn for
  Monday morning.
- Episode 3's linear-prediction section now establishes observations, features,
  one weight per feature, weighted contributions, summation, bias, and expanded
  linear-model notation before compressing the computation into a dot product
  and translating it into C++.
- Initial cross-platform evidence now drives a named three-episode and
  three-Short experiment: capability-led packaging, a complete insight in the
  opening sentence, a concrete failure inside the first minute, meaningful code
  around minute two, and 20-25 second single-idea Shorts with progressive
  disclosure. Episode 3's scheduled title has been changed and API-verified as
  `Building a Linear Prediction from Scratch in C++ | Deep Learning, All the
  Way Down #3`. Long-form episode titles must retain the exact series name and
  episode number even when their leading promise changes.
- X publishing packages now use one durable navigation reply beneath every
  episode announcement: complete YouTube playlist plus GitHub source. The main
  tweet continues to link directly to its specific episode.
- Episode 3 now closes by previewing Episode 4's complete destination:
  matrix multiplication plus broadcasting to evaluate
  `inputs.matmul(weights) + bias` for batched dense computation.
- Retrieval answer keys must reproduce and answer the same episode's actual
  closing questions without silent substitution or omission. Episode 3's
  publishing package now contains the first pinned-comment answer key.


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
- Added value-semantic equal-shape `Tensor::operator+`. It rejects differing
  ranks/shapes, copies output ownership once, moves completed local vectors into
  the result, accepts a const right operand, and leaves both inputs unchanged.
  The first known result (`2 + 1 = 3`) was observed under normal and sanitized
  builds; the second element and rejection paths remain unautomated.
- Added equal-shape elementwise `Tensor::operator*` and extracted operation-
  neutral same-shape validation. Strict and sanitized runs produced complete
  known outputs: `[2,3] + [1,4] = [3,7]` and
  `[2,3] * [1,4] = [2,12]`.
- Refactored addition and multiplication through a private const
  `elementwise_binary` member. An abbreviated function-template parameter
  accepts operation-specific lambdas while the helper centralizes shape
  validation, allocation, traversal, and result construction. Known outputs
  remain correct under strict and sanitized builds.
- Demonstrated the template visibility model: `auto operation` makes the helper
  a function template; its lambda specializations work from `tensor.cpp`
  because all instantiating calls and the complete definition occur in that
  translation unit. Correctly predicted that moving the calling operator bodies
  into the header while hiding the helper definition in the `.cpp` would fail
  at instantiation.
- Added rank-1 `dot()` by composing elementwise multiplication with full sum.
  `[2,3] dot [1,4]` produces rank-0 value `14` under strict and sanitized
  builds.
- Workflow decision: Codex owns mechanical example and verification-harness
  maintenance; the learner remains responsible for learning-critical library
  and algorithm implementation.
- Derived zero-copy transpose metadata, storage offsets, strided column views,
  and non-empty/empty view bounds. Added stored row-major strides and base
  offset to `Tensor`; indexing no longer allocates/recomputes strides.
- Chose explicit deep-copy semantics for ordinary tensor copies and shared
  storage only for explicit view-producing operations (Decision 0004).
- Retrieved the Rule-of-Five implications: custom copies suppress implicit
  moves, explicitly defaulted memberwise moves are appropriate, and `noexcept`
  enables container relocation without fallback copies.
- Migrated numerical storage to `shared_ptr<vector<double>>` while preserving
  public borrowed read-only storage access. Implemented logical materialization
  over shape/strides/offset, including scalar and empty traversal.
- Implemented deep copy construction by materializing logical values into new
  contiguous storage. Implemented strong-guarantee copy assignment with a
  complete temporary and generic `std::swap`, relying on one non-throwing move
  construction and two non-throwing move assignments.
- All 16 tests pass under strict warnings and ASan/UBSan after adding an
  independent copy-assignment contract case.
- Implemented rank-two `T()` as a zero-copy transpose by swapping shape and
  stride axes while sharing storage and preserving offset.
- Added mechanical tests proving transpose coordinate mapping, bidirectional
  mutation aliasing, rank validation, and independent compact materialization
  when a transpose view is copied. All 19 tests pass under strict warnings and
  ASan/UBSan.
- Reworked `sum()` to traverse logical coordinates without materializing an
  `O(numel)` input copy. Reworked elementwise operations to allocate only their
  contiguous output and read both inputs through logical view coordinates.
- Added transpose addition/multiplication regression coverage. All 20 tests pass
  under strict warnings and ASan/UBSan.
- Implemented `select(axis,index)` as a zero-copy rank-reducing view: it removes
  the selected shape/stride entry and advances the inherited base offset by
  `index * strides[axis]`.
- Added coverage for middle/last-axis selection, nonzero offsets, aliasing,
  chained selection to a scalar, invalid axes/indices, and subset
  reduction/arithmetic. All 23 tests pass under strict warnings and ASan/UBSan.
- Derived contiguity as gap-free logical row-major traversal. Implemented
  `is_contiguous()` by scanning right-to-left with an expected suffix-block
  stride, ignoring stride values on size-one axes and treating scalar/empty
  tensors as contiguous. Offset does not affect contiguity.
- Added coverage for base tensors, transposes, row/column selections, scalars,
  empty tensors, and a size-one axis with a deliberately noncanonical stride.
  All 24 tests pass under strict warnings and ASan/UBSan.
- Removed the misleading public `storage()` accessor after views made clear that
  a backing allocation is not the tensor's logical value sequence.
- Passed Milestone 3.1 through a live mastery review covering ownership,
  aliasing, copy-of-view materialization, chained view mapping, bounds,
  contiguity, and representation synthesis.
- Completed the Milestone 3.2 prerequisite diagnostic. The learner now
  distinguishes cache-line utilization, prefetch latency hiding, bandwidth,
  hierarchy-level bottlenecks, spatial locality, and temporal reuse, with
  corrections around register versus cache-line residency.
- Added and measured the first 1024-by-1024 layout benchmark: contiguous median
  approximately 2.55 ms versus transpose 4.38 ms (1.72x), with substantially
  higher transpose variability and no fixed thread affinity.
- Added cleanly compiling raw-vector contiguous/transpose cases using the same
  coordinate traversal. After restoring 1024-by-1024, raw medians were about
  1.00 ms contiguous and 1.56 ms transpose; Tensor medians in the same run were
  2.58 ms and 4.47 ms.
- Added a 2 KiB through 32 MiB working-set sweep. Transpose/base ratios remained
  near 1 through 512 KiB, rose at 8 MiB, and reached 4.04x Tensor / 2.09x raw at
  32 MiB, matching the learner's cache-line retention/eviction prediction.
- Passed Milestone 3.2 with a deliberate stop before hardware-counter profiling
  or fast paths. Exact cache attribution and deeper profiling are preserved for
  a future kernel-optimization branch.
- Derived and implemented rank-two matrix multiplication with logical view
  access, contiguous output, zero-inner-dimension semantics, and output-size
  overflow validation.
- Added rectangular, non-contiguous, zero-sized, invalid-input, and overflow
  tests. All 28 tests pass under strict warnings and ASan/UBSan.
- Passed Milestone 4.1 with matrix-specific optimization and profiling deferred.
  The learner requested forward progress after authoring and validating the
  reference kernel.

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
- Previously deferred representation cases are now mechanically covered by a
  Codex-authored tensor suite: rank mismatch, per-axis bounds, scalar access,
  zero-sized access, empty sum, independent copies, moved-from reassignment,
  arithmetic, reduction, and invalid operands.
- These tests establish implementation behavior but do not substitute for
  learner-authored mastery evidence. Copy/move guarantees and representation
  limitations still require retrieval.
- The current logical-coordinate traversal is a correct reference path but
  performs per-element checked indexing and index advancement. Contiguous fast
  paths remain deferred to an evidence-driven optimization milestone.
- The learner initially treated a size-one axis as if coordinate `1` were valid,
  then corrected the model: its only coordinate is zero, so its stride cannot
  affect physical traversal.

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

Review Episode 4's replacement, analytics-driven causal arc before recording.
When the technical learning track resumes, begin the Milestone 5.1 diagnostic
for the backward contract of `C = A.matmul(B)` under a scalar downstream loss.

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
- [`docs/learning/phase-3/layout-and-view-foundations.md`](learning/phase-3/layout-and-view-foundations.md)
- [`docs/learning/phase-3/traversal-cost-and-memory-locality.md`](learning/phase-3/traversal-cost-and-memory-locality.md)
- [`docs/learning/phase-4/matrix-multiplication-foundations.md`](learning/phase-4/matrix-multiplication-foundations.md)
- [`docs/learning/detours/cmake-targets-from-first-principles.md`](learning/detours/cmake-targets-from-first-principles.md)

## Video-series production state

- The canonical release and distribution history is maintained in
  [`docs/distribution-timeline.md`](distribution-timeline.md).
- Episodes 1 and 2 are public. Two X announcements and one LinkedIn announcement
  are confirmed.
- Episode 3 is now uploaded and scheduled for Monday, 2026-08-17 at 11:00 AM
  ET. The August 16 API audit verified HD processing, custom thumbnail, main
  playlist membership, and the exact schedule. Remaining prepublication work:
  end-screen verification, a manual comments-setting check, and brief desktop
  and mobile playback. Tags are live; captions are not yet available. Manual
  chapters are intentionally omitted until a transcript-assisted workflow makes
  them inexpensive and reliable.
- The target cadence is Monday-Wednesday-Saturday at 11:00 AM ET.
- The next distribution actions are the Episode 2 approximately 48-hour
  analytics snapshot, Episode 3's release and X announcement, Short 1's 24-hour
  cross-platform checkpoint, and a tailored r/cpp Show and Tell submission.
  Short 1 is already public on YouTube, X, and Instagram. The missed Episode 2
  LinkedIn announcement has been cancelled.
- The native vertical recording system is documented in
  [`youtube-series/production/vertical-obs-setup.md`](../youtube-series/production/vertical-obs-setup.md): separate OBS profile and scene collection, calibrated mobile code typography, camera/X branding, sharp and 4 px blurred code states, and deterministic production hotkeys.
- Short 1 now has its final 1080x1920 branded thumbnail at
  [`youtube-series/shorts/short-01-scalar-shapes/thumbnail.png`](../youtube-series/shorts/short-01-scalar-shapes/thumbnail.png).
- Short 1's complete release package is ready at
  [`youtube-series/shorts/short-01-scalar-shapes/publishing.md`](../youtube-series/shorts/short-01-scalar-shapes/publishing.md).
  It was published Sunday, 2026-08-16 at 2:00 PM ET, ahead of Episode 3.
- Publishing governance now requires every `publishing.md`, including native
  Short packages, to contain a concise platform-ready pinned comment.
- Local YouTube automation is operational under
  [`tools/youtube-channel/`](../tools/youtube-channel/). OAuth authorization with
  analytics, account-read, and channel-management scopes succeeded; the first
  private sync discovered 15 uploads and stored a timestamped snapshot. The
  Analytics API has not yet processed rich rows for Episodes 2-3 or Short 1, so
  current reporting falls back to Data API counters. The accepted security and
  mutation contract is recorded in
  [Decision 0007](decisions/0007-local-youtube-channel-automation.md).
  The OAuth app is in Production and the durable token was reissued after that
  transition, avoiding Testing mode's seven-day refresh-token expiration.
  Analytics now use a committed 2026-08-12 series boundary, excluding 11 older
  unrelated uploads from both reports and per-video Analytics API queries.
- Short 1 published at exactly 2:00:03 PM ET on 2026-08-16:
  `https://www.youtube.com/shorts/pC-Ng6V9a_Q`. The first API snapshot recorded
  8 views. The finalized channel comment was posted through the API and manually
  pinned. The Short is in the dedicated public Shorts playlist. YouTube does not
  expose its related-video field through Data API v3, so that setting remains
  unverified.
- The first series-only analytics analysis is recorded at
  [`youtube-series/analytics/reports/2026-08-16-initial-baseline.md`](../youtube-series/analytics/reports/2026-08-16-initial-baseline.md).
  It keeps current public counters separate from delayed detailed Analytics and
  excludes the channel's older uploads.
- The immediate Aug 16-22 production and distribution schedule is recorded at
  [`youtube-series/production/immediate-distribution-plan-2026-08-16.md`](../youtube-series/production/immediate-distribution-plan-2026-08-16.md).
  Long-form production remains the critical path; native Shorts, X, LinkedIn,
  Reddit, blogging, and Hacker News each have separate gates and windows.
- Cross-platform analytics access and profile branding are now an active
  distribution branch documented at
  [`youtube-series/production/social-analytics-and-branding-plan.md`](../youtube-series/production/social-analytics-and-branding-plan.md).
  YouTube, bounded X, and owned-profile Instagram collection are operational.
  LinkedIn personal analytics still requires vetted Community Management
  access.

## Last updated

2026-08-17 — Episode 4 was rewritten around a stronger dense-layer promise, an
immediate row-column result, a real rank failure, early implementation, and
repeated observable payoffs. Decision 0007 moves each episode's retrieval
answers into that episode's own first pinned comment. The technical learning
track remains at the Milestone 5.1 tensor-autograd diagnostic; video production
and distribution are the active high-value branch.
