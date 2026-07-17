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
learning rate `0.1`. Excessive-learning-rate evidence remains.
