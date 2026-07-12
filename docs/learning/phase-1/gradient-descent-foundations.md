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

Build curvature intuition from a one-dimensional quadratic, then connect the
Hessian of linear-regression MSE to convexity and learning-rate stability.

## Directional derivative checkpoint

### Demonstrated derivation

For the concrete loss

\[
L(w,b)=w^2+b^2
\]

at \((1,2)\), the learner constructed paths from a starting point and a direction:

\[
(w(t),b(t))=(1+at,2+ct).
\]

Substitution created the one-variable path function:

\[
h(t)=L(1+at,2+ct),
\]

and direct differentiation gave:

\[
h'(0)=2a+4c.
\]

The learner independently recognized that

\[
\nabla L(1,2)=
\begin{bmatrix}2\\4\end{bmatrix}
\]

and therefore:

\[
h'(0)=\nabla L(1,2)^\top
\begin{bmatrix}a\\c\end{bmatrix}.
\]

The resulting interpretation was stated correctly: the dot product gives the
local rate of loss change when leaving a specific parameter point in the chosen
direction. For unit directions, it is change per unit Euclidean distance.

### Steepest descent geometry

Using

\[
\nabla L^\top d=\|\nabla L\|\|d\|\cos\theta,
\]

the learner identified \(\theta=\pi\) as the minimizing angle for unit \(d\), and
constructed:

\[
d_{\text{steepest}}=-\frac{\nabla L}{\|\nabla L\|}.
\]

Ordinary gradient descent was decomposed into this unit direction and step length:

\[
-\eta\nabla L
=
\eta\|\nabla L\|
\left(-\frac{\nabla L}{\|\nabla L\|}\right).
\]

The learner correctly concluded that ordinary gradient-descent steps shrink as
the gradient magnitude shrinks.

### Conceptual distinction established

- Parameter point: current location \(\theta_0\in\Theta\).
- Displacement direction: a vector based at that point, not a normalized parameter
  point.
- Path: \(\theta(t)=\theta_0+td\).
- Directional derivative: derivative at \(t=0\) of the one-variable composition
  \(L(\theta(t))\).
- Gradient: local partial-derivative vector evaluated at a specific point.

## Retrieval prompts

1. Distinguish derivative, gradient, negative gradient, and update step.
2. Derive both MSE gradient components through residual notation.
3. Why does a negative-gradient step guarantee only a first-order local decrease?
4. What role does the learning rate play beyond choosing a direction?
