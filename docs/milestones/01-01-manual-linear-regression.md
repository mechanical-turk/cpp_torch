# Milestone 1.1 — Manual Linear Regression

## Motivation

Build the smallest complete learning system without tensors, autodiff, modules,
or optimizers. Every mathematical quantity and parameter update remains explicit
so later abstractions have concrete meaning.

## Dependencies and diagnostic

- Phase 0 complete
- Learner understands the affine model, residuals, MSE, one-variable derivatives,
  partial derivatives, and the chain-rule derivation of MSE gradients
- Learner can apply the negative-gradient update in one and two parameters
- Dot-product geometry, first-order multivariable approximation, curvature, and
  convergence behavior require further grounding
- Routine arithmetic should be performed by Codex unless the mechanics themselves
  are the learning objective

## Learning objectives

### Mathematics and ML

- Interpret the affine model, residuals, per-example loss, and empirical risk.
- Derive MSE gradients through expansion and the chain rule.
- Understand gradient and negative-gradient geometry through dot products and
  directional derivatives.
- Derive why sufficiently small negative-gradient steps decrease a differentiable
  objective to first order.
- Derive the quadratic loss surface, Hessian, convexity, and conditions for a
  unique optimum in the one-feature case.
- Explain learning-rate stability, overshoot, oscillation, and convergence.
- Validate analytic gradients with central finite differences.
- Distinguish optimization success from statistical generalization.

### C++ and systems

- Represent a small dataset with clear value semantics.
- Separate prediction, residual, loss, gradient, and update responsibilities
  without prematurely building framework abstractions.
- Use `double`, deterministic data, const-correct interfaces, and explicit loops.
- Test mathematical invariants and gradient agreement with GoogleTest.
- Record loss history and export transparent CSV for Python visualization.
- Measure only where measurement answers a milestone question.

## Hands-on sequence

1. Complete gradient geometry and quadratic/convexity derivations.
2. Numerically inspect the loss surface with a disposable C++ or Python experiment.
3. Specify a minimal learner-authored C++ API and invariants.
4. Implement forward prediction, MSE, analytic gradients, and gradient descent.
5. Add finite-difference gradient checks and convergence tests.
6. Compare learning rates and intentionally reproduce overshoot/divergence.
7. Export and visualize loss/parameter trajectories.
8. Complete a derivation, code, and explanation mastery gate.

## Acceptance criteria

- Analytic gradients are derived and independently verified by central
  differences across several parameter values.
- Loss decreases under a justified stable learning rate and parameters converge
  to the known synthetic relationship within stated tolerances.
- A deliberately excessive learning rate produces explained instability.
- Tests cover prediction, loss, gradients, convergence, and invalid input
  contracts chosen during design.
- Strict, sanitized, and ordinary test configurations pass.
- Learner can connect every line of the training loop to its mathematical role.
- No tensor/autodiff/module abstraction is introduced.

## Evidence, review, mastery, and retrospective

The learner has implemented an explicit scalar training loop and analytic MSE
gradients. A central-difference checker exposed and corrected a sum-versus-mean
objective mismatch. At `(w,b)=(1,1)`, numerical and analytic components agree to
approximately `2e-11`. Systematic multi-point checks and GoogleTest coverage are
now implemented: both components agree within a `1e-8` assertion tolerance at
three parameter points. The regression behavior is exposed through a small
header/source boundary using `std::span<const Sample>`, with CMake library,
example, and test targets. Convergence and unstable-learning-rate evidence remain.
The optimizer has since been separated from console output, and an automated
test verifies convergence from `(1,1)` to the known `(2,1)` relationship at
learning rate `0.1`. Excessive-learning-rate behavior, boundary visualization,
and invalid-input contracts are now also verified. Focused prediction and
known-value loss tests now pass under strict and sanitized builds. The final
derivation, code, and design mastery review is complete.

### Mastery evidence

- Re-derived MSE gradients and correctly distinguished residual dependence on
  `x_i` from the additional slope sensitivity factor `x_i`.
- Explained central differences, their reduced truncation bias, and the
  floating-point cancellation tradeoff in choosing epsilon.
- Derived the exact Hessian and global learning-rate boundary, then generalized
  from its two preserved directions to arbitrary initial errors using a basis
  decomposition.
- Connected gradient convergence to parameter convergence through the constant,
  invertible Hessian and proved global optimality from zero nonnegative MSE.
- Explained `std::span` container flexibility and, after correction, its
  non-owning lifetime contract.
- Defended public/private implementation boundaries, exception-based invalid
  input contracts, and dataset-dependent learning-rate policy.
- Distinguished successful optimization of empirical risk from generalization:
  finite training samples do not prove the real data-generating relationship is
  linear or that unseen points lie on the fitted line.

### Revision topics

- Retrieve sum-loss versus mean-loss gradient scaling without prompting.
- Continue sharpening the distinction between API-surface motivation and linkage
  mechanics.
- State non-owning view lifetime obligations immediately when proposing spans.

### Retrospective

The implementation progressed from a printed scalar loop to a tested library,
reproducible stability experiment, and Python visualization. The most valuable
mathematical redesign was introducing the Hessian only after observed divergence
created a concrete question. The teaching process also established a permanent
requirement to orient new subjects before introducing their notation.

**Status: complete — 2026-07-20.**
