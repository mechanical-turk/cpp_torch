# Episode 6 - Mean Squared Error

## Video brief

- **Title:** Building Mean Squared Error from Scratch in C++ | Deep Learning, All the Way Down #6
- **Target runtime:** 8-10 minutes
- **Viewer promise:** take a batch of predictions and reduce its mistakes to one scalar loss using tensor operations we already built.
- **Starting point:** `/Users/keremkazan/Documents/Projects/deep-learning-all-the-way-down/main.cpp` at commit `79461fb` (`chapter 05 - broadcasting`). The file ends with `pred_23`, a `[2,1]` tensor containing `{3.5, 0.0}`.
- **Only code file:** `main.cpp`
- **In scope:** residuals, squared error, `mean()`, the empty-mean contract, and a free `mse_loss()` function.
- **Deferred:** gradients, automatic differentiation, parameter updates, optimizers, loss reductions along selected axes, and other loss functions.

---

## 00:00-00:35 - A prediction is not good or bad by itself

### Visual

Show [`assets/prediction-with-cancelling-residuals.png`](assets/prediction-with-cancelling-residuals.png) while discussing it. Do not reveal the final loss yet.

### Narration

> Welcome back to *Deep Learning, All the Way Down.
>
> Our tensor can now produce these two predictions: `3.5` and `0.0`. But neither number is good or bad by itself. If those are the values we wanted, the model got everything right. If we wanted `2.5` and `1.0`, it did terribly.
>
> A prediction only becomes measurable once we compare it with a target. Today we're going to make that comparison, turn every mistake into a number, and reduce the whole batch to one scalar loss.

Move directly into `main.cpp`.

---

## 00:35-01:35 - Compute the residuals

### Narration

> We already have `pred_23`, with shape `[2,1]`. Let's give those two predictions targets of `2.5` and `1.0`.

### Live coding

Add this immediately after the existing `pred_23` assertions:

```cpp
const Tensor targets(
  {2, 1},
  {
    2.5,
    1.0
  }
);

const Tensor residuals = pred_23 - targets;

assert(residuals.shape() == std::vector<std::size_t>{2, 1});
assert(residuals.data() == std::vector<double>{1.0, -1.0});
```

### Narration

> The difference between a prediction and its target is called a residual. Our first prediction is one unit too high, so its residual is `1.0`. The second is one unit too low, so its residual is `-1.0`.
>
> We can already calculate them with tensor subtraction. Now let's try the simplest way to turn them into one number.

---

## 01:35-02:30 - The first measurement fails

### Visual

```cpp
const Tensor residual_total = residuals.sum();

assert(residual_total.at({}) == 0.0);
```

### Narration

> The sum is zero. If we treated that as our loss, we'd be claiming the predictions were perfect.
>
> But we can see what happened. The residuals were `1.0` and `-1.0`, so they cancelled each other. The model made two mistakes in opposite directions, and their signs hid both of them.
>
> Squaring removes the sign. Both residuals become `1.0`, zero would stay zero, and larger misses would contribute more heavily than smaller ones.

### Live coding

```cpp
const Tensor squared_residuals = residuals * residuals;

assert(
    squared_residuals.data() ==
    std::vector<double>{1.0, 1.0}
);
```

### Narration

> Elementwise multiplication already gives us the square. We don't need another traversal or a special square operator.

---

## 02:30-03:30 - Why the sum is not enough

### Live coding

```cpp
const Tensor total_squared_error = squared_residuals.sum();

assert(total_squared_error.rank() == 0);
assert(total_squared_error.at({}) == 2.0);
```

### Narration

> Summing the squares gives us `2.0`, but it creates another problem. If we duplicated this batch, we'd have four equally accurate predictions and the total would double from `2.0` to `4.0`.
>
> The model didn't get worse. We only measured more observations.
>
> We want the typical squared residual, so we divide the total by the number of values. That gives us the mean squared error.

### On screen

```text
2 residuals:  1.0 + 1.0             sum = 2.0
4 residuals:  1.0 + 1.0 + 1.0 + 1.0  sum = 4.0

same squared error per prediction, different totals
```

---

## 03:30-05:00 - Add a `mean()` reduction

### Narration

> `mean()` is a general tensor reduction, just like `sum()`, so it belongs on `Tensor`.
>
> Before we write it, we need to decide what an empty mean means. The sum of an empty tensor is naturally zero because zero is the additive identity. A mean asks us to divide that sum by the number of values. For an empty tensor, that would be zero divided by zero, so there is no valid result. We'll reject it explicitly.

### Live coding

Add this public member beside `sum()`:

```cpp
[[nodiscard]] Tensor mean() const {
  if (numel() == 0) {
    throw std::invalid_argument(
        "mean is undefined for an empty tensor"
    );
  }

  const double scale =
      1.0 / static_cast<double>(numel());

  return sum() * Tensor({}, {scale});
}
```

### Narration

> `sum()` produces a scalar tensor. We multiply that scalar by the reciprocal of the element count.
>
> The cast makes the conversion from `size_t` to `double` explicit. With two values, `scale` is `0.5`, so the total squared error of `2.0` becomes a mean of `1.0`.

### Live coding

```cpp
const Tensor mean_squared_error = squared_residuals.mean();

assert(mean_squared_error.rank() == 0);
assert(mean_squared_error.at({}) == 1.0);
```

Run the program and confirm that the assertions pass.

---

## 05:00-06:20 - Compose the complete loss function

### Narration

> We now have the whole calculation spread across `main`: subtract, square, and take the mean. Let's give that composition a name.
>
> Mean squared error is a machine-learning operation built from tensors. It isn't a fundamental behavior every tensor must own, so we'll keep it outside the class as a free function.

### Live coding

Add this after the `Tensor` class and before `main()`:

```cpp
[[nodiscard]] Tensor mse_loss(
    const Tensor& prediction,
    const Tensor& target
) {
  if (prediction.shape() != target.shape()) {
    throw std::invalid_argument(
        "mse_loss requires equal shapes"
    );
  }

  const Tensor residual = prediction - target;
  return (residual * residual).mean();
}
```

### Narration

> The function requires predictions and targets to have exactly the same shape. Broadcasting is useful for arithmetic like adding one bias to every row, but silently broadcasting a target could hide a mistake in the training data.
>
> After that check, the implementation is the definition: subtract the target, square each residual, and take the mean.
>
> There are no indexing loops here. The loss function is built by composing operations whose traversal rules already live inside `Tensor`.

---

## 06:20-07:30 - Replace the manual calculation

### Live coding

Keep the intermediate assertions as the derivation, then verify the composed function:

```cpp
const Tensor loss = mse_loss(pred_23, targets);

assert(loss.rank() == 0);
assert(loss.at({}) == 1.0);
```

Add a zero-loss case:

```cpp
const Tensor perfect_loss = mse_loss(pred_23, pred_23);
assert(perfect_loss.at({}) == 0.0);
```

And verify the empty-mean contract:

```cpp
bool rejected_empty_mean = false;

try {
  static_cast<void>(Tensor({0}, {}).mean());
} catch (const std::invalid_argument&) {
  rejected_empty_mean = true;
}

assert(rejected_empty_mean);
```

Run the program.

### Narration

> Our residuals are `1.0` and `-1.0`. Their plain sum is zero, but squaring gives us `1.0` and `1.0`, and their mean is `1.0`.
>
> Comparing the predictions with themselves produces zero, and asking for the mean of no values throws instead of quietly producing a `NaN`.

---

## 07:30-08:30 - Review and next step

### On screen

```text
What we covered

- residuals: prediction - target
- squared error: residual * residual
- mean() as a tensor reduction
- the empty-mean contract
- mse_loss() composed from tensor operations
- a rank-zero loss tensor
```

### Narration

> We covered residuals, squared error, the `mean()` reduction and its empty-tensor contract, and composed them into `mse_loss()`, which returns a rank-zero tensor.

Replace the recap with:

```text
Next episode

- computation graphs
- local derivatives
- backward gradient propagation
```

### Narration

> Next, we'll trace that loss backward and calculate how each input contributed to it. That's where automatic differentiation begins.

---

## Questions

### Narration

> Now, as always, I'll share a few questions for you to ponder before the next episode. You can read the answers in the pinned comment.

1. Why can signed residuals not simply be
   summed to measure the model's total error?

2. Why is the sum of an empty tensor zero
   while its mean is undefined?

3. Why does `mean()` belong on `Tensor`, while
   `mse_loss()` works better as a free function?

Read each question aloud, leaving enough time for it to be read on screen.

### Sign-off

> That brings us to the end of this episode. Thanks for watching, and I will see you next time.

Replace the questions with a clean end-screen background and hold it for approximately five seconds. Place the YouTube Subscribe and complete-series-playlist elements only over this tail.
