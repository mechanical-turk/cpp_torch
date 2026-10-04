# Chapter 11 keyword research

Prepared September 14, 2026, before drafting the script.

## Scope from the actual starting point

The recorded Chapter 10 main.cpp already contains Tensor-level autograd,
broadcast arithmetic, matmul/sum backward, ReLU, sigmoid, tanh and working
linear/nonlinear training examples. Its ending promises linear and activation
modules plus a first multilayer perceptron. Do not rebuild Tensor or scalar
autograd. Keep MNIST, data loaders, softmax/cross-entropy and CUDA outside this
10-15-minute episode.

Build a small 2-input, 4-hidden-unit, 1-output network and train it on the four
XOR cases. Reuse mean squared error for this controlled fit; it is not a claim
that MSE is the preferred classification loss. Use a linear output, threshold
at 0.5 only when interpreting the final values, not inside the training graph.

## Sources and observed language

- [YouTube: Building a Neural Network from Scratch: The XOR Problem Animation](https://www.youtube.com/watch?v=A9EmBsgsMlI): title and description use neural network, XOR, MLP and decision boundary.
- [YouTube: Solving the XOR Problem with PyTorch](https://www.youtube.com/watch?v=KAipbKHYNcc): independent example of the XOR/neural-network phrasing. Our implementation does not use PyTorch.
- [Author's C++ neural-network repository](https://github.com/oktonion/neural-network-from-scratch-in-cpp): C++, neural network from scratch and XOR appear together. This establishes vocabulary, not market demand.
- [PyTorch C++ frontend tutorial](https://docs.pytorch.org/tutorials/advanced/cpp_frontend.html): primary terminology reference for modules, forward, parameters and composition. We are not reproducing its registration/ownership framework.
- [PyTorch Linear reference](https://docs.pytorch.org/docs/2.14/generated/torch.nn.Linear.html): input/output feature terminology and bounded random initialization. Our weight layout stays input-features by output-features, matching our existing matmul without a transpose.
- [Stanford CS231n architecture notes](https://cs231n.github.io/neural-networks-1/): fully connected layers, nonlinearities and network composition.
- [Stanford CS231n training notes](https://cs231n.github.io/neural-networks-2/): avoid identical weight initialization across hidden units; normalize initialization scale. We use a simple fan-in-scaled uniform distribution, not a claim of optimal initialization.

No search volume, current YouTube autocomplete, owned query demand or ranking
difficulty was available. Do not label this an SEO opportunity score.

## Selection

Primary phrase: neural network from scratch in C++.

Supporting: multilayer perceptron, MLP, linear layer, hidden layer, activation
function, Tensor, autograd, backpropagation, gradient descent, weight
initialization, XOR.

Working title: Building Our First Neural Network in C++ | Deep Learning, All the Way Down #11

Reject for this episode: MNIST classifier, image recognition, GPU training,
CUDA, PyTorch replacement, production framework, Sequential container, generic
module registry. No artificial repetition of the selected words.

## Spoken-keyword map

| Term | Spoken placement |
| --- | --- |
| neural network, C++, XOR | Cold opening: teach a network the four XOR cases in C++. |
| linear layer, module | Group a weight matrix, bias and forward operation into Linear. |
| weight initialization | Give hidden units different starting weights before training. |
| hidden layer, activation function, MLP | Connect Linear, Tanh, Linear into a multilayer perceptron. |
| parameters, gradients | Collect the four parameter Tensors for resets and updates. |
| backpropagation, autograd | Existing loss.backward follows all the composed operations. |
| gradient descent | Apply the general parameter update in the full-batch training loop. |
| MNIST | Closing destination only, no claim it was loaded or trained here. |

## Evidence-led scope

[Long-form retention comparison](../analytics/reports/2026-08-29-long-form-retention-comparison-episodes-01-06.md)
shows repeated opening losses and navigation toward concrete implementation.
Start with four visible cases, move into useful code inside 30 seconds, avoid a
series recap, and introduce each abstraction when the next edit uses it.
The creator's 10-15-minute limit and preference for natural transitions are
editorial constraints, not measured optimal durations. No Shorts controversy,
mandatory question structure or rapid-cut pacing is imported.

