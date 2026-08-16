# Milestone 5.1 — Tensor Reverse-Mode Autograd Core

## Motivation

The tensor can now execute the forward operations needed by a dense model:
matrix multiplication, broadcast elementwise operations, and reductions.
Training requires differentiating compositions of those operations with respect
to tensor parameters. This milestone replaces handwritten tensor gradients with
a reverse-mode computation graph.

## Dependencies

- Milestone 1.2 — Scalar Reverse-Mode Autograd
- Milestone 3.1 — Stored Strides, Offsets, and Views
- Milestone 4.1 — Matrix Multiplication Reference Kernel
- Milestone 4.2 — Broadcasting Foundations

## Learning objectives

- Transfer node identity, reverse topological traversal, and gradient
  accumulation from scalar values to tensor values.
- Distinguish scalar local derivatives from tensor local linear maps.
- Understand vector-Jacobian products without materializing full Jacobians.
- Define which tensors require gradients and how gradients are initialized,
  accumulated, cleared, and observed.
- Implement backward rules for the smallest operation set needed by a dense
  model.
- Handle broadcast backward by reducing repeated logical uses.
- Validate tensor gradients with analytic cases and finite differences.
- Make graph ownership, saved-forward-state, and mutation assumptions explicit.

## Initial scope

The first vertical slice will deliberately avoid a broad framework API. It will
support a scalar loss built from a small set of tensor operations and propagate
gradients to leaf tensors. Higher-order gradients, in-place graph mutation,
device/dtype dispatch, concurrency, graph optimization, and production memory
reclamation are deferred.

Generalized batched matrix multiplication is also deferred. The first dense
model only requires `[batch,input] @ [input,output]`; rank-N batch dimensions
become a required kernel extension before multi-head attention.

## Initial diagnostic

For `C = A.matmul(B)` and scalar loss `L`, explain what information the backward
rule receives, what gradients it must produce, and why constructing the full
Jacobian of `C` with respect to `A` or `B` would be wasteful.

## Gate

The learner must derive and implement the core reverse-mode graph, accumulation,
and backward rules needed for an end-to-end scalar-loss tensor expression;
verify them analytically and numerically; and defend graph lifetime, gradient
state, broadcasting reduction, and mutation contracts.
