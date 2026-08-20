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
> Right now, if you give this thing one observation, it does one dot
> product, adds the bias, and hands you back one prediction. But normally you
> don't want to do that one observation at a time, you want to stack a bunch
> of them

Switch to new image

>  into a matrix and run all of them through the same weights at once.

> And once you do that, your core process evolves from a single dot product into 
> matrix multiplication. And since every row is using the exact same bias, at
> some point we're going to need a way to reuse that one value instead of
> copying it everywhere, and that's broadcasting.
>
> Let's get the batch working first. 
> 
> Here's what happens when we just hand
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

> Suppose we have 2 observations
> And suppose each observation has 3 features

> That set of observations can be expressed as a 2 by matrix
> Each row represents one observation
> Each column represents one feature

```cpp
const Tensor inputs(
    {2, 3},
    {
        4.0, 3.0, 2.0,
        1.0, 2.0, 0.5
    }
);

const Tensor weights(
    {3, 1},
    {
        0.5,
        -1.0,
        2.0
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

### Live coding

Add the public operation:

```cpp
[[nodiscard]] Tensor matmul(const Tensor& other) const {
  if (rank() != 2 || other.rank() != 2) {
    throw std::invalid_argument("matmul requires two rank-two tensors");
  }

  const std::size_t left_rows = shape_[0];
  const std::size_t left_cols = shape_[1];
  const std::size_t right_rows = other.shape_[0];
  const std::size_t right_cols = other.shape_[1];

  if (left_cols != right_rows) {
    throw std::invalid_argument("matmul inner dimensions must match");
  }

  const std::vector<std::size_t> result_shape{
      left_rows,
      right_cols
  };

  std::vector<double> result_data(
      left_rows * right_cols,
      0.0
  );
```

### Narration

> The result keeps the number of rows from the left matrix and the number of
> columns from the right matrix. The two inner dimensions have to match,
> because they determine the length of every dot product we're about to do.

### On screen

```text
inputs                  weights          result

[ 4.0  3.0  2.0 ]      [  0.5 ]         [  3.0 ]
[ 1.0  2.0  0.5 ]  @   [ -1.0 ]    =    [ -0.5 ]
                         [  2.0 ]

result[0,0] = [4.0, 3.0, 2.0] dot [0.5, -1.0, 2.0] = 3.0
result[1,0] = [1.0, 2.0, 0.5] dot [0.5, -1.0, 2.0] = -0.5
```

### Narration

> Before we write the loops, let's make the actual job clear. To produce one
> value in the result, we take one row from the left matrix and one column
> from the right matrix, then compute their dot product. The output coordinate
> tells us exactly which row and which column to use.
>
> In this example the weights only have one column, so the result only has one
> column. The first output value is the first input row dotted with the weights,
> and the second output value is the second input row dotted with those same
> weights.

> This is the same basic idea as a stride. Every output row contains right_cols values, so moving to the next row means skipping right_cols elements. row * right_cols skips all the complete rows before the one we want, and adding column moves to the correct position inside that row.

Continue inside `matmul()`:

```cpp
  for (std::size_t row = 0; row < left_rows; ++row) {
    for (
        std::size_t column = 0;
        column < right_cols;
        ++column
    ) {
      double sum = 0.0;

      for (
          std::size_t index = 0;
          index < left_cols;
          ++index
      ) {
        sum +=
            at({row, index}) *
            other.at({index, column});
      }

      result_data[row * right_cols + column] = sum;
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
> there. Using `at()` makes that relationship explicit: read one value from
> the selected row on the left, read the corresponding value from the selected
> column on the right, multiply them, and add the product to the running sum.
>
> Once that dot product is finished, we still need to place it into the flat
> output storage. This is the same basic idea as a stride. Every output row
> contains `right_cols` values, so moving to the next row means skipping
> `right_cols` elements. `row * right_cols` skips all the complete rows before
> the one we want, and adding `column` moves to the correct position inside
> that row.

### Verify immediately

```cpp
const Tensor linear = inputs.matmul(weights);

assert((
    linear.shape() ==
    std::vector<std::size_t>{2, 1}
));

assert((
    linear.data() ==
    std::vector<double>{3.0, -0.5}
));
```

### On screen

```text
inputs.matmul(weights)

[
  [ 3.0],
  [-0.5]
]
```

### Narration

> And matrix multiplication works. Every input row is producing its own
> prediction now. This version is easy to read, but `at()` does more work than
> we need inside
> the hottest loop. Every lookup constructs an index vector, checks it, and
> converts the two-dimensional coordinate into a flat storage index.
>
> We already checked both ranks and the inner dimensions before entering the
> loops, and our tensor is still stored contiguously in row-major order. So we
> can compute those flat indices directly here.

Replace the accumulation inside the innermost loop:

```cpp
        sum +=
            data_[row * left_cols + index] *
            other.data_[index * right_cols + column];
```

### Narration

> On the left, `[row,index]` maps to `row * left_cols + index`. On the right,
> `[index,column]` maps to `index * right_cols + column`. The calculation is
> unchanged; we've just removed the temporary index vectors and repeated
> checked lookups from the inner loop.
>
> Matrix multiplication is done. The only thing left is the bias.

---

## 04:00-04:50 - Make the layer work by copying the bias

### Live coding

```cpp
const Tensor expanded_bias(
    {2, 1},
    {
        0.5,
        0.5
    }
);

const Tensor copied_predictions =
    linear + expanded_bias;

assert((
    copied_predictions.data() ==
    std::vector<double>{3.5, 0.0}
));
```

### On screen

```text
[ 3.0]      [0.5]      [3.5]
[-0.5]  +   [0.5]  =   [0.0]
```

### Narration

> Okay, that's the right answer, but look at what we just did to get it.
> That's the exact same bias value on every row, and we copied it into a
> whole column just so addition would accept two equal shapes. Broadcasting
> is going to let the smaller tensor describe that reuse directly, without
> us ever copying anything.

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
