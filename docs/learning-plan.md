# cpp_torch Learning Plan

## 1. Purpose

`cpp_torch` is an educational C++ machine-learning library built to develop deep,
low-level understanding of both:

1. machine learning, including its mathematical foundations; and
2. modern, production-grade C++ engineering.

Neither track is subordinate to the other. The project is not a simplified race
to a working neural-network API, nor is machine learning merely an excuse to
practice C++. Important ideas must be understood mathematically, implemented,
tested, measured, debugged, and explained.

The long-term capability target includes increasingly sophisticated workloads,
eventually including small transformers and language models. This target guides
the dependency graph; it is not permission to skip foundations.

This plan has no deadlines. The expected investment is approximately 30–40
hours per week, but progression is determined by demonstrated mastery rather
than elapsed time.

## 2. North Star

Every decision should maximize durable learning and intellectual growth.

When in doubt:

- prefer understanding over progress;
- prefer hands-on investigation over passive explanation;
- prefer a clear manual implementation before an external abstraction;
- prefer measurement over performance intuition alone;
- prefer a small disposable experiment when it isolates an idea better;
- prefer revisiting a prerequisite over carrying a hidden gap forward; and
- prefer redesigning freely over preserving an educationally inferior API.

Working code is necessary, but it is not evidence of mastery by itself.

## 3. Scope

### In scope

- rigorous mathematics: linear algebra, multivariable calculus, probability,
  statistics, optimization, and numerical analysis;
- ML foundations, from regression through neural networks, attention,
  transformers, and small language models;
- tensors, numerical kernels, automatic differentiation, optimizers, modules,
  datasets, training loops, serialization, and experiment infrastructure;
- C++23 library design and the surrounding production ecosystem;
- ownership, lifetimes, value semantics, API design, error handling, templates,
  compilation, linking, packaging, testing, debugging, profiling, and CI;
- computer architecture, memory systems, allocators, cache behavior, SIMD,
  concurrency, and the C++ memory model;
- manual reference implementations followed by principled evaluation of
  optimized libraries and formats;
- simple data export from C++, followed by analysis and visualization in Python;
- advanced branches including convolutions, GPU programming, distributed
  systems, ML compilers, and model serialization; and
- explicit detour milestones whenever a prerequisite gap is discovered.

### Provisional non-goals

- recreating PyTorch feature for feature;
- matching PyTorch's API or serialization formats;
- achieving performance parity with mature vendor libraries;
- production-scale distributed training;
- polished cross-platform support from the beginning; and
- creating the public course during this project.

These non-goals may change when doing so increases learning value. The eventual
course will primarily use video, but course production and student-facing
repository design are currently out of scope. The repository is optimized for
the author's personal learning.

## 4. Working Agreement

### Responsibilities

The learner writes all project code and learning notes. The mentor does not
implement project features. The mentor:

- runs adaptive Socratic teaching sequences;
- probes reasoning and exposes hidden misconceptions;
- teaches mathematical, ML, C++, and systems prerequisites;
- helps design experiments and milestone acceptance criteria;
- reviews designs, diffs, tests, benchmarks, and explanations;
- gives progressively stronger hints before direct fixes;
- helps debug without prematurely removing the learning opportunity; and
- withholds milestone completion when mastery has not been demonstrated.

Disposable snippets used for teaching may be written collaboratively. Code that
becomes part of the project library is written by the learner.

### Feedback protocol

All work and all feedback must be attached to a named milestone. Reviews assess
only the dimensions relevant to that milestone, while considering:

- mathematical correctness;
- behavioral correctness and edge cases;
- C++ design and production tooling;
- performance reasoning and evidence; and
- clarity of explanation.

Feedback normally proceeds in this order:

1. diagnostic questions;
2. conceptual hints;
3. increasingly specific clues;
4. a direct explanation or fix only when further struggle has lower learning
   value.

### Adaptive roadmap rules

The roadmap is a dependency graph, not a calendar.

An unexpected topic is classified as one of:

- a prerequisite gap, which creates a required detour milestone;
- a high-value branch worth pursuing immediately; or
- a useful tangent recorded in the backlog.

APIs may be broken and redesigned freely. Important redesigns should be recorded
with the rejected model, observed failure, and improved reasoning.

## 5. Milestone Anatomy and Mastery Gate

The plan is hierarchical: broad phases contain small, focused milestones. Every
milestone should define the following before work begins:

1. **Motivation:** the concrete question or capability being pursued.
2. **Dependencies:** prerequisite milestones and assumed knowledge.
3. **Learning objectives:** mathematical, ML, C++, and systems outcomes.
4. **Socratic sequence:** adaptive questions, derivations, predictions, and
   counterexamples.
5. **Hands-on investigations:** tiny programs, debugger exercises, numerical
   checks, and benchmarks used during teaching.
6. **Implementation artifact:** the project code written by the learner.
7. **Correctness evidence:** unit tests, property tests where appropriate,
   reference comparisons, and numerical checks.
8. **Performance evidence:** measurements and explanations where relevant;
   optimization is required only when it serves the learning objective.
9. **Documentation artifact:** notes, derivations, design decisions, rejected
   alternatives, and experimental results.
10. **Review:** milestone-tethered feedback across the relevant dimensions.
11. **Mastery assessment:** explanation, derivation, debugging, and design
    defense without relying solely on the implementation.
12. **Retrospective:** what changed in the learner's mental model and what gaps
    remain.

A milestone completes only when the learner can, as applicable:

- derive the important mathematics and state its assumptions;
- predict behavior before running the program;
- explain the implementation and its invariants;
- justify ownership, lifetime, API, and error-handling decisions;
- test meaningful normal, boundary, and failure cases;
- use appropriate debugging and diagnostic tools;
- interpret measurements rather than merely report them; and
- identify the design's limitations and likely next redesign.

## 6. Technical Principles

### Language and platform

- Target C++23.
- Develop initially on macOS with Apple Clang, `clangd`, VS Code, and LLDB.
- Keep the build editor-independent and use standard, portable CMake practices.
- Add Linux Clang/GCC coverage after the initial foundation; defer MSVC until it
  has clear learning value.
- Use modern C++23 features where they improve the design, while learning their
  portability and toolchain implications.

### Numerical implementation

- Begin with `double` as the sole tensor element type.
- Use `long double` only when useful as an experimental higher-precision
  reference, not as the default tensor type.
- Add `float` and broader dtype machinery later as a dedicated lesson in
  precision, dispatch, stability, API design, and performance.
- Build clear, manual reference kernels before using Eigen, BLAS, or other
  optimized backends.
- Optimize only after establishing correctness and collecting measurements.
- Study loop order, locality, tiling, vectorization, and parallelism before
  comparing against production libraries.

### Deliberate throwaway work

Throwaway implementations are encouraged when they isolate a concept. In
particular:

- scalar autograd begins as a small laboratory rather than a required ancestor
  of tensor autograd;
- the first tensor may support contiguous storage only; and
- a later redesign introduces strides, offsets, shared storage, aliasing, views,
  and non-contiguous layouts.

The value of a discarded design must be captured in its retrospective.

### Dependencies

- Use production-grade development tooling rather than reimplementing test and
  benchmark frameworks.
- Implement domain mechanisms manually when doing so exposes important ideas.
- Introduce external numerical, concurrency, data, and serialization libraries
  only after building enough understanding to evaluate them critically.
- Evaluate dependencies and formats using explicit criteria: correctness,
  maintenance, API quality, performance, portability, interoperability,
  precision, schema evolution, security, compression, and dependency cost.

### Error handling

Do not impose an ideological project-wide policy prematurely. Study error
categories in context:

- assertions for violated internal invariants and programmer bugs;
- exceptions for invalid public API use during early milestones; and
- `std::expected`-style results for recoverable operations such as parsing and
  I/O when those milestones arrive.

The eventual policy should emerge from concrete comparisons.

### Data and visualization

- Start with transparent formats such as CSV and plain text.
- Implement a small documented binary format when persistence becomes relevant.
- Export experiment data from C++ and use Python notebooks for visualization.
- Treat serialization, schemas, reproducibility, and library selection as
  engineering subjects in their own right.

### PyTorch's role

- Initially use PyTorch as a behavioral oracle only after independent derivation
  and implementation.
- Study PyTorch source later, when its essential ideas can be distinguished from
  complexity caused by scale, compatibility, devices, and production demands.

## 7. Production Tooling Track

Production tooling begins immediately and expands when concrete problems make a
tool meaningful. The intended toolkit includes:

- target-based CMake and CMake presets;
- `compile_commands.json` and reliable `clangd` integration;
- a production test framework integrated with CTest;
- strict compiler warnings;
- AddressSanitizer and UndefinedBehaviorSanitizer, followed by other diagnostics
  when applicable;
- `clang-format` and `clang-tidy`;
- LLDB and deliberate debugger exercises;
- a production benchmark framework;
- profiling, allocation inspection, and hardware-aware performance analysis;
- GitHub Actions with milestone-specific acceptance checks; and
- installation, exported targets, external consumers, dependency managers, and
  packaging when the library boundary becomes concrete.

CI begins in the foundation phase. Acceptance criteria grow rather than being
pretended complete on day one.

Git is used normally, but is not a teaching track because the learner is already
proficient with it.

## 8. Dependency-Ordered Roadmap

The exact child milestones are created immediately before their parent phase or
when a discovered gap requires one. This avoids false precision while retaining
a coherent direction.

### Phase 0: Engineering baseline

Establish the smallest real C++23 library, executable, test, benchmark, and CI
workflow. Learn compilation and linking boundaries, CMake targets, warnings,
sanitizers, static analysis, LLDB, and acceptance criteria through concrete
artifacts rather than configuration dumping.

Initial intended milestones:

1. compile and link a minimal library and consumer;
2. add a testing workflow and practice test design;
3. make undefined behavior observable with sanitizers and LLDB;
4. add benchmark and profiling baselines; and
5. establish focused GitHub Actions checks.

### Phase 1: Scalar learning systems laboratory

Build the smallest end-to-end learning systems while isolating the mathematics.
Begin with manual linear regression, then a disposable scalar reverse-mode
autograd engine. Cover derivatives, the chain rule, computational graphs,
topological ordering, gradient accumulation, optimization, finite differences,
and object lifetime.

Likely demonstrations progress through linear regression, logistic regression,
and XOR, but each receives its own dependency-appropriate milestone.

### Phase 2: Contiguous tensor foundations

Build a deliberately limited dense, CPU-only, `double` tensor with contiguous
storage. Study shape algebra, indexing, storage order, integer overflow, bounds,
value semantics, moves and copies, invariants, exception safety, and reference
numerical kernels.

The first tensor is allowed to be replaced rather than generalized indefinitely.

### Phase 3: Memory, architecture, and general tensor layouts

Combine a dedicated systems sequence with a tensor redesign. Study object
lifetimes, allocation, alignment, cache hierarchies, virtual memory, locality,
and the cost model of tensor operations. Introduce shapes, strides, offsets,
shared storage, views, aliasing, non-contiguous layouts, reshape/transpose
semantics, and mutation hazards.

### Phase 4: Tensor operations and numerical kernels

Develop elementwise operations, broadcasting, reductions, and matrix
multiplication. For each operation, connect shape rules, forward mathematics,
numerical behavior, memory access, tests, and performance. Progress from obvious
reference kernels to measured improvements such as loop reordering, tiling,
SIMD, and eventually comparisons with Eigen or BLAS.

### Phase 5: Automatic differentiation

Build tensor reverse-mode autodiff from first principles. Cover local derivative
maps, vector-Jacobian products, gradient accumulation, saved intermediates,
broadcast/reduction backward rules, mutation/versioning, graph lifetime, and
gradient checking.

After reverse mode is grounded, branch into forward mode, Jacobian-vector
products, full Jacobians, higher-order derivatives, and their mathematical
relationships when they add conceptual value.

### Phase 6: Learning framework

Develop parameters, modules, initializers, activations, losses, optimizers,
training/evaluation modes, and explicit training loops. Revisit linear and
logistic regression and XOR using the actual library, then move to multilayer
networks and more substantial datasets.

Every convenience abstraction must follow an explicit implementation that makes
the hidden mechanism visible.

### Phase 7: Data, persistence, and experiment systems

Study datasets, sampling, batching, deterministic randomness, loaders, metrics,
checkpointing, schemas, and reproducible experiments. Begin with self-written
CSV/text and a simple binary format, then compare established libraries and
formats. Export raw results for Python visualization.

### Phase 8: Concurrency and parallel execution

Study the C++ memory model, threads, synchronization, atomics, false sharing,
work decomposition, and scheduling. Build small mechanisms such as a thread pool
before evaluating higher-level runtimes. Apply concurrency to data loading and
CPU kernels, with race detection, correctness tests, and scalability analysis.

### Phase 9: Neural architectures

Introduce architectures in dependency order, each with rigorous mathematics and
manual implementations. Expected branches include:

- convolution and spatial models;
- embeddings and sequence modeling;
- attention and multi-head attention;
- normalization and residual connections;
- transformer blocks; and
- a small language model with tokenization, training, evaluation, and sampling.

### Phase 10: Advanced systems branches

Pursue these as deep, individually scoped branches after the shared foundations:

- GPU programming and accelerator memory/execution models;
- advanced SIMD and kernel generation;
- distributed training concepts and small-scale experiments;
- ML graph compilers, tracing, fusion, and scheduling;
- richer serialization and model interchange; and
- production backend dispatch and external library integration.

This phase is intentionally open-ended. Coverage is chosen for conceptual depth,
not feature count.

## 9. First Concrete Milestone

The next planning conversation should define **Milestone 0.1: Minimal C++23
Library Boundary**. Its purpose is not to scaffold the entire future framework.
It is to understand and demonstrate the smallest production-shaped build:

- one library target;
- one public header and private implementation boundary;
- one external-facing consumer executable;
- reproducible Debug and Release builds; and
- an explanation of compilation, linking, target usage requirements, and how
  `clangd` obtains accurate build information.

Before any files are implemented, the mentor should run a Socratic diagnostic on
translation units, headers, declarations versus definitions, linkage, static
versus shared libraries, CMake targets, and compiler/linker stages. Detour
milestones should be created for gaps that deserve isolated treatment.

The milestone's detailed contract and acceptance criteria will be written only
after that diagnostic. Testing, sanitizers, benchmarks, formatting, static
analysis, and CI are separate small milestones so each tool is learned rather
than pasted into a monolithic setup.

## 10. Living Decisions and Open Questions

Decisions are recorded here when they affect multiple phases. Local choices
belong in their milestone notes.

Current decisions:

- dependency-based roadmap with no deadlines;
- approximately 30–40 hours per week available;
- uncompromised depth in both ML and C++;
- extreme mathematical depth, including proofs when meaningful;
- C++23, macOS, Apple Clang, `clangd`, VS Code, and LLDB initially;
- learner writes all project code;
- hands-on, adaptive Socratic teaching before and during implementation;
- milestone completion requires demonstrated mastery;
- production-grade tooling begins in Phase 0;
- `double` first, manual kernels first, external numerical libraries later;
- disposable experiments and complete redesigns are welcome;
- C++ to raw data to Python visualization initially;
- public GitHub repository with early CI;
- no early API compatibility promise; and
- course creation remains out of scope.

Questions intentionally deferred until grounded by experience:

- the final tensor ownership and aliasing model;
- the long-term dtype and kernel-dispatch architecture;
- the eventual project-wide error policy;
- external dependency and package-management strategy;
- installation and distribution strategy;
- serialization formats and libraries;
- CPU parallel runtime choices;
- GPU platform and abstraction level; and
- the exact breadth of advanced systems branches.

Deferral is deliberate: each decision should be made when the learner can
understand and test its implications.
