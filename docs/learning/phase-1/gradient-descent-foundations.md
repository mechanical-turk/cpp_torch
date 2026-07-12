# Gradient Descent Foundations

## Milestone connection

- Phase 1 — Scalar learning systems laboratory
- Milestone 1.1 — Manual Linear Regression
- Status: theory diagnostic in progress

## Demonstrated understanding

The learner independently demonstrated:

- (w) is slope and (b) is the intercept in \(\hat y=wx+b\).
- Residual convention: \(r_i=\hat y_i-y_i\).
- Per-observation squared loss: \(\ell_i=r_i^2\).
- Mean loss: \(L=(1/n)\sum_i\ell_i\).
- One-variable derivative sign and magnitude as local change information.
- The gradient is the derivative in one dimension and a vector of partial
  derivatives in multiple dimensions.
- Negative gradient versus gradient-descent step: direction first, then scaling
  by positive learning rate.
- For one observation:

  \[
  \frac{\partial\ell_i}{\partial w}=2r_ix_i,
  \qquad
  \frac{\partial\ell_i}{\partial b}=2r_i.
  \]

- For mean squared error:

  \[
  \frac{\partial L}{\partial w}=\frac{2}{n}\sum_i r_ix_i,
  \qquad
  \frac{\partial L}{\partial b}=\frac{2}{n}\sum_i r_i.
  \]

- The slope sensitivity contains \(x_i\) because
  \(\partial\hat y_i/\partial w=x_i\), whereas intercept sensitivity is always
  one.
- A learning rate balances local-approximation validity against useful progress.

## Misconceptions corrected

- Residual signs were initially reversed while squared loss remained correct.
- The first expanded slope derivative initially omitted the \(2w x_i^2\) term.
- The first intercept derivative introduced an extra \(2x_i\); chain-rule
  sensitivity \(\partial r_i/\partial b=1\) removed it.
- Gradient was briefly conflated with negative gradient. The gradient describes
  steepest local increase under Euclidean geometry; gradient descent uses its
  negative.
- A translation from several parameters to first-order error was initially framed
  as compounding parameter error. The actual approximation gap comes from omitted
  curvature and higher-order terms.

## Quiz evidence

The learner correctly retrieved:

- update direction from derivative sign;
- one- and two-parameter changes under a learning rate;
- the local loss-change sum;
- the negative sum-of-squared-partials form after substituting a gradient step;
- the reason large learning rates may overshoot local information; and
- per-example and mean-loss gradient derivations.

## Teaching calibration

- Proceed one conceptual step at a time.
- Use Socratic questions and avoid assuming vector-calculus vocabulary.
- Assign derivations and conceptual explanations to the learner.
- Codex performs repetitive numerical arithmetic unless it is itself instructive.

## Next concept

Build dot-product intuition from ordinary two-dimensional vectors, then use it to
interpret directional derivatives and prove the negative gradient is the steepest
descent direction under a fixed Euclidean step length.

## Retrieval prompts

1. Distinguish derivative, gradient, negative gradient, and update step.
2. Derive both MSE gradient components through residual notation.
3. Why does a negative-gradient step guarantee only a first-order local decrease?
4. What role does the learning rate play beyond choosing a direction?

