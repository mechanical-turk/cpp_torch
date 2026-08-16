# Chapter 3 - Teaching Tensors to Compute

## Video brief

- **Working title:** Tensor Operations in C++: Arithmetic, Reductions & Dot
  Products | Deep Learning, All the Way Down #3
- **Target runtime:** 38-44 minutes
- **Viewer promise:** transform the tensor from a passive container into a
  composable numerical object and use it to express a complete linear
  prediction
- **Starting point:** the final Episode 2 `main.cpp`
- **Only code file:** `main.cpp`
- **Deliberately deferred:** broadcasting, matrix multiplication, stored
  strides, views, generic element types, autograd, external dependencies, and a
  build system

---

## 00:00-00:35 - Opening, previous state, and today's work

### Narration

> Welcome back to *Deep Learning, All the Way Down*, where we uncover how deep
> learning works by rebuilding its foundations in modern C++.
>
> In the previous episode, we completed the tensor's basic data structure. It
> can represent scalars and empty tensors, protect shape arithmetic from
> overflow, provide checked reads and mutation, and reduce all its values into
> a sum.
>
> Today, we will teach it to compute with other tensors. We will implement
> elementwise arithmetic, make reductions remain inside the tensor abstraction,
> build a dot product by composing those operations, and use the result to
> calculate a prediction.

### Segue into retrieval

> Before we write the first operator, let’s answer the questions from the end of
> the previous episode that define how tensor arithmetic must behave.

---

## 00:35-03:25 - Before we continue: Episode 2 retrieval

### Question 1

> Why does scalar shape `[]` imply one stored value rather than zero?

### Answer

> Shape `[]` describes a rank-zero tensor: there are no axes along which to
> choose a coordinate. It still represents one scalar value. Its element count
> is the product of an empty collection of dimensions, which is the
> multiplicative identity, one.

### Question 2

> Why does shape `[2,0,3]` have rank three but contain zero values?

### Answer

> Rank counts dimensions, so the three entries make its rank three. Element
> count multiplies their sizes. Because one dimension has size zero, the product
> is zero and there are no valid coordinates.

### Question 3

> Why must shape multiplication be checked before the multiplication occurs?

### Answer

> Unsigned overflow wraps during the multiplication. Checking afterward would
> inspect an already-corrupted result. We instead establish that the next
> multiplication fits before performing it.

### Question 4

> Why does mutable `at()` return `double&` rather than `double`?

### Answer

> Returning `double` would give the caller a copy. Returning `double&` refers to
> the stored element itself, so assigning through that reference mutates the
> selected tensor value.

### Question 5

> Why can individual values be mutable while the storage vector remains
> structurally protected?

### Answer

> Changing an existing value does not change the number of stored elements, so
> shape and storage still agree. Resizing the vector could violate that
> invariant, which is why the tensor exposes checked element mutation without
> exposing structural mutation.

### Question 6

> What makes `sum()` a reduction?

### Answer

> It combines many input values into fewer output values. Our full-tensor sum
> combines every element into one scalar result.

### Question 7

> Why is the sum of an empty tensor zero?

### Answer

> Summation begins at the additive identity, zero. An empty tensor supplies no
> values to add, so the accumulator remains zero.

### Question 8

> If two tensors have the same shape, what must an elementwise addition do to
> produce its output without changing either input?

### Answer

> It must combine values at corresponding coordinates, preserve the shared
> shape, and place the results into independent storage. The two operands remain
> unchanged.

### Transition

> Those answers give us the contract for our first operation: preserve shape,
> preserve both operands, and create a new result.

---

## 03:25-07:25 - Define elementwise computation

### Visual

```text
A = [[1, 2, 3],
     [4, 5, 6]]

B = [[10, 20, 30],
     [40, 50, 60]]

C = [[11, 22, 33],
     [44, 55, 66]]
```

Highlight corresponding coordinates:

```text
C[0,0] = A[0,0] + B[0,0] = 1 + 10 = 11
C[0,1] = A[0,1] + B[0,1] = 2 + 20 = 22
C[1,2] = A[1,2] + B[1,2] = 6 + 60 = 66
```

### Narration

> Elementwise computation applies one rule independently at every coordinate.
> For addition, the value at coordinate `[i,j]` in the output is the value at
> `[i,j]` in the left tensor plus the value at `[i,j]` in the right tensor.
>
> That definition requires both tensors to describe the same coordinates. We
> will therefore begin with a deliberately strict contract: the shapes must be
> exactly equal.

### Visual: establish the contract

```text
[2,3] + [2,3]  -> valid, output shape [2,3]
[3]   + [3]    -> valid, output shape [3]
[]    + []     -> valid, output shape []
[0]   + [0]    -> valid, output shape [0]

[2,3] + [3,2]  -> invalid
[3]   + [1,3]  -> invalid for now
```

### Narration

> Exact shape equality is not the most general rule used by mature tensor
> libraries. Broadcasting will eventually allow some different shapes to
> interact. But broadcasting is a new coordinate-mapping rule, not a small
> exception to elementwise traversal. We will earn that abstraction later.
>
> Notice that our existing scalar and empty-tensor semantics need no special
> cases. Two scalar tensors both have shape `[]`, so they have one pair of
> values to combine. Two tensors of shape `[0]` have equal shapes but no values,
> so their result is another empty tensor.

### Subject boundary

This section defines only equal-shape elementwise operations. Do not introduce
broadcasting terminology beyond the brief deferral above.

---

## 07:25-13:25 - Implement tensor addition

### Narration

> Adding two tensors is not one addition. It is one addition for every
> coordinate in their shared shape.

### Visual

```text
[1, 2, 3] + [10, 20, 30]

index 0:  1 + 10 = 11
index 1:  2 + 20 = 22
index 2:  3 + 30 = 33

result: [11, 22, 33]
```

### Live coding: declare the operator

Add this public member to `Tensor`:

```cpp
[[nodiscard]] Tensor operator+(const Tensor& other) const {
  if (shape_ != other.shape_) {
    throw std::invalid_argument(
        "elementwise operations require equal shapes"
    );
  }

  std::vector<double> result_data;
  result_data.reserve(numel());

  for (std::size_t index = 0; index < numel(); ++index) {
    result_data.push_back(data_[index] + other.data_[index]);
  }

  return Tensor(shape_, std::move(result_data));
}
```

### Walk through the signature

> `operator+` lets an ordinary expression such as `left + right` call this
> member function.
>
> The right operand is a const reference. The reference avoids copying an
> entire tensor merely to read it, and const prevents the operation from
> changing it.
>
> The member function itself is also const, which prevents it from changing the
> left operand. The result is returned by value because it is a new tensor with
> independent state.

### Walk through the body

> We reject unequal shapes before touching any values. Once the shapes agree,
> their element counts agree as a consequence of the constructor invariant.
>
> `reserve()` allocates enough capacity for the output without changing its
> size. Each `push_back()` then constructs the next actual result value.
>
> A member function may access private members of another object of the same
> class, which is why we can read `other.data_` directly here.

### Why move only the completed local vector

> `result_data` is local state that will never be used again. Moving it into the
> result lets the new tensor take ownership of the vector's allocation instead
> of copying every output value a second time.
>
> We still copy `shape_`, because the result needs its own shape and the left
> operand must remain unchanged.

### Assertions

```cpp
const Tensor left({3}, {1.0, 2.0, 3.0});
const Tensor right({3}, {10.0, 20.0, 30.0});

const Tensor added = left + right;

assert((added.shape() == std::vector<std::size_t>{3}));
assert((added.data() == std::vector<double>{11.0, 22.0, 33.0}));
assert((left.data() == std::vector<double>{1.0, 2.0, 3.0}));
assert((right.data() == std::vector<double>{10.0, 20.0, 30.0}));

const Tensor scalar_sum = Tensor({}, {2.0}) + Tensor({}, {3.0});
assert(scalar_sum.rank() == 0);
assert(scalar_sum.at({}) == 5.0);

const Tensor empty_sum = Tensor({0}, {}) + Tensor({0}, {});
assert((empty_sum.shape() == std::vector<std::size_t>{0}));
assert(empty_sum.numel() == 0);
```

### Shape-mismatch assertion

```cpp
bool rejected_mismatched_shapes = false;

try {
  const auto invalid = Tensor({2}, {1.0, 2.0})
      + Tensor({1, 2}, {3.0, 4.0});
} catch (const std::invalid_argument&) {
  rejected_mismatched_shapes = true;
}

assert(rejected_mismatched_shapes);
```

### Summary

> Tensor addition preserves the shared shape, combines corresponding values,
> and returns independent storage. Those three properties are the foundation
> of every equal-shape elementwise operation we add next.

---

## 13:25-20:25 - Separate traversal from arithmetic

### Begin with deliberate duplication

Show the direct addition implementation beside the operations we want:

```text
addition        result[i] = left[i] + right[i]
subtraction     result[i] = left[i] - right[i]
multiplication  result[i] = left[i] * right[i]
```

### Narration

> Shape validation, allocation, traversal, and result construction are
> identical for all three operations. Only the arithmetic applied to each pair
> changes.
>
> Copying the whole function twice would work, but it would create three places
> where the same traversal could drift apart. Instead, we will separate the
> stable mechanism from the changing arithmetic rule.

### Live coding: add the private helper

```cpp
[[nodiscard]] Tensor elementwise_binary(
    const Tensor& other,
    const auto& operation
) const {
  if (shape_ != other.shape_) {
    throw std::invalid_argument(
        "elementwise operations require equal shapes"
    );
  }

  std::vector<double> result_data;
  result_data.reserve(numel());

  for (std::size_t index = 0; index < numel(); ++index) {
    result_data.push_back(operation(data_[index], other.data_[index]));
  }

  return Tensor(shape_, std::move(result_data));
}
```

### Explain `const auto& operation`

> `operation` is any callable object that accepts the two current values and
> returns their combined value. Using `auto` here makes this member a function
> template, even though we did not write the longer `template` syntax
> explicitly.
>
> We pass the callable by const reference because the helper only invokes it.
> It does not need its own copy and does not modify the callable.

Keep this explanation narrow. Template instantiation, header visibility, and
generic library design belong to a later productionization episode.

### Live coding: rewrite the public operators

```cpp
[[nodiscard]] Tensor operator+(const Tensor& other) const {
  return elementwise_binary(
      other,
      [](const double left, const double right) {
        return left + right;
      }
  );
}

[[nodiscard]] Tensor operator-(const Tensor& other) const {
  return elementwise_binary(
      other,
      [](const double left, const double right) {
        return left - right;
      }
  );
}

[[nodiscard]] Tensor operator*(const Tensor& other) const {
  return elementwise_binary(
      other,
      [](const double left, const double right) {
        return left * right;
      }
  );
}
```

### Narration

> Each lambda supplies the one piece that varies. The helper owns everything
> common to equal-shape traversal.
>
> This is not abstraction for its own sake. We first wrote one complete
> operation, observed concrete duplication pressure, and only then extracted
> the shared mechanism.

### Assertions

```cpp
const Tensor arithmetic_left({3}, {2.0, 3.0, 4.0});
const Tensor arithmetic_right({3}, {5.0, 6.0, 7.0});

assert(((arithmetic_left + arithmetic_right).data()
        == std::vector<double>{7.0, 9.0, 11.0}));
assert(((arithmetic_left - arithmetic_right).data()
        == std::vector<double>{-3.0, -3.0, -3.0}));
assert(((arithmetic_left * arithmetic_right).data()
        == std::vector<double>{10.0, 18.0, 28.0}));
```

### Important distinction

> Multiplying two tensors can describe fundamentally different operations. The
> `*` operator we just wrote performs elementwise multiplication, not matrix
> multiplication.

### Visual

```text
elementwise

[1, 2] * [3, 4] = [3, 8]

same coordinate × same coordinate
```

Then contrast it with only the defining idea of matrix multiplication:

```text
matrix multiplication

output[i,j] = row i dot column j
```

### Narration

> Elementwise multiplication preserves the shared shape and multiplies values
> at corresponding coordinates. Matrix multiplication contracts an inner
> dimension by taking row-column dot products, so it follows a different shape
> rule and computes different values.
>
> We will not blur those concepts behind one implementation. Today `*` means
> elementwise multiplication. Matrix multiplication will receive its own
> explicit operation later.

### Summary

> Similar notation does not imply similar tensor semantics. Always ask how
> coordinates map from the inputs to the output.

---

## 20:25-25:25 - Keep reductions inside the tensor abstraction

### Return to the current limitation

Show the current signature:

```cpp
double sum() const;
```

> This implementation computes the correct number, but it creates a structural
> problem: the moment our tensor performs a reduction, the result stops being a
> tensor.

### Visual

```text
Tensor [1, 2, 3]
        |
       sum
        |
        6          <- ordinary double

Tensor [1, 2, 3]
        |
       sum
        |
Tensor shape []
       data [6]    <- composable scalar tensor
```

### Narration

> A full sum reduces every axis, so its output has no axes. That does not mean
> the result must leave the tensor abstraction. We already have a representation
> for one value with no axes: a rank-zero tensor.
>
> Keeping the result as a tensor means the next operation can consume it through
> the same API. Later, it also gives automatic differentiation a tensor node to
> attach to the computation graph.

Do not begin teaching autograd here. The single sentence above establishes the
future connection without opening a new subject.

### Live coding: change `sum()`

```cpp
[[nodiscard]] Tensor sum() const {
  double result = 0.0;

  for (const double value : data_) {
    result += value;
  }

  return Tensor({}, {result});
}
```

### Explain the changed exception contract

> Episode 2 marked `sum()` as `noexcept` because it returned a `double` and its
> loop performed no throwing operation.
>
> This version constructs a tensor and therefore allocates vector storage.
> Allocation can fail by throwing an exception, so retaining `noexcept` would
> make a false promise. We remove it.

### Assertions

```cpp
const Tensor reduced = Tensor({2, 3}, {1, 2, 3, 4, 5, 6}).sum();
assert(reduced.rank() == 0);
assert(reduced.numel() == 1);
assert(reduced.at({}) == 21.0);

const Tensor reduced_scalar = Tensor({}, {7.0}).sum();
assert(reduced_scalar.rank() == 0);
assert(reduced_scalar.at({}) == 7.0);

const Tensor reduced_empty = Tensor({0}, {}).sum();
assert(reduced_empty.rank() == 0);
assert(reduced_empty.at({}) == 0.0);
```

### Summary

> Reduction changes a tensor's shape; it does not have to abandon the tensor
> abstraction. A full sum naturally produces shape `[]`: one scalar value with
> no remaining axes.

### Transition

> Now elementwise multiplication produces a tensor, and summation also produces
> a tensor. Composing them gives us a new operation without writing a new
> arithmetic loop.

---

## 25:25-32:55 - Build dot product by composition

### Visual derivation

```text
left  = [2, 3, 4]
right = [5, 6, 7]

elementwise product = [10, 18, 28]
sum                 = 56
```

Then introduce the notation:

\[
\mathbf{x} \cdot \mathbf{y}
= \sum_{i=0}^{n-1} x_i y_i
\]

### Narration

> A dot product is defined for two vectors of the same length. We multiply
> corresponding values and then sum those products.
>
> Our first contract therefore accepts exactly two rank-one tensors with equal
> shapes. The output is a rank-zero tensor containing the dot product.

### Live coding

Add this public member:

```cpp
[[nodiscard]] Tensor dot(const Tensor& other) const {
  if (rank() != 1 || other.rank() != 1) {
    throw std::invalid_argument("dot requires two rank-one tensors");
  }

  if (shape_ != other.shape_) {
    throw std::invalid_argument("dot requires vectors of equal length");
  }

  // TODO(performance): Benchmark a fused dot-product kernel that avoids
  // allocating and traversing an intermediate product tensor.
  return (*this * other).sum();
}
```

### Walk through the implementation

> The rank check distinguishes vectors from scalars and matrices. Equal shape
> then guarantees equal vector length.
>
> The final line is the mathematical definition expressed directly in code:
> elementwise multiplication followed by reduction. We reuse both operations
> rather than introducing another loop that could disagree with them.

### Explain `*this`

Rewrite the expression with extra parentheses:

```cpp
return ((*this) * other).sum();
```

### Narration

> Every non-static member function receives an implicit pointer named `this`.
> Inside this const member function, `this` points to the left-hand tensor on
> which `dot()` was called.
>
> The first asterisk is the built-in pointer-dereference operator. `*this`
> means "the tensor object pointed to by `this`."
>
> The second asterisk is our overloaded tensor multiplication operator. It
> combines that left tensor with `other` and returns their elementwise product.
>
> Finally, `.sum()` is called on the temporary product tensor.

Show the complete evaluation order:

```text
this                         pointer to the left tensor
*this                        the left tensor object
(*this) * other              elementwise product tensor
((*this) * other).sum()      rank-zero sum tensor
```

### Equivalent member-call form

```cpp
return this->operator*(other).sum();
```

### Narration

> This form makes the member-function call explicit, but the operator form
> mirrors the dot-product definition more clearly. The parentheses in the
> original expression group the temporary product before calling `sum()`.

### Inspect the performance cost without guessing its magnitude

> This implementation is deliberately our clear reference version. It mirrors
> the derivation and lets us verify dot product by composing operations whose
> behavior we already understand.
>
> But that composition has a visible cost. Elementwise multiplication allocates
> an intermediate tensor containing every product. `sum()` then traverses that
> storage a second time before the temporary tensor is destroyed.

### Visual

```text
composed reference implementation

left * right
    -> allocate n products
    -> write n products

.sum()
    -> read n products
    -> accumulate one result
```

### Narration

> A fused implementation could multiply each pair and immediately add the
> product to one accumulator. That would avoid the size-`n` intermediate tensor
> and the second traversal.
>
> We can establish those structural differences by reading the code. What we
> cannot honestly claim yet is how much faster fusion would make this operation
> for real tensor sizes on real hardware.
>
> Reliable microbenchmarking requires us to control compiler optimization,
> prevent the computation from being removed, separate setup from measured
> work, repeat the operation, and interpret variation. Rather than introduce
> that entire subject in the middle of dot product, we will leave an explicit
> performance TODO and return to both implementations when we build proper
> benchmarking infrastructure.

### On screen

```text
clear reference implementation
        |
identify a plausible cost
        |
record an optimization hypothesis
        |
benchmark before redesigning
```

### Transition

> For now, correctness and compositional clarity remain the contract. Let’s
> verify the ordinary, empty, and invalid dot-product cases.

### Empty-vector dot product

### Visual

```text
[] of values with shape [0]
dot
[] of values with shape [0]

elementwise products: no values
sum of no values:     0
result shape:         []
```

### Narration

> Two vectors of length zero satisfy the dot-product contract. They produce no
> pairwise products, and the sum of that empty sequence is zero. The result is
> therefore a rank-zero tensor containing zero.

### Assertions

```cpp
const Tensor dot_result = Tensor({3}, {2.0, 3.0, 4.0})
    .dot(Tensor({3}, {5.0, 6.0, 7.0}));

assert(dot_result.rank() == 0);
assert(dot_result.at({}) == 56.0);

const Tensor empty_dot = Tensor({0}, {}).dot(Tensor({0}, {}));
assert(empty_dot.rank() == 0);
assert(empty_dot.at({}) == 0.0);
```

### Rejection assertions

```cpp
bool rejected_matrix_dot = false;

try {
  const auto invalid = Tensor({1, 2}, {1.0, 2.0})
      .dot(Tensor({1, 2}, {3.0, 4.0}));
} catch (const std::invalid_argument&) {
  rejected_matrix_dot = true;
}

assert(rejected_matrix_dot);

bool rejected_unequal_lengths = false;

try {
  const auto invalid = Tensor({2}, {1.0, 2.0})
      .dot(Tensor({3}, {3.0, 4.0, 5.0}));
} catch (const std::invalid_argument&) {
  rejected_unequal_lengths = true;
}

assert(rejected_unequal_lengths);
```

---

## 32:55-39:00 - Express a linear prediction

### Begin with one observation

### Visual

```text
one observation

feature 0 = 4.0
feature 1 = 3.0
feature 2 = 2.0

features = [4.0, 3.0, 2.0]
```

### Narration

> A model receives information about something we want it to evaluate. One
> observation might describe a house, a financial instrument, an image, or any
> other object using measurable numeric properties.
>
> We call those input properties features. Here one observation has three
> features, so we store them in one rank-one tensor of length three.

### Give each feature a weight

### Visual

```text
features = [ 4.0,  3.0, 2.0 ]
weights  = [ 0.5, -1.0, 2.0 ]

feature 0 uses weight 0
feature 1 uses weight 1
feature 2 uses weight 2
```

### Narration

> A linear model assigns one weight to each feature. The weight controls how
> that feature contributes to the prediction.
>
> A positive weight gives a positive contribution when its feature is positive.
> A negative weight gives a negative contribution. Its magnitude controls how
> strongly the feature is scaled.
>
> For now, assume these weights have already been chosen. Learning how training
> discovers useful weights is a later step. Right now, we are only defining the
> forward computation that uses them.

### Compute each weighted contribution

### Visual

```text
feature   weight   contribution

  4.0  ×   0.5  =      2.0
  3.0  ×  -1.0  =     -3.0
  2.0  ×   2.0  =      4.0
```

### Narration

> Multiplying corresponding features and weights gives three separate weighted
> contributions. But the model must produce one prediction, so we add those
> contributions together.

### Visual

```text
weighted sum = 2.0 + (-3.0) + 4.0
             = 3.0
```

### Introduce the bias

### Visual

```text
weighted sum = 3.0
bias         = 0.5

prediction   = 3.0 + 0.5
             = 3.5
```

### Narration

> Finally, the bias adds a constant offset. If every feature were zero, every
> weighted contribution would also be zero, and the bias would be the model's
> prediction. It therefore acts as the model's baseline before the features
> move the result away from it.

### Write the expanded model

\[
\hat{y}
= w_0x_0 + w_1x_1 + w_2x_2 + b
\]

### Narration

> `x` represents the feature vector, `w` represents the weight vector, `b` is
> the bias, and `y-hat` is the prediction. The hat distinguishes the model's
> prediction from an observed target value, which is commonly written as `y`.

### Compress the weighted sum into a dot product

### Visual

\[
\hat{y} = \mathbf{w} \cdot \mathbf{x} + b
\]

```text
w dot x = sum of corresponding products
        = 2.0 + (-3.0) + 4.0
        = 3.0
```

### Narration

> The dot product is compact notation for exactly the work we just performed:
> multiply every feature by its corresponding weight, then sum the products.
> Adding the bias gives the final prediction.
>
> The feature and weight tensors both have shape `[3]`, so their dot product is
> valid and returns a rank-zero tensor. The bias is also a rank-zero tensor.
> Their shapes therefore agree, and our existing elementwise addition combines
> them into the scalar prediction.

### Live coding

```cpp
const Tensor weights({3}, {0.5, -1.0, 2.0});
const Tensor features({3}, {4.0, 3.0, 2.0});
const Tensor bias({}, {0.5});

const Tensor prediction = weights.dot(features) + bias;

assert(prediction.rank() == 0);
assert(prediction.at({}) == 3.5);

std::cout << "prediction: " << prediction.at({}) << '\n';
std::cout << "All assertions passed.\n";
```

### Narration

> This is forward computation only. The weights do not learn, no gradients are
> calculated, and the result retains no record of the operations that produced
> it.
>
> But the expression is already structurally important. A real training system
> will eventually execute computations like this, measure their error, and walk
> backward through the recorded operations to update the parameters.

### Summary

> We began with storage and shape. We can now compose tensor operations into a
> mathematical model: weighted features, reduction, bias, and one scalar
> prediction.

---

## 39:00-41:30 - Review

### Visual recap

```text
equal-shape coordinate rule
            |
            v
        +   -   *
            |
            v
  sum() -> scalar Tensor
            |
            v
 dot() = multiply then sum
            |
            v
prediction = weights.dot(features) + bias
```

### Narration

> Our tensor is no longer only a validated container. It can now add, subtract,
> and multiply equal-shape tensors without changing either input.
>
> We separated their shared traversal from their arithmetic rules, then changed
> `sum()` to return a rank-zero tensor so reductions remain composable.
>
> That let us define dot product directly as elementwise multiplication followed
> by summation. Finally, we combined a dot product with a scalar bias to express
> one complete linear prediction.
>
> The limitations remain intentional. Different shapes cannot interact,
> matrices cannot multiply, and no operation records a computation graph. But
> we now have the first small vocabulary from which larger numerical programs
> can be assembled.

---

## 41:30-42:00 - Next episode setup

### Visual

```text
Next episode

- matrix multiplication
- broadcasting
- batched dense computation

inputs.matmul(weights) + bias
```

### Narration

> Next, we will implement matrix multiplication, extend our elementwise
> operations with broadcasting, and combine them to batch predictions from a batch of observations

---

## 42:00-43:15 - Questions for Episode 4

> Before the next episode, pause here and make sure you can answer these
> questions:

1. Why does an equal-shape elementwise operation preserve the operands' shape?
2. Why does a full `sum()` return a tensor with shape `[]`, and why did that
   change remove its previous `noexcept` guarantee?
3. How does `weights.dot(features) + bias` build a linear prediction from
   elementwise multiplication, reduction, and scalar-tensor addition?

End the episode after the questions. Do not place another recap or call to
action after them.
