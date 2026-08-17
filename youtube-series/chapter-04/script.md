# Episode 4 - Building a Linear Layer in C++

## Video brief

- **Working title:** Building a Linear Layer in C++: Matmul & Broadcasting |
  Deep Learning, All the Way Down #4
- **Target runtime:** 23-27 minutes
- **Viewer promise:** run one linear transformation across a batch with
  `inputs.matmul(weights) + bias`
- **Starting point:** the final Episode 3 `main.cpp`
- **Only code file:** `main.cpp`
- **Deferred:** stored tensor strides, offsets, zero-copy views, rank-N batched
  matrix multiplication, optimized kernels, autograd, dtypes, dependencies, and
  build tooling

## 00:00-00:45 - From one observation to a batch

### On screen

Begin speaking immediately with
[`assets/observation-to-prediction.png`](assets/observation-to-prediction.png).

Keep it visible through the first explanation. As the narration says, "Now
stack several observations," switch to
[`assets/observations-to-predictions.png`](assets/observations-to-predictions.png).

### Narration

> Welcome back to *Deep Learning, All the Way Down*, where we rebuild deep
> learning from first principles in modern C++.
>
> Let's start with the simplest case. We have one observation, stored as a
> vector, and one weight for each feature. We take the dot product, add the
> bias, and that gives us one prediction.
>
> But usually we want to run more than one observation at a time. So we stack
> them as rows in a matrix and apply the same weights to every row. Once we do
> that, the dot product turns into matrix multiplication. And because every
> observation uses the same bias, we need to add that one value to every result.
> That reuse is broadcasting.
>
> That is what we are building today. We will get the batch working first, then
> let each observation produce several outputs. Right now, our `dot()` operation
> only accepts vectors, so let's see what happens when we give it a matrix.

---

## 00:45-01:40 - Let the current tensor fail

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

> `dot()` rejects both operands because they have rank two. That is correct: a
> vector dot product chooses no output coordinate and returns one scalar.
>
> Here, each output coordinate chooses one row from the left matrix and one
> column from the right matrix. Their dot product becomes the value stored at
> that coordinate.

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

### Narration

> The left matrix supplies the output rows. The right matrix supplies the
> output columns. The shared dimension is traversed and summed, so it disappears
> from the output shape.

---

## 01:40-02:10 - Reuse the safe element count

### Narration

> Matrix multiplication needs to allocate its output. We already wrote the
> overflow-safe shape-product rule, so I am extracting that existing rule into
> a helper rather than duplicating it.

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

Replace the constructor's inline element-count calculation with:

```cpp
Tensor(
    std::vector<std::size_t> shape,
    std::vector<double> data
)
    : shape_(std::move(shape)),
      data_(std::move(data)) {
  if (checked_numel(shape_) != data_.size()) {
    throw std::invalid_argument(
        "tensor shape does not match its data"
    );
  }
}
```

### Narration

> No tensor semantics changed. Construction and new operations now share one
> checked definition of element count.

---

## 02:10-05:20 - Implement matrix multiplication

### Live coding

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

> These checks give both axes a matrix-specific meaning. `rows` comes from the
> left matrix. `columns` comes from the right. Both operands must agree on the
> length of the row-column dot product.

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

> The outer loops choose one output row and column. The inner loop computes the
> dot product stored there.
>
> Our tensor still owns contiguous row-major storage. The left matrix has
> `inner` values per row, so `[row,index]` maps to
> `row * inner + index`. The right matrix has `columns` values per row, so
> `[index,column]` maps to `index * columns + column`.

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

> Matrix multiplication works. Each input row now produces one output vector.
> We still need one bias value per output column.

---

## 05:20-06:30 - Make the layer work by copying the bias

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

> The linear layer already produces the correct answer. The problem is its
> representation.
>
> The two bias values are identical for every input row, yet we copied them
> into a matrix just to satisfy equal-shape addition. Broadcasting lets the
> smaller tensor describe those repeated reads directly.

---

## 06:30-08:30 - Derive broadcasting from the waste

### On screen

```text
linear  [2,2]
bias      [2]

right-aligned:

linear  [2,2]
bias    [1,2]
```

### Narration

> Broadcasting aligns shapes from the right. The bias has no row axis, so its
> missing leading dimension behaves like size one.
>
> Two aligned dimensions are compatible when they are equal or at least one is
> one. Equal dimensions move together. A size-one dimension has only coordinate
> zero, so its value is reused while the output moves along that axis.

### On screen

```text
output [0,0] -> linear [0,0], bias [0]
output [0,1] -> linear [0,1], bias [1]
output [1,0] -> linear [1,0], bias [0]
output [1,1] -> linear [1,1], bias [1]
```

### Narration

> Moving across output columns advances through both tensors. Moving to another
> output row advances through the matrix but must not move through the bias.

### On screen

```text
output axis               row  column

linear effective stride    2      1
bias effective stride      0      1
```

### Narration

> A stride records how far storage moves when a coordinate increases. An
> effective row stride of zero means changing the output row keeps reading the
> same bias values. Nothing is copied.
>
> These strides exist only during this operation. Making strides part of the
> tensor itself comes next episode.

---

## 08:30-10:30 - Compute the broadcasted shape

### Live coding

Add the header used by `std::max`:

```cpp
#include <algorithm>
```

Add this private helper:

```cpp
[[nodiscard]] static std::vector<std::size_t>
broadcast_shape(
    const std::vector<std::size_t>& left,
    const std::vector<std::size_t>& right
) {
  const std::size_t output_rank =
      std::max(left.size(), right.size());

  std::vector<std::size_t> output(output_rank);

  for (
      std::size_t offset = 0;
      offset < output_rank;
      ++offset
  ) {
    const std::size_t left_dimension =
        offset < left.size()
            ? left[left.size() - 1 - offset]
            : 1;

    const std::size_t right_dimension =
        offset < right.size()
            ? right[right.size() - 1 - offset]
            : 1;

    std::size_t output_dimension = 0;

    if (left_dimension == right_dimension) {
      output_dimension = left_dimension;
    } else if (left_dimension == 1) {
      output_dimension = right_dimension;
    } else if (right_dimension == 1) {
      output_dimension = left_dimension;
    } else {
      throw std::invalid_argument(
          "tensor shapes are not broadcast-compatible"
      );
    }

    output[output_rank - 1 - offset] =
        output_dimension;
  }

  return output;
}
```

### Narration

> `offset` walks from the right edge. If an operand has no axis at that
> position, its missing leading dimension becomes one.
>
> Each aligned pair either agrees, expands a size-one dimension, or rejects the
> operation. We cannot simply take the maximum: zero and one are compatible,
> but their output dimension is zero.

---

## 10:30-13:20 - Describe how each operand is reused

### Live coding

Add ordinary row-major strides:

```cpp
[[nodiscard]] static std::vector<std::size_t>
row_major_strides(
    const std::vector<std::size_t>& shape
) {
  std::vector<std::size_t> strides(
      shape.size(),
      1
  );

  std::size_t stride = 1;

  for (
      std::size_t axis = shape.size();
      axis > 0;
      --axis
  ) {
    const std::size_t current_axis = axis - 1;
    strides[current_axis] = stride;
    stride *= shape[current_axis];
  }

  return strides;
}
```

### Narration

> Shape `[2,2]` produces ordinary strides `[2,1]`. Shape `[2]` produces
> stride `[1]`.

Add effective broadcast strides:

```cpp
[[nodiscard]] static std::vector<std::size_t>
broadcast_strides(
    const std::vector<std::size_t>& input_shape,
    const std::vector<std::size_t>& output_shape
) {
  const std::vector<std::size_t> input_strides =
      row_major_strides(input_shape);

  std::vector<std::size_t> effective_strides(
      output_shape.size(),
      0
  );

  for (
      std::size_t offset = 0;
      offset < input_shape.size();
      ++offset
  ) {
    const std::size_t input_axis =
        input_shape.size() - 1 - offset;

    const std::size_t output_axis =
        output_shape.size() - 1 - offset;

    if (input_shape[input_axis] != 1) {
      effective_strides[output_axis] =
          input_strides[input_axis];
    }
  }

  return effective_strides;
}
```

### Narration

> The effective vector begins at zero. Missing leading axes remain zero.
> Size-one axes also remain zero because their only valid coordinate is zero.
> Every other aligned axis keeps its ordinary row-major stride.

---

## 13:20-15:00 - Traverse the output once

### Live coding

Add a helper that maps one output coordinate through an operand's effective
strides:

```cpp
[[nodiscard]] static std::size_t storage_index(
    const std::vector<std::size_t>& coordinate,
    const std::vector<std::size_t>& strides
) {
  std::size_t index = 0;

  for (
      std::size_t axis = 0;
      axis < coordinate.size();
      ++axis
  ) {
    index += coordinate[axis] * strides[axis];
  }

  return index;
}
```

Add row-major coordinate advancement:

```cpp
static void advance_coordinate(
    std::vector<std::size_t>& coordinate,
    const std::vector<std::size_t>& shape
) {
  for (
      std::size_t axis = shape.size();
      axis > 0;
      --axis
  ) {
    const std::size_t current_axis = axis - 1;
    ++coordinate[current_axis];

    if (coordinate[current_axis] < shape[current_axis]) {
      return;
    }

    coordinate[current_axis] = 0;
  }
}
```

### Narration

> We will traverse one output coordinate space. The same coordinate is dotted
> with two different stride vectors, so it can select different physical values
> from the two operands.
>
> The coordinate advances like an odometer. The rightmost axis changes first,
> then carries into the axis to its left.

---

## 15:00-17:40 - Give every elementwise operation broadcasting

### Live coding

Replace `elementwise_binary()` with:

```cpp
[[nodiscard]] Tensor elementwise_binary(
    const Tensor& other,
    const auto& operation
) const {
  const std::vector<std::size_t> result_shape =
      broadcast_shape(shape_, other.shape_);

  const std::size_t result_numel =
      checked_numel(result_shape);

  if (result_numel == 0) {
    return Tensor(result_shape, {});
  }

  const std::vector<std::size_t> left_strides =
      broadcast_strides(shape_, result_shape);

  const std::vector<std::size_t> right_strides =
      broadcast_strides(other.shape_, result_shape);

  std::vector<std::size_t> coordinate(
      result_shape.size(),
      0
  );

  std::vector<double> result_data;
  result_data.reserve(result_numel);

  for (
      std::size_t index = 0;
      index < result_numel;
      ++index
  ) {
    const std::size_t left_index =
        storage_index(coordinate, left_strides);

    const std::size_t right_index =
        storage_index(coordinate, right_strides);

    result_data.push_back(
        operation(
            data_[left_index],
            other.data_[right_index]
        )
    );

    advance_coordinate(coordinate, result_shape);
  }

  return Tensor(
      result_shape,
      std::move(result_data)
  );
}
```

### Narration

> Addition, subtraction, and multiplication already share this helper. Changing
> its shape and traversal rules once gives all three operators broadcasting.
>
> An empty output returns before accessing storage. A scalar still performs one
> iteration with an empty coordinate. Every result is appended in logical
> row-major order, so the output owns ordinary contiguous storage.

The old Test 19 expected `[2]` and `[1,2]` to be incompatible. Broadcasting
makes them compatible. Replace that test with:

```cpp
const Tensor formerly_mismatched =
    Tensor({2}, {1.0, 2.0}) +
    Tensor({1, 2}, {3.0, 4.0});

assert((
    formerly_mismatched.shape() ==
    std::vector<std::size_t>{1, 2}
));

assert((
    formerly_mismatched.data() ==
    std::vector<double>{4.0, 6.0}
));
```

---

## 17:40-18:30 - Run the complete linear layer

### Live coding

```cpp
const Tensor bias({2}, {10.0, -10.0});

const Tensor predictions =
    inputs.matmul(weights) + bias;

assert((
    predictions.shape() ==
    std::vector<std::size_t>{2, 2}
));

assert((
    predictions.data() ==
    std::vector<double>{14.0, -5.0, 20.0, 1.0}
));
```

### On screen

```text
inputs.matmul(weights) + bias

[
  [14, -5],
  [20,  1]
]
```

### Narration

> This is the expression from the opening. Matrix multiplication produces one
> weighted output vector per input row. Broadcasting applies the same bias
> vector to every row without materializing a repeated bias matrix.

---

## 18:30-21:30 - Harden the contracts after the payoff

### Empty inner dimension

```cpp
const Tensor empty_product =
    Tensor({2, 0}, {}).matmul(
        Tensor({0, 3}, {})
    );

assert((
    empty_product.shape() ==
    std::vector<std::size_t>{2, 3}
));

assert((
    empty_product.data() ==
    std::vector<double>{
        0.0, 0.0, 0.0,
        0.0, 0.0, 0.0
    }
));
```

### Narration

> The row and column both have length zero. Their dot product is an empty sum,
> so every output value is zero.

### Two-direction broadcasting

```cpp
const Tensor rows({2, 1}, {1.0, 2.0});
const Tensor columns({1, 3}, {10.0, 20.0, 30.0});

const Tensor grid = rows + columns;

assert((
    grid.shape() ==
    std::vector<std::size_t>{2, 3}
));

assert((
    grid.data() ==
    std::vector<double>{
        11.0, 21.0, 31.0,
        12.0, 22.0, 32.0
    }
));
```

### Narration

> Broadcasting is not a matrix-plus-bias special case. The left operand reuses
> one value across columns while the right operand reuses one row down the
> leading axis.

### Scalar and empty output

```cpp
const Tensor shifted =
    Tensor({2, 2}, {1.0, 2.0, 3.0, 4.0}) +
    Tensor({}, {10.0});

assert((
    shifted.data() ==
    std::vector<double>{11.0, 12.0, 13.0, 14.0}
));

const Tensor empty_broadcast =
    Tensor({0, 2}, {}) +
    Tensor({1, 2}, {10.0, 20.0});

assert((
    empty_broadcast.shape() ==
    std::vector<std::size_t>{0, 2}
));

assert(empty_broadcast.numel() == 0);
```

### Narration

> A scalar has no axes, so its single value is reused everywhere.
>
> Zero and one are broadcast-compatible, but their output dimension remains
> zero. The result therefore contains no elements.

### Invalid dimensions

```cpp
bool rejected_inner_dimensions = false;

try {
  const auto invalid =
      Tensor({2, 3}, std::vector<double>(6)).matmul(
          Tensor({4, 2}, std::vector<double>(8))
      );
} catch (const std::invalid_argument&) {
  rejected_inner_dimensions = true;
}

assert(rejected_inner_dimensions);

bool rejected_broadcast = false;

try {
  const auto invalid =
      Tensor(
          {2, 2},
          {1.0, 2.0, 3.0, 4.0}
      ) +
      Tensor({3}, {5.0, 6.0, 7.0});
} catch (const std::invalid_argument&) {
  rejected_broadcast = true;
}

assert(rejected_broadcast);
```

### Narration

> Matrix multiplication rejects unequal inner dimensions. Broadcasting rejects
> aligned dimensions that differ when neither is one.

Place the final output immediately before `return 0;`:

```cpp
std::cout << "predictions:\n";
std::cout
    << predictions.at({0, 0}) << ' '
    << predictions.at({0, 1}) << '\n'
    << predictions.at({1, 0}) << ' '
    << predictions.at({1, 1}) << '\n';

std::cout << "All assertions passed.\n";
```

---

## 21:30-22:30 - Name the capability precisely

### On screen

```text
inputs      [observations, input_features]
weights     [input_features, outputs]
bias        [outputs]
predictions [observations, outputs]
```

### Narration

> We now have the forward numerical core of a linear, or dense, layer. Each
> input row is one observation. Matrix multiplication reduces the shared
> feature axis. Broadcasting adds one bias per output to every observation.
>
> This is ordinary rank-two matrix multiplication whose rows happen to contain
> a batch. It is not generalized batched matrix multiplication over rank-three
> or higher tensors.
>
> Both kernels still assume contiguous row-major storage. A transpose or slice
> cannot yet share storage while changing how coordinates map into it.

---

## 22:30-23:20 - Review and next episode

### On screen

```text
rank-two dot failure
        -> row-column dot products
        -> matrix multiplication
        -> copied bias matrix
        -> zero-stride reuse
        -> inputs.matmul(weights) + bias
```

### Narration

> We turned the rank-two dot failure into matrix multiplication, produced a
> batch of output vectors, and made the final layer work with a copied bias.
>
> That copy exposed the need for broadcasting. Right alignment determined the
> output shape, and effective zero strides represented repeated reads without
> repeated storage.
>
> Next, we will store strides and offsets inside the tensor and use them to
> build transpose and selection as zero-copy views.

---

## 23:20-23:50 - Questions for Episode 5

### Narration

> I will leave you with three questions. Their answers are in the pinned comment
> below.

1. In `[m,k] @ [k,n]`, why must `k` match, and why does it disappear from the
   output shape?
2. How does an effective stride of zero let bias shape `[2]` participate in an
   operation whose output shape is `[2,2]` without allocating repeated data?
3. Why do the direct row-major index formulas in `matmul()` become insufficient
   once transpose and selection can return zero-copy views?

End the episode after the questions.
