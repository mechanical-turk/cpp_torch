# Scalar Reverse-Mode Autograd Foundations

## Milestone connection

- Phase 1 — Scalar learning systems laboratory
- Milestone 1.2 — Scalar Reverse-Mode Autograd
- Status: prerequisite diagnostic pending

## Accepted unit orientation

The learner accepted a code-heavy disposable scalar engine to isolate reverse-mode
autodiff before tensor concerns. The unit will connect local derivative rules,
upstream sensitivities, accumulation, topological traversal, and C++ ownership.

## Teaching calibration carried forward

- Motivate each new subject before introducing its notation.
- Introduce one conceptual dependency at a time without reducing exercises to
  repetitive arithmetic.
- The learner authors project implementation; Codex maintains learning artifacts
  and supplies review, diagnostics, and progressively stronger hints.
- Classify learner answers precisely as correct, incomplete, or incorrect.

## Computation-graph diagnostic evidence

For one observation, the learner decomposed the expression into primitive nodes:

\[
m=wx,\quad p=m+b,\quad r=p-y,\quad L=r^2.
\]

After initially omitting the second input derivative of each binary operation,
the learner retrieved the complete local rules. In a one-at-a-time reverse pass,
the learner then correctly propagated an output seed of one to obtain:

\[
\frac{\partial L}{\partial r}=2r,\quad
\frac{\partial L}{\partial p}=2r,\quad
\frac{\partial L}{\partial m}=2r,
\]

\[
\frac{\partial L}{\partial b}=2r,\quad
\frac{\partial L}{\partial w}=2rx,\quad
\frac{\partial L}{\partial x}=2rw,\quad
\frac{\partial L}{\partial y}=-2r.
\]

This established the distinction between an operation's local derivative and the
stored total sensitivity `dL/d(node)` propagated from the scalar output.

## Manual graph implementation checkpoint

The learner authored a stack-allocated `Node {data, grad}` graph for one linear
regression observation. The forward values were constructed explicitly and the
reverse pass was handwritten in dependency order with `+=` accumulation. Strict
compilation produced loss `2.25` and the independently predicted gradients:

`r=-3`, `p=-3`, `m=-3`, `w=-6`, `x=-4.5`, `b=-3`, and `y=3`.

This is the baseline that later graph automation must reproduce. It contains no
ownership machinery, operator overloading, callbacks, or automatic traversal.

## Graph metadata and automatic traversal checkpoint

The learner extended each operation output with its operation kind and non-owning
links to its immediate input nodes. They explained why the output retains its
parents rather than each input retaining its consumers: one input may participate
in arbitrarily many later operations, while a primitive operation has fixed inputs.

The learner implemented local reverse rules for multiplication, addition,
subtraction, and square using `+=`, with assertions enforcing each operation's
required parent links. They then implemented a parent-first DFS that produces a
dependency-ordered `std::vector<Node*>`, and reverse iteration now replaces the
handwritten backward sequence. The original numerical gradients remain unchanged
under strict compilation.

The learner correctly predicted why traversal needs a visited set for a DAG:
when a node such as `m` is reused by `loss = m + m`, its gradient must accumulate
both incoming contributions, but its local backward rule must execute only once.
Running it twice would propagate the already-accumulated gradient twice.

The shared-node experiment `m=x*y; loss=m+m` then produced `loss=24`,
`m.grad=2`, `x.grad=8`, and `y.grad=6`, providing direct evidence for both
accumulation and unique traversal.

## Ownership and API checkpoint

The selected initial ownership model is a stack-friendly `Value` handle backed
by `std::shared_ptr<Node>`, with each operation output sharing ownership of its
parents. This permits graph values to be copied and returned while preserving
node identity and lifetime. The learner identified the reference-count overhead
accepted in exchange for this ergonomic lifetime model. Ownership edges point
only toward parents in an acyclic graph, so releasing outputs can trigger a
destruction chain without shared-ownership cycles.

Alternatives considered:

- `unique_ptr` cannot directly represent a node reused by multiple operations.
- An owning graph arena with borrowed node links avoids per-edge reference counts
  but couples every `Value` lifetime to an external graph owner.

The gradient-state contract separates clearing from backward propagation so
intentional accumulation remains possible. A fresh pass over a reused graph must
clear every reachable gradient and then seed the scalar output with one; stale
intermediate gradients otherwise get propagated again.

The learner began a reusable engine with a private shared-owned node handle and
read-only data/gradient access. Multiplication constructs a new operation node
with designated aggregate initialization, preserving named-field clarity while
hiding graph-node construction behind the `Value` API.

## Header/source boundary checkpoint

The reusable scalar engine was extracted into `value.hpp`, `value.cpp`, and a
consumer-only `main.cpp`. The learner encountered and corrected two concrete
translation-unit boundary failures:

- Defining `class Value` again in `value.cpp` was a class redefinition; the
  header owns the sole complete class definition, while the source supplies
  qualified out-of-class method definitions.
- Declaring but not defining the private constructor that wraps a shared node
  compiled successfully but produced an unresolved-symbol linker failure.

The final header exposes the complete `Value` layout through a
`std::shared_ptr<detail::Node>` while only forward-declaring `detail::Node`.
`Node`, operation metadata, traversal containers, and traversal algorithms remain
defined in `value.cpp`. This keeps consumer recompilation independent of changes
to those implementation details. A strict two-translation-unit build links and
reproduces the expected one-observation gradients across repeated cleared passes.

## Autograd-driven training checkpoint

The learner authored a CMake-built scalar linear-regression loop that constructs
mean squared loss entirely from `Value` operations, calls one reverse pass per
epoch, and replaces the parameter handles with fresh leaves after each gradient
step. No handwritten loss-gradient formulas appear in the training program.

The first run plateaued at loss `0.15625` with `w=b=1.625`. Review exposed an
update-order bug: after replacing `w`, the bias update incorrectly read the new
`w.data()` and zero-valued new `w.grad()` instead of the old bias state. The
learner corrected the bias update to use `b.data()` and `b.grad()`.

With learning rate `0.1` for 1000 epochs, the corrected program reaches `w=2`,
`b=1`, and loss approximately `1.66e-30`. This is the first end-to-end evidence
that the learner-authored reverse-mode graph can supply gradients that train a
model to the known optimum.

## Exact next diagnostic

Resolve the focused training-loop review, then complete a compact correctness and
mastery gate before beginning contiguous tensor foundations.
