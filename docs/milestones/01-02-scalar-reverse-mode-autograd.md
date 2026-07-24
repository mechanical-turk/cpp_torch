# Milestone 1.2 — Scalar Reverse-Mode Autograd

## Motivation

Replace handwritten global derivatives with a small scalar computation graph
whose operations know only their own local derivatives. Use the laboratory to
make reverse-mode accumulation, traversal order, and C++ graph lifetime concrete
before tensors introduce shapes, storage, broadcasting, and mutation hazards.

This implementation is deliberately disposable, but its mathematics, tests,
ownership reasoning, and diagnostic practices must be production-grade.

## Dependencies and diagnostic

- Milestone 1.1 complete
- Chain rule and partial derivatives are available but require retrieval through
  an explicit computation graph
- Gradient accumulation at reused values has not yet been assessed
- Reverse versus forward traversal and topological ordering have not yet been
  assessed
- C++ ownership strategy must be derived from graph lifetime requirements rather
  than selected prematurely

Begin with an adaptive diagnostic for the scalar graph of one linear-regression
observation:

\[
\hat y=wx+b,\quad r=\hat y-y,\quad L=r^2.
\]

The learner should identify graph nodes, local derivatives, upstream gradients,
reverse traversal, and accumulation points before designing the C++ type.

## Learning objectives

### Mathematics and ML

- Distinguish a function's local derivative rule from the total derivative of a
  final output with respect to an earlier value.
- Apply the chain rule as reverse propagation of upstream sensitivity.
- Explain why reverse mode computes gradients of one scalar output with respect
  to many inputs efficiently.
- Explain gradient accumulation when one value influences the output through
  multiple paths.
- Relate backward propagation to a topological ordering of a directed acyclic
  computation graph.
- Validate autograd results independently with analytic and finite-difference
  references.

### C++ and systems

- Design explicit node ownership and graph lifetime semantics.
- Compare value ownership, raw/non-owning links, `unique_ptr`, `shared_ptr`, and
  weak references against the actual graph requirements.
- Use operator overloading without obscuring graph construction or invariants.
- Represent local backward behavior while reasoning about capture lifetime and
  allocation cost.
- Define accumulation, repeated-backward, zeroing, and graph-reuse contracts.
- Detect lifetime and undefined-behavior defects with sanitizers.
- Keep public APIs minimal and test observable behavior rather than private
  representation.

## Hands-on sequence

1. Complete the graph/chain-rule prerequisite diagnostic.
2. Build a throwaway manual graph with explicit nodes and handwritten reverse
   steps; no operator overloading.
3. Specify ownership, lifetime, and gradient-state invariants.
4. Implement a minimal learner-authored scalar `Value` graph.
5. Add operations incrementally, with analytic and numerical checks for each.
6. Reproduce branching and reused-node accumulation cases.
7. Implement and explain topological reverse traversal.
8. Rebuild the linear-regression training loop using autograd rather than
   handwritten gradients.
9. Run strict, sanitized, and debugger-backed failure investigations.
10. Complete derivation, code, ownership, and debugging mastery gates.

## Initial non-goals

- Tensor storage, shapes, broadcasting, or tensor-valued gradients
- GPU execution or parallel backward passes
- A PyTorch-compatible API
- Graph optimization, fusion, or production performance
- Higher-order derivatives before first-order reverse mode is mastered

## Acceptance criteria

- Local derivative rules compose to correct total derivatives on multi-operation
  expressions.
- Reused values accumulate gradients from every downstream path.
- Backward traversal processes dependencies in a justified order.
- Results agree with analytic derivatives and central finite differences.
- Ownership and lifetime behavior is explicit, defended, and sanitizer-clean.
- Repeated backward and gradient reset behavior has a documented, tested
  contract.
- An autograd-driven scalar linear-regression loop converges without using the
  handwritten gradient implementation.
- Strict, ordinary, and sanitized test configurations pass.
- The learner can derive, implement, debug, and explain the full graph lifecycle.

## Evidence, review, mastery, and retrospective

Completed 2026-07-23.

Evidence:

- Derived and implemented local reverse rules for multiplication, addition,
  subtraction, and square.
- Demonstrated accumulation on a reused node and unique reverse-topological
  traversal.
- Chose and defended a shared-owned handle model, including its lifetime,
  reference-count, acyclic-ownership, and shallow-const implications.
- Defined and exercised explicit gradient clearing and repeated-backward
  behavior.
- Extracted a reusable header/source boundary with an incomplete internal node
  type and diagnosed both class-redefinition and missing-definition linker
  failures.
- Reproduced the known one-observation analytic gradients exactly.
- Trained scalar linear regression entirely through autograd, reaching `w=2`,
  `b=1`, and loss approximately `1.66e-30`.
- Passed ordinary, warnings-as-errors, and ASan/UBSan builds.
- Explained why parameter updates require rebuilding the dynamic forward graph:
  cached forward values, links, and resulting gradients belong to the old
  parameter state.

The planned broad GoogleTest and direct finite-difference suite for the disposable
engine was explicitly deferred to preserve momentum toward tensors. This is
recorded debt rather than production-grade validation; it must be restored if the
scalar engine is promoted or reused beyond this learning laboratory.

Retrospective:

Reverse mode became concrete as accumulated sensitivities flowing once through a
DAG in reverse topological order. The ownership experiment exposed that
value-like handles may have shallow constness and shared mutable graph state. The
engine also demonstrated why a working forward expression is not enough: graph
lifetime, repeated backward, reset semantics, and parameter-update ordering are
part of correctness.
