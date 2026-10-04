# MNIST MLP comparison: measured results

Seven configurations, 15 epochs, 10,000 training images and 2,000 validation images.
Validation records come from the original training split. No official test data was used for selection.

## Main comparison

Initialization seed 42. All reported train/validation metrics use the final epoch-15 weights.

| Hidden layers | Activation | LR | Shuffle | Parameters | Train accuracy | Validation accuracy | Gap (pp) | Train loss | Validation loss | Seconds |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 32 | tanh | 0.1 | No | 25,450 | 95.97% | 94.15% | 1.82 | 0.1496 | 0.2266 | 15.5 |
| 32 | tanh | 0.1 | Yes | 25,450 | 96.16% | 94.00% | 2.16 | 0.1423 | 0.2211 | 17.0 |
| 128 | tanh | 0.1 | Yes | 101,770 | 96.21% | 93.85% | 2.36 | 0.1398 | 0.2233 | 67.5 |
| 128 | tanh | 0.03 | Yes | 101,770 | 92.98% | 92.00% | 0.98 | 0.2563 | 0.2863 | 67.6 |
| 128 | relu | 0.1 | Yes | 101,770 | 97.25% | 94.45% | 2.80 | 0.1061 | 0.1985 | 66.5 |
| 128 + 64 | relu | 0.1 | Yes | 109,386 | 98.83% | 95.30% | 3.53 | 0.0517 | 0.1640 | 69.4 |
| 128 + 64 | tanh | 0.1 | Yes | 109,386 | 97.55% | 94.40% | 3.15 | 0.0959 | 0.1940 | 69.8 |

The gap is train accuracy minus validation accuracy. Timing includes evaluation and is not a clean performance benchmark.

## Initialization sensitivity

Selected by lowest epoch-15 validation loss in the initial sweep: **deep-128-64-relu**.
Only the baseline and selected model were repeated with seed 43.

| Model | Seed | Train accuracy | Validation accuracy | Gap (pp) | Validation loss |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline-32-tanh | 42 | 95.97% | 94.15% | 1.82 | 0.2266 |
| deep-128-64-relu | 42 | 98.83% | 95.30% | 3.53 | 0.1640 |
| baseline-32-tanh | 43 | 96.08% | 93.25% | 2.83 | 0.2219 |
| deep-128-64-relu | 43 | 98.60% | 94.95% | 3.65 | 0.1676 |

## Learning checkpoints

Training loss is evaluated after the epoch at fixed weights, not averaged while the weights change.

| Model | Seed | Epoch | Train loss | Validation loss | Train accuracy | Validation accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline-32-tanh | 42 | 1 | 0.5142 | 0.5089 | 87.80% | 87.60% |
| baseline-32-tanh | 42 | 5 | 0.2604 | 0.2943 | 92.65% | 91.65% |
| baseline-32-tanh | 42 | 10 | 0.1908 | 0.2490 | 94.74% | 93.40% |
| baseline-32-tanh | 42 | 15 | 0.1496 | 0.2266 | 95.97% | 94.15% |
| shuffle-32-tanh | 42 | 1 | 0.5041 | 0.4997 | 88.35% | 88.30% |
| shuffle-32-tanh | 42 | 5 | 0.2540 | 0.2911 | 92.87% | 92.05% |
| shuffle-32-tanh | 42 | 10 | 0.1904 | 0.2443 | 94.68% | 93.10% |
| shuffle-32-tanh | 42 | 15 | 0.1423 | 0.2211 | 96.16% | 94.00% |
| wide-128-tanh | 42 | 1 | 0.4464 | 0.4383 | 88.66% | 89.10% |
| wide-128-tanh | 42 | 5 | 0.2543 | 0.2900 | 92.76% | 91.50% |
| wide-128-tanh | 42 | 10 | 0.1878 | 0.2475 | 94.59% | 92.90% |
| wide-128-tanh | 42 | 15 | 0.1398 | 0.2233 | 96.21% | 93.85% |
| wide-128-tanh-lr003 | 42 | 1 | 0.9222 | 0.9079 | 81.87% | 81.30% |
| wide-128-tanh-lr003 | 42 | 5 | 0.3733 | 0.3770 | 90.05% | 90.40% |
| wide-128-tanh-lr003 | 42 | 10 | 0.2946 | 0.3108 | 92.02% | 91.10% |
| wide-128-tanh-lr003 | 42 | 15 | 0.2563 | 0.2863 | 92.98% | 92.00% |
| wide-128-relu | 42 | 1 | 0.4384 | 0.4259 | 88.76% | 88.60% |
| wide-128-relu | 42 | 5 | 0.2358 | 0.2805 | 93.21% | 91.95% |
| wide-128-relu | 42 | 10 | 0.1580 | 0.2281 | 95.66% | 93.45% |
| wide-128-relu | 42 | 15 | 0.1061 | 0.1985 | 97.25% | 94.45% |
| deep-128-64-relu | 42 | 1 | 0.5152 | 0.4986 | 85.62% | 85.65% |
| deep-128-64-relu | 42 | 5 | 0.2190 | 0.2784 | 93.49% | 91.85% |
| deep-128-64-relu | 42 | 10 | 0.1151 | 0.2062 | 96.75% | 94.30% |
| deep-128-64-relu | 42 | 15 | 0.0517 | 0.1640 | 98.83% | 95.30% |
| deep-128-64-tanh | 42 | 1 | 0.4767 | 0.4762 | 88.35% | 88.55% |
| deep-128-64-tanh | 42 | 5 | 0.2293 | 0.2770 | 93.29% | 91.85% |
| deep-128-64-tanh | 42 | 10 | 0.1546 | 0.2307 | 95.75% | 93.10% |
| deep-128-64-tanh | 42 | 15 | 0.0959 | 0.1940 | 97.55% | 94.40% |
| baseline-32-tanh | 43 | 1 | 0.5425 | 0.5357 | 87.28% | 87.45% |
| baseline-32-tanh | 43 | 5 | 0.2616 | 0.2918 | 92.74% | 91.70% |
| baseline-32-tanh | 43 | 10 | 0.1907 | 0.2456 | 94.72% | 92.75% |
| baseline-32-tanh | 43 | 15 | 0.1488 | 0.2219 | 96.08% | 93.25% |
| deep-128-64-relu | 43 | 1 | 0.5448 | 0.5260 | 83.96% | 83.85% |
| deep-128-64-relu | 43 | 5 | 0.2152 | 0.2743 | 93.83% | 92.00% |
| deep-128-64-relu | 43 | 10 | 0.1191 | 0.2050 | 96.54% | 94.30% |
| deep-128-64-relu | 43 | 15 | 0.0571 | 0.1676 | 98.60% | 94.95% |

## Boundaries

- These are validation results, not the earlier 88.2% test-subset result.
- More training data, other initializers, Adam, momentum, regularization and augmentation were not compared.
- One split and limited seed repeats do not establish a universal architecture ranking.
- An accuracy gap alone does not demonstrate deterioration from overfitting. Inspect whether validation loss rises as training loss falls.
- All experiments use the actual C++ Tensor/autograd engine with normal -O2.

[Protocol and source context](README.md) · [Raw measurements](results.json)
