# Episode 4 - Matrix Multiplication in C++

## Video brief

- **Working title:** Building Matrix Multiplication in C++: Predicting a Whole
  Batch at Once | Deep Learning, All the Way Down #4
- **Target runtime:** 6-9 minutes. Not padded to hit a bigger number — this is
  a one-mechanism episode, and it's a short mechanism.
- **Viewer promise:** run one matrix multiplication across a batch of
  observations and get a real batch of predictions back, then see exactly why
  adding the bias still isn't clean
- **Starting point:** the final Episode 3 `main.cpp`
- **Only code file:** `main.cpp`
- **Deferred to Episode 5:** broadcasting — this episode ends on the copied
  bias being wasteful, not on the fix
- **Deferred further out:** stored tensor strides, offsets, zero-copy views,
  rank-N batched matrix multiplication, optimized kernels, autograd, dtypes,
  dependencies, and build tooling

## 00:00-00:35 - From one observation to a batch

### On screen

Begin speaking immediately with
[`assets/observation-to-prediction.png`](assets/observation-to-prediction.png).

Keep it visible through the first sentence. On "stack several observations,"
switch to
[`assets/observations-to-predictions.png`](assets/observations-to-predictions.png).

### Narration

> Welcome back to *Deep Learning, All the Way Down*.
>
> So right now, if you give this thing one observation, it does one dot
> product, adds the bias, and hands you back one prediction. But normally you
> don't want to do that one observation at a time, you want to stack a bunch
> of them into a matrix and run all of them through the same weights at once.
> And once you do that, the dot product isn't a dot product anymore, it's
> matrix multiplication. And since every row is using the exact same bias, at
> some point we're going to need a way to reuse that one value instead of
> copying it everywhere, and that's broadcasting.
>
> Let's get the batch working first. Here's what happens when we just hand
> our `dot()` a matrix.

---

## 00:35-01:20 - Let the current tensor fail

### Live coding

At the bottom of `main()`, remove the Episode 3 prediction demo beginning with:

```cpp
// features = [4.0, 3.0, 2.0]
```

Remove that block through the old `"Success!"` print, but keep `return 0;`.
Replace it with:

```cpp
const Tensor inputs(
    {2, 3},
    {
        1.0, 2.0, 3.0,
        4.0, 5.0, 6.0
    }
);

const Tensor weights(
    {3, 2},
    {
        1.0, 0.0,
        0.0, 1.0,
        1.0, 1.0
    }
);

const Tensor invalid = inputs.dot(weights);
```

Compile and run.

```text
dot requires two rank-one tensors
```

Delete the deliberate failure before continuing.

### Narration

> Yeah, that's the right call. A vector dot product doesn't have an output
> coordinate at all, it just collapses down to one number. But here, every
> spot in the output needs its own row from the left matrix and its own
> column from the right, and those two get dotted together.

### On screen

```text
left  [m,k]
right   [k,n]
        └─┘ shared dimension

output [m,n]
```

\[
C_{i,j} = \sum_{r=0}^{k-1} A_{i,r}B_{r,j}
\]

---

## 01:20-04:00 - Implement matrix multiplication

### Narration

> One small thing before we get into matmul itself. It needs to allocate its
> output, so I'm just pulling that overflow-safe element count we already
> wrote into its own helper instead of copy-pasting it in again.

### Live coding

Add this private helper:

```cpp
[[nodiscard]] static std::size_t checked_numel(
    const std::vector<std::size_t>& shape
) {
  for (const std::size_t dimension : shape) {
    if (dimension == 0) {
      return 0;
    }
  }

  std::size_t result = 1;

  for (const std::size_t dimension : shape) {
    if (
        result >
        std::numeric_limits<std::size_t>::max() / dimension
    ) {
      throw std::overflow_error(
          "tensor element count overflows size_t"
      );
    }

    result *= dimension;
  }

  return result;
}
```

Replace the constructor's inline element-count calculation with a call to
`checked_numel(shape_)`. No semantics changed; construction and matmul now
share one checked definition.

Add the public operation:

```cpp
[[nodiscard]] Tensor matmul(const Tensor& other) const {
  if (rank() != 2 || other.rank() != 2) {
    throw std::invalid_argument(
        "matmul requires two rank-two tensors"
    );
  }

  const std::size_t rows = shape_[0];
  const std::size_t inner = shape_[1];
  const std::size_t other_inner = other.shape_[0];
  const std::size_t columns = other.shape_[1];

  if (inner != other_inner) {
    throw std::invalid_argument(
        "matmul inner dimensions must match"
    );
  }

  const std::vector<std::size_t> result_shape{
      rows,
      columns
  };

  std::vector<double> result_data(
      checked_numel(result_shape),
      0.0
  );
```

### Narration

> So `rows` comes from the left matrix, `columns` comes from the right, and
> the two of them have to agree on whatever's in the middle, that's the
> length of the dot product.

Continue inside `matmul()`:

```cpp
  for (std::size_t row = 0; row < rows; ++row) {
    for (
        std::size_t column = 0;
        column < columns;
        ++column
    ) {
      double sum = 0.0;

      for (
          std::size_t index = 0;
          index < inner;
          ++index
      ) {
        sum +=
            data_[row * inner + index] *
            other.data_[index * columns + column];
      }

      result_data[row * columns + column] = sum;
    }
  }

  return Tensor(
      result_shape,
      std::move(result_data)
  );
}
```

### Narration

> The two outer loops are just picking one output row and one output column.
> The inner loop is what's actually computing the dot product that lands
> there. And because we're still contiguous row-major, `[row,index]` works
> out to `row * inner + index`, and `[index,column]` works out to
> `index * columns + column`.

### Verify immediately

```cpp
const Tensor linear = inputs.matmul(weights);

assert((
    linear.shape() ==
    std::vector<std::size_t>{2, 2}
));

assert((
    linear.data() ==
    std::vector<double>{4.0, 5.0, 10.0, 11.0}
));
```

### On screen

```text
inputs.matmul(weights)

[
  [ 4,  5],
  [10, 11]
]
```

### Narration

> And matrix multiplication works. Every input row is producing its own
> output vector now. The only thing left is one bias per output column.

---

## 04:00-04:50 - Make the layer work by copying the bias

### Live coding

```cpp
const Tensor expanded_bias(
    {2, 2},
    {
        10.0, -10.0,
        10.0, -10.0
    }
);

const Tensor copied_predictions =
    linear + expanded_bias;

assert((
    copied_predictions.data() ==
    std::vector<double>{14.0, -5.0, 20.0, 1.0}
));
```

### On screen

```text
[
  [ 4,  5],       [10, -10]       [14, -5],
  [10, 11]    +   [10, -10]   =   [20,  1]
]
```

### Narration

> Okay, that's the right answer, but look at what we just did to get it.
> Those two bias values are identical on every single row, and we copied them
> into a whole matrix just so addition would accept two equal shapes.
> Broadcasting is going to let the smaller tensor describe that reuse
> directly, without us ever copying anything.

---

## 04:50-05:30 - Review and next episode

### On screen

```text
inputs      [observations, input_features]
weights     [input_features, outputs]
bias        [outputs] -- only works today if copied

rank-two dot failure -> matrix multiplication -> a real batch of predictions
        -> bias only works if we copy it
```

### Narration

> So that's the episode. The rank-two dot failure turned into matrix
> multiplication, and that's giving us a real batch of predictions in one
> shot, no per-row loop on our end, it just falls out of the shapes.
>
> The one thing that's not clean yet is the bias — it only works right now
> because we copied it into a full matrix. Next time we fix that:
> broadcasting, so the bias describes its own reuse instead of us copying it
> anywhere.

---

## 05:30-06:00 - Questions for Episode 5

### Narration

> Three questions. Answers in the pinned comment.

1. In `[m,k] @ [k,n]`, why must `k` match, and why does it disappear from the
   output shape?
2. The bias we copied into a full matrix has the exact same values on every
   row. What's the actual cost of that copy, and what would you want a
   smarter version to do instead?
3. Our indexing formulas in `matmul()` assume contiguous row-major storage on
   both operands. What would break if one of them were a transposed view
   instead?

End the episode after the questions.
