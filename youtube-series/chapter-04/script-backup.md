# Episode 4 - Building a Linear Layer from Scratch in C++

## Video brief

- **Working title:** Building a Linear Layer from Scratch in C++ | Matmul and
  Broadcasting | Deep Learning, All the Way Down #4
- **Target runtime:** 25-29 minutes
- **Viewer promise:** apply one linear transformation to a batch of inputs with
  `inputs.matmul(weights) + bias`
- **Starting point:** the final Episode 3 `main.cpp`
- **Only code file:** `main.cpp`
- **Deliberately deferred:** stored strides and offsets, zero-copy views,
  rank-N batched matrix multiplication, optimized kernels, autograd, generic
  element types, external dependencies, and a build system

Compile and run with:

```sh
clang++ -std=c++23 main.cpp -o main
./main
```

The existing test labels still print. The final lines are:

```text
predictions:
14 -5
20 1
All assertions passed.
```

---

## 00:00-00:20 - One matrix cell is still a dot product

### On screen

Begin on the failure produced by the current tensor:

```cpp
inputs.dot(weights);
```

```text
dot requires two rank-one tensors
```

Then highlight the first row and first column:

```text
[1, 2, 3] dot [1, 0, 1] = 4
```

End the opening on:

```text
inputs [2,3] @ weights [3,2] + bias [2]

              [[14, -5],
               [20,  1]]
```

### Narration

> Welcome back to *Deep Learning, All the Way Down*, where we rebuild deep
> learning from first principles in modern C++. Our tensor rejects these
> matrices. But each output cell is still a dot product: this row times this
> column gives four. Today we will build matrix multiplication and reuse one
> bias across every row without copying it.

---

## 00:20-00:30 - Recap and destination

### Narration

> Last time, our tensor learned arithmetic, reduction, dot product, and one
> scalar prediction. Now we will run the same linear transformation across a
> matrix of inputs.

---

## 00:30-01:00 - Retrieve the three rules we need

Display each complete question while answering it in one sentence.

### Question 1

> Why does an equal-shape elementwise operation preserve the operands' shape?

### Answer

> It produces one output for every shared input coordinate, so the output has
> the same coordinate set and the same shape.

### Question 2

> Why does a full `sum()` return a tensor with shape `[]`, and why did that
> change remove its previous `noexcept` guarantee?

### Answer

> Summing every axis leaves one scalar, and constructing that result can
> allocate and throw, so the function can no longer promise `noexcept`.

### Question 3

> How does `weights.dot(features) + bias` build a linear prediction from
> elementwise multiplication, reduction, and scalar-tensor addition?

### Answer

> The dot product multiplies corresponding features and weights, reduces those
> contributions to one scalar, and then adds the scalar bias.

### Transition

> That expression handles one feature vector. Now let us run the current code
> against two matrices and follow the failure.

---

## 01:00-02:15 - Follow the rank failure into matrix multiplication

### Live setup

Add the standard-library headers used explicitly by the existing file:

```cpp
#include <string>
#include <utility>
```

At the bottom of `main()`, remove the final Episode 3 explanatory comments and
demo beginning with:

```cpp
// features = [4.0, 3.0, 2.0]
```

Remove that block through the old `"Success!"` print, but keep `return 0;`.
This avoids redeclaring its `weights` and `bias` variables. In its place, begin
the Episode 4 setup:

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
```

Temporarily add and run:

```cpp
const Tensor invalid = inputs.dot(weights);
```

After observing the exception, delete this line before continuing. It is a
deliberate failure demonstration; leaving it in place would prevent every later
assertion from running.

### Narration

> `dot()` rejects this because both tensors have rank two. That rejection is
> correct. A vector dot product chooses no output coordinate and returns one
> scalar. Here, we need a result for every pairing of an input row and a weight
> column.

### On screen

```text
inputs row 0   [1, 2, 3]
weights col 0 [1, 0, 1]

output[0,0] = 1*1 + 2*0 + 3*1 = 4
```

```text
inputs row 0   [1, 2, 3]
weights col 1 [0, 1, 1]

output[0,1] = 1*0 + 2*1 + 3*1 = 5
```

### Narration

> The output coordinate chooses the row and column. A third coordinate moves
> across the selected row and down the selected column, multiplying and
> accumulating as it goes.

### General rule

```text
left  [m,k]
right   [k,n]
        └─┘ these dimensions must match

output [m,n]
```

\[
C_{i,j} = \sum_{r=0}^{k-1} A_{i,r}B_{r,j}
\]

### Narration

> The left matrix contributes `m` output rows. The right matrix contributes
> `n` output columns. The shared size `k` is traversed and summed, so it does
> not appear in the output shape.

---

## 02:15-02:45 - Reuse the existing safe element count

### Narration

> Matrix multiplication must allocate storage for its output shape. We already
> wrote the correct overflow-safe element-count rule in Episode 2, so before we
> allocate, I am moving that exact rule into a reusable helper. This is a
> refactor, not a new tensor rule.

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

Replace the constructor's inline calculation:

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

---

## 02:45-06:15 - Implement matmul while following one output cell

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

> The rank check comes first because everything below gives the two axes a
> matrix-specific meaning. `rows` comes from the left matrix, `columns` comes
> from the right matrix, and both operands must agree on `inner`.

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

> The two outer loops choose one output coordinate: `row` and `column`. The
> inner loop computes the dot product stored at that coordinate.
>
> Our tensor still guarantees contiguous row-major storage. The left matrix has
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

> Matrix multiplication now works. Every input row has produced one output
> vector. We still need to add one bias per output.

---

## 06:15-08:00 - Make the prediction work the wasteful way

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

> We already have the correct predictions. Nothing about this result is
> mathematically wrong. The problem is how we represented the bias.
>
> The two bias values do not change between input rows, yet we copied them once
> for every row just to satisfy the equal-shape addition rule. For one million
> input rows, this representation would store two million bias values to
> describe two numbers.
>
> Broadcasting lets us express that reuse directly.

---

## 08:00-10:15 - Derive broadcasting from the repeated bias

### Right-align the shapes

```text
linear  [2,2]
bias      [2]

right-aligned:

linear  [2,2]
bias    [1,2]
```

### Narration

> Broadcasting compares axes from the right. The bias has no leading row axis,
> so we treat that missing axis as size one.
>
> Equal dimensions already name the same coordinates. If one dimension is one,
> it has only coordinate zero, so the same value can be reused while the other
> operand moves. Any other mismatch is invalid.

### On screen

```text
output [0,0] -> linear [0,0], bias [0]
output [0,1] -> linear [0,1], bias [1]
output [1,0] -> linear [1,0], bias [0]
output [1,1] -> linear [1,1], bias [1]
```

### Narration

> Changing the output row must not move through the bias storage. Changing the
> output column must move to the next bias value.

### Introduce effective strides

```text
output axis               row  column

linear effective stride    2      1
bias effective stride      0      1
```

### Narration

> A stride tells us how far the flat storage position moves when one coordinate
> increases. Giving the bias an effective row stride of zero means every output
> row reuses the same two values. This describes the repeated reads without
> allocating the repeated matrix.
>
> These are temporary strides used by the operation. Stored tensor strides and
> zero-copy views remain the next episode's subject.

---

## 10:15-12:15 - Compute the broadcast result shape

### Live coding

Add:

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

> `offset` counts from the right edge. If an operand has no axis at that
> position, its missing leading dimension becomes one.
>
> Each axis either agrees, expands a size-one dimension, or rejects the
> operation. Notice that we do not use `max`. Zero and one are compatible, but
> their output dimension must remain zero, not one.

---

## 12:15-14:30 - Build the two effective stride vectors

### Ordinary row-major strides

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

> We first recover the ordinary row-major strides implied by each input shape.
> For shape `[2,2]` they are `[2,1]`; for shape `[2]` the stride is `[1]`.

### Effective broadcast strides

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

> The effective vector begins entirely at zero. Missing leading axes stay zero,
> and real size-one axes stay zero. Every other aligned axis retains its
> ordinary stride.

---

## 14:30-16:00 - Traverse one output coordinate space

### Convert a coordinate into an operand storage index

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

### Advance in row-major logical order

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

> We will traverse the output coordinates once. The same output coordinate is
> dotted with each operand's effective strides, so it can select different
> physical values from the two inputs.
>
> The coordinate advances like an odometer: the rightmost axis changes first,
> then carries into the axis to its left.

---

## 16:00-18:15 - Generalize the shared elementwise kernel

### Live coding

Replace `elementwise_binary()`:

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

> Addition, subtraction, and multiplication already share this helper. By
> changing its shape and traversal rules once, all three operators acquire
> broadcasting.
>
> Empty outputs return before any data access. A scalar output still has one
> iteration with an empty coordinate, and both storage indices remain zero.
>
> The output values are appended in logical row-major order, so the result owns
> ordinary contiguous storage even when an input value was reused.

### Run the original expression

The old Test 19 expected `[2]` and `[1,2]` to be incompatible. Broadcasting
makes that pair valid. Replace that obsolete rejection test with:

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

Now run the expression that motivated the episode:

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

> This is the exact expression we wanted. The matrix multiplication produces
> one weighted output vector per input row. Broadcasting applies the same bias
> vector to every row without materializing the expanded bias matrix.

---

## 18:15-22:30 - Harden the contracts after the main result works

### Matrix multiplication edge cases

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

> A row of length zero and a column of length zero have matching lengths. Their
> dot product is an empty sum, so each of the six output values is zero.

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
```

### Broadcasting in two directions

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

> Broadcasting is not a special case for matrix plus bias. Here, the left
> operand reuses one value across each row, while the right operand reuses one
> row down the leading axis.

### Scalar and empty outputs

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

> Scalar shape has no axes, so every missing axis acts like one and the single
> value is reused everywhere.
>
> For `[0,2]` and `[1,2]`, zero and one are compatible, but the result keeps
> the zero dimension. The output therefore contains no elements.

### Incompatible shapes

```cpp
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

> The aligned final axes are two and three. They are unequal, and neither is
> one, so no coordinate-reuse rule can make these shapes compatible.
>
> Because every elementwise operator uses the same kernel, subtraction and
> multiplication now inherit these broadcasting rules too.

### Print only after every assertion has run

Place this immediately before `return 0;`:

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

## 22:30-24:00 - State the exact capability and its limits

### On screen

```text
inputs      [observations, input_features]
weights     [input_features, outputs]
bias        [outputs]
predictions [observations, outputs]
```

### Narration

> We have implemented the forward numerical core of a linear, or dense, layer.
> Each input row is one observation. Matrix multiplication reduces the shared
> feature axis. Broadcasting adds one bias per output to every observation.
>
> This is ordinary rank-two matrix multiplication where rows happen to contain
> a batch. It is not generalized batched matrix multiplication over rank-three
> or higher tensors.
>
> Both kernels also assume that every tensor owns contiguous row-major storage.
> The stride vectors used for broadcasting are temporary. A transpose or slice
> cannot yet share storage while changing how logical coordinates map to it.

---

## 24:00-25:00 - Review and next episode

### Visual recap

```text
rank-two dot failure
        |
        v
one row-column dot product
        |
        v
matrix multiplication
        |
        v
repeated bias matrix
        |
        v
zero-stride reuse
        |
        v
inputs.matmul(weights) + bias
```

### Narration

> We followed one concrete failure into matrix multiplication, and we built the
> complete kernel from row-column dot products.
>
> We then made the final prediction work with a copied bias matrix, used that
> waste to derive broadcasting, and represented repeated reads with effective
> zero strides.
>
> Next, we will make strides part of the tensor itself, add storage offsets, and
> use them to build transpose and slice operations that share storage instead
> of copying it.

---

## 25:00-25:45 - Questions for Episode 5

> Before the next episode, pause here and make sure you can answer these
> questions:

1. In `[m,k] @ [k,n]`, why does `k` have to match, and why does it disappear
   from the output shape?
2. How does an effective stride of zero let `[2]` participate in an operation
   whose output shape is `[2,2]` without allocating a repeated input?
3. Why will the direct row-major index formulas in `matmul()` stop being
   sufficient once transpose and slice can return zero-copy views?

End the episode after the questions.
