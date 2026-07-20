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

## Numerical-gradient checkpoint

The first dataset-level numerical-gradient implementation summed per-example
gradients, while the analytic implementation differentiated mean loss. For a
dataset of size `n`, the numerical result was therefore `n` times the analytic
result. Dividing by the sample count aligned the objectives. At `(w,b)=(1,1)`,
both components then agreed to approximately `2e-11`.

This established an important checking invariant: two gradient implementations
are comparable only when they differentiate exactly the same scalar objective,
including reductions such as sum versus mean.

Checks at `(1,1)`, the exact-fit point `(2,1)`, and `(-1.5,3)` produced maximum
absolute disagreement of roughly `1.3e-10`. At the optimum, the analytic
gradient was exactly zero while numerical `dL/db` was about `3.7e-17`, showing
why floating-point checks need tolerances rather than exact equality.

The checks are now automated with per-component `EXPECT_NEAR` assertions at
`1e-8`. The code was separated from `main()` into a reusable CMake library. A
`PUBLIC` C++23 requirement and include directory propagate to linked consumers;
without the target edge, the example lacked both `-std=gnu++2b` and the header
search path during compilation.

## Convergence and instability checkpoint

The optimizer was separated from console output through a silent
`gradient_descent_step`. Automated evidence now shows that learning rate `0.1`
converges from `(1,1)` to the exact `(2,1)` solution, while learning rate `1.0`
raises loss from approximately `1.67` to `5.42e11` after only 10 epochs. This
observed contrast supplies the concrete motivation for deriving the curvature
of this particular loss surface; curvature is no longer an unmotivated detour.

## Exact two-parameter stability derivation

The learner reconstructed the dataset loss and gradients manually:

\[
L(w,b)=\frac{1}{3}(5w^2+3b^2+6wb-26w-18b+35),
\]

\[
\frac{\partial L}{\partial w}=\frac{10w+6b-26}{3},
\qquad
\frac{\partial L}{\partial b}=2w+2b-6.
\]

Using errors `u=w-2` and `v=b-1`, the learner derived the coupled update and
represented repeated gradient descent as `z_n=A^n z_0`. Two preserved error
ratios were found:

\[
r_{1,2}=\frac{-1\pm\sqrt{10}}{3}.
\]

Their scalar update multipliers imply the joint stability interval:

\[
0<a<\frac{4-\sqrt{10}}{2}\approx0.4189.
\]

The learner then independently closed the generalization gap: direction vectors
on the two distinct preserved lines are linearly independent and form a basis of
`R^2`; by linearity, every starting error decomposes into those directions, and
both components converge when both scalar multipliers have magnitude below one.

The learner connected the Hessian to gradient change through
`delta_g = H delta_theta`, then derived the exact quadratic relationship
`g(theta)=H[u,v]` by measuring from the zero-gradient optimum. Since `H` is
invertible, gradient convergence implies parameter-error convergence. The exact
solution has zero MSE, which is globally minimal because squared loss is
nonnegative.

Numerical verification now compares learning rates on both sides of the derived
boundary. After 100 epochs, `0.4` reaches loss near `1e-8`, the boundary retains
loss near `1.57`, and `0.43` grows to roughly `5e4`.

A Matplotlib plot over 200 epochs makes the orders-of-magnitude behavior visible:
the stable loss reaches floating-point scale, the boundary loss remains near
`1.5712`, and the unstable loss reaches roughly `1.58e9`. Parameter plots remain
to expose the sign-alternating boundary behavior hidden by squared loss.

Terminology and teaching corrections established during this unit:

- Coupling means each coordinate update depends on both errors; individual
  coordinate errors need not decrease monotonically for total loss to decrease.
- The preserved-ratio search is motivated by reducing a coupled recurrence to a
  scalar multiplier, not by assuming arbitrary linear combinations already have
  that form.
- New geometric or algebraic terminology must follow concrete motivation rather
  than precede it.

## Next concept

Turn the single-point numerical comparison into systematic multi-point
correctness evidence, then add convergence and unstable-learning-rate evidence.

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
