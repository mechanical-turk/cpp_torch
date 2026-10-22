# Chapter 14 keyword research

Prepared October 4, 2026. The searches below were run before the narration was
written, after the creator chose the scope (a layer-by-layer gradient report,
residual connections, and a deeper network that trains) and after the edit
sequence had been prototyped against the Chapter 13 source.

## Scope from the actual starting point

The Chapter 13 final source (the verifier's frozen baseline) trains a
Sequence of explicitly listed Linear and Tanh layers on MNIST with eight hidden
layers, a decaying learning rate, and 5 epochs. It has no way to look inside the
network, and a network deeper than about eight layers cannot be trained with it.

This episode adds, in order: a traced forward pass and a printed report of the
signal size and gradient size at every layer; the same network at sixteen hidden
layers, built with a `hidden_layer` helper (a `Sequence` is itself a `Layer`),
which does not train; a `Residual` layer that adds its input to a body layer's
output, which does. Keep momentum, velocity, Adam, more training data,
regularization, initialization schemes, normalization and attention out of this
episode. Training on more data and optimizers are named only in the closing list.

## Sources and observed language

- [Aman.ai: Residual/Skip Connections](https://aman.ai/primers/ai/residual-connections/),
  [AI Summer: skip connections](https://theaisummer.com/skip-connections/) and
  [DeepAI: Residual Connections](https://deepai.org/machine-learning-glossary-and-terms/residual-connections):
  "residual connections" and "skip connections" are interchangeable terms; the
  usual account is that addition lets the gradient pass through the identity
  path, so it is multiplied by one in earlier layers. The script uses
  "residual connection" as the primary term and shows the gradient report as
  evidence instead of asserting the account.
- [He, Zhang, Ren and Sun, Deep Residual Learning for Image Recognition (2015)](https://arxiv.org/pdf/1512.03385v1):
  the original source for recasting a layer as F(x) + x with identity shortcuts.
  The script does not discuss ResNet, ImageNet or the paper's degradation
  argument.
- [Neptune and others on monitoring gradient norms per layer](https://neptune.ai/?p=47645),
  [MathWorks: detect vanishing gradients](https://www.mathworks.com/help/deeplearning/ug/detect-vanishing-gradients-in-deep-neural-networks.html):
  the standard diagnostic is the gradient magnitude at every layer, with early
  layers 1000 times smaller than later ones given as a red flag. This supports
  the report as a real practice, not an invented trick. Those pages use
  framework hooks; the episode writes the same measurement by hand.
- Vocabulary check: "vanishing gradient" is the established name for the
  effect. "Signal" is used in the script for the typical size of a layer's
  output values, defined on screen as a root mean square.

No search volume, YouTube autocomplete, owned query demand or ranking
difficulty was available in this pass. Do not label this an SEO opportunity
score. No comparable hand-built C++ residual-connection video was located, which
supports novelty only, not demand.

## Selection

Primary phrase: residual connections in C++.

Supporting: debugging gradients, vanishing gradient, deeper neural network,
neural network in C++, MNIST, layers, signal and gradient.

Working title: Residual Connections and Debugging Gradients in C++ | Deep Learning, All the Way Down #14

Reject for this episode: skip connections as a lead term (kept as a natural
synonym only if it fits), ResNet, "from scratch" without a named capability,
exploding gradient (the residual network shows a larger starting signal, but we
do not study it), batch or layer normalization, He or Xavier initialization,
overfitting as a lead term (the closing beat mentions the train and test gap
only), momentum, Adam, optimizer.

## Spoken-keyword map

| Term | Where it is spoken |
| --- | --- |
| C++ neural network, MNIST | Cold open, first sentence. |
| debugging gradients | Cold open, fourth sentence ("a tool for debugging gradients"). |
| layer by layer, signal, gradient | Section A, where `print_signal` is written and its first table is read. |
| vanishing gradient | Section B, immediately after the sixteen-layer table and the explanation of why the gradient shrinks. |
| residual connection | Cold open and Section C, where the idea is stated and the `Residual` layer is written. |
| deeper network, sixteen layers | Sections B and C, around the two sixteen-layer runs. |

## Evidence-led scope

[Long-form retention comparison](../analytics/reports/2026-08-29-long-form-retention-comparison-episodes-01-06.md)
shows repeated opening losses and movement toward concrete implementation. The
episode names the network, dataset and plan in the first two sentences and
starts code within about 30 seconds. The 10-15 minute target is an editorial
constraint from the long-form playbook, not a measured optimum. No newer
long-form retention data was consulted for this script.
