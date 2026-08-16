# Chapter 2 - Completing the Tensor Data Structure

## Video brief

- **Working title:** Completing Our Tensor in C++: Scalars, Mutation, and Reductions | Deep Learning, All the Way Down #2
- **Target runtime:** 33-37 minutes
- **Viewer promise:** remove Chapter 1's artificial restrictions, make the
  tensor safe for scalar and empty shapes, protect element-count arithmetic from
  overflow, support checked mutation, and implement the first whole-tensor
  operation
- **Only code file:** `main.cpp`
- **Deliberately deferred:** generic dtypes, elementwise arithmetic,
  broadcasting, views, autograd, external dependencies, and a build system

Compile and run with:

```sh
clang++ -std=c++23 main.cpp -o main
./main
```

Expected final output:

```text
All assertions passed.
shape: [2, 3]
rank: 2
elements: 6
value at [1, 2]: 42
sum: 57
```

---

## 00:00-00:45 - Cold open

### Narration

> Welcome back to *Deep Learning, All the Way Down*, where we uncover how deep
> learning works by rebuilding its foundations in modern C++.
>
> Last time, we built the smallest tensor that could own flat storage, describe
> its shape, and support checked multidimensional reads. Today, we will complete
> that basic data structure by supporting scalars and empty tensors, preventing
> shape overflow, enabling checked mutation, and implementing our first
> reduction operation: sum.

### Visual

Show the final Chapter 1 tensor briefly, then replace it with today's four goals:

```text
Chapter 2

scalar and empty shapes
safe element counting
checked mutation
whole-tensor sum
```

### Production note

Deliver the series identity, previous state, and current promise as one
continuous opening. Do not insert a separate recap or title sequence.

### Segue into retrieval

> Before we change the implementation, let’s quickly answer the questions we
> left at the end of Chapter 1. Each answer gives us something we will rely on
> today.

Cut directly from this sentence to the first question. Do not insert another
section card or recap montage.

---

## 00:45-02:30 - Before we continue: Chapter 1 retrieval

### Question 1

> What are the rank and element count of shape `[2,3,4]`?

### Answer

> Rank is the number of axes, so the rank is three. Element count is the product
> of the dimensions: two times three times four, which is twenty-four.

### Visual

```text
shape = [2, 3, 4]
rank  = 3
numel = 2 × 3 × 4 = 24
```

### Question 2

> Why do six values not uniquely determine shape `[2,3]`?

### Answer

> Element count tells us how many values exist, not how they are organized.
> Six values are compatible with `[6]`, `[2,3]`, `[3,2]`, `[1,6]`, and
> infinitely many other shapes.
>
> The reason there are infinitely many is that a dimension of size one does not
> change the product. We can begin with `[6]` and keep adding size-one
> dimensions: `[1,6]`, `[1,1,6]`, `[1,1,1,6]`, and so on. Every shape still
> describes six values, but each has a different rank and organization.
>
> The flat values alone therefore cannot tell us which shape was intended.

### Question 3

> What invariant does the constructor establish?

### Answer

> The number of values implied by the shape must equal the number of values in
> storage. Once construction succeeds, the tensor's shape and storage cannot
> contradict each other.

### Question 4

> Why does `data()` return a const reference?

### Answer

> Returning a reference avoids copying the vector. Making it const prevents the
> caller from resizing the storage through this accessor and breaking the
> relationship between shape and storage.

### Question 5

> For shape `[2,3]`, why does coordinate `[1,2]` map to flat position five?

### Answer

> Each row contains three values. Reaching row one skips one complete row, and
> column two advances two more positions. The flat index is `1 * 3 + 2`, which
> equals five.

### Transition

> Every answer depended on the relationship between shape and element count.
> We will begin by extending that relationship to shapes Chapter 1 could not
> represent.

---

## 02:30-08:30 - Scalars, singleton vectors, and empty tensors

## Intentional clip module 1

### Candidate Short title

`Why a Scalar Tensor Has One Value but No Dimensions`

### Clip boundary

The clip begins at the hook and ends after the four cases are derived. It must
not refer to Chapter 1 or depend on the preceding retrieval section.

### Hook

> These four tensor shapes expose an important distinction between rank and
> element count: `[]`, `[1]`, `[0]`, and `[5,0]`.

### Vertical-safe visual

Keep all essential information inside the centered vertical crop:

```text
shape  rank  elements  meaning
[]       0      1      scalar
[1]      1      1      singleton vector
[0]      1      0      empty vector
[5,0]    2      0      empty matrix
```

### Narration

> Shape `[]` contains no axes, so its rank is zero. But it still represents one
> value: a scalar. There are no coordinates to choose because there is only one
> possible value.
>
> Shape `[1]` has one axis, and that axis has one valid coordinate: zero. It is
> not a scalar. It is a rank-one vector containing one value.
>
> Shape `[0]` also has one axis, but that axis has no valid coordinates. It is a
> rank-one empty vector containing no values.
>
> Shape `[5,0]` has two axes, so its rank is two. We can think of it as five
> rows, each containing zero values. It is therefore an empty matrix.
>
> Rank answers how many axes exist. Element count answers how many values exist.
> Those are different questions.

### Segue into implementation

> These are not four unrelated exceptions that we need to hard-code. Our
> existing element-count loop is already very close to describing all of them.
> Let’s open the constructor and see what actually needs to change.

### Live coding: relax construction

Remove the Chapter 1 checks that reject an empty shape and zero dimensions.
Keep the product initialized to one:

```cpp
std::size_t expected_elements = 1;

for (const std::size_t dimension : shape_) {
  expected_elements *= dimension;
}

if (expected_elements != data_.size()) {
  throw std::invalid_argument("tensor shape does not match its data");
}
```

### Explain the behavior in the code

> The product begins at one. For scalar shape `[]`, the loop has no dimensions
> to visit, so it performs no multiplication and the result remains one. This is
> called the empty product.
>
> For `[0]`, it multiplies by zero and produces zero. For `[5,0]`, it multiplies by five
> and then by zero, which also produces zero.
>
> That means the multiplication already gives every shape in our table the
> correct element count. The only code preventing those tensors from existing
> is the pair of checks we added in Chapter 1 to reject empty shapes and
> zero-sized dimensions. We can remove them.

### Clip conclusion

> A missing dimension and a zero-sized dimension are not the same thing. With
> no dimensions, the product remains one and represents a scalar. With a zero
> dimension, the product becomes zero and represents an empty tensor.

Explain what the unchanged loop now produces:

```text
Tensor({}, {7.0})       valid scalar
Tensor({1}, {7.0})      valid singleton vector
Tensor({0}, {})         valid empty vector
Tensor({2,0,3}, {})     valid rank-three empty tensor
Tensor({}, {})          invalid: scalar needs one value
Tensor({0}, {7.0})      invalid: empty tensor needs zero values
```

### Assertions

```cpp
const Tensor scalar({}, {7.0});
assert(scalar.rank() == 0);
assert(scalar.numel() == 1);

const Tensor singleton({1}, {7.0});
assert(singleton.rank() == 1);
assert(singleton.numel() == 1);

const Tensor empty_vector({0}, {});
assert(empty_vector.rank() == 1);
assert(empty_vector.numel() == 0);

const Tensor higher_rank_empty({2, 0, 3}, {});
assert(higher_rank_empty.rank() == 3);
assert(higher_rank_empty.numel() == 0);
```

---

## 08:30-16:00 - Make tensor arithmetic overflow-safe

## Intentional clip module 2

### Candidate Short title

`The Unsigned Overflow Bug Hiding in This Tensor Constructor`

### Segue from scalar and empty tensors

> Scalars and empty tensors now work, and the assertions confirm that our
> element-count rule handles both correctly. But while reading the constructor,
> we passed over a warning that has been sitting in the code since Chapter 1.

Highlight the first TODO:

```cpp
expected_elements *= dimension;
// TODO: handle overflow
```

> We actually left the same warning in two places. The constructor multiplies
> dimensions to validate the tensor, and `at()` multiplies strides to locate an
> element. Both calculations use `std::size_t`, so before we add more behavior,
> we need to prove that neither calculation can silently wrap around.

Briefly show the second TODO, then return to the constructor. We will solve the
constructor first because the safety of indexing will depend on the invariant
established here.

### Hook

> This multiplication validates our tensor, but with a sufficiently large shape
> it can silently validate the wrong tensor.

### Vertical-safe visual

Show only the relevant expression and a small unsigned-number wheel:

```cpp
expected_elements *= dimension;
```

```text
largest size_t + 1 -> 0
```

### Narration

> `std::size_t` is an unsigned integer with a finite maximum value. Unsigned
> arithmetic wraps modulo its representable range. If a shape product exceeds
> that range, it can wrap to a much smaller number.
>
> This is worse than merely reporting the wrong element count. The wrapped
> result participates in our constructor invariant and could make an invalid
> shape appear to agree with the storage.

### Derive the safe check

### Narration

> We need to check before multiplying. For a positive dimension, the next
> multiplication would overflow when:

```text
current_product > max_size_t / dimension
```

> Zero needs one special step because we cannot divide by it. We inspect the
> whole shape for zero first. If one exists, the tensor is empty and the element
> count is zero. Otherwise, every dimension is positive and we can safely use
> this check inside the loop.

### Live coding

```cpp
#include <algorithm>
#include <limits>
```

Replace the unchecked multiplication:

```cpp
const bool has_zero_dimension = std::ranges::contains(shape_, 0);

if (has_zero_dimension) {
  expected_elements = 0;
} else {
  for (const std::size_t dimension : shape_) {
    if (
        expected_elements >
        std::numeric_limits<std::size_t>::max() / dimension
    ) {
      throw std::overflow_error("tensor element count overflows size_t");
    }

    expected_elements *= dimension;
  }
}
```

### Walk through the implementation

> We handle an empty shape first. Otherwise, before every multiplication, we
> check whether it fits. If it does not, the constructor throws.

### Assertion

> We test one overflowing shape and one enormous shape that is still empty
> because it contains a zero.

```cpp
bool rejected_overflow = false;

try {
  const Tensor impossible(
      {std::numeric_limits<std::size_t>::max(), 2},
      {}
  );
} catch (const std::overflow_error&) {
  rejected_overflow = true;
}

assert(rejected_overflow);

const Tensor huge_but_empty(
    {std::numeric_limits<std::size_t>::max(), 2, 0},
    {}
);
assert(huge_but_empty.numel() == 0);
```

### Clip conclusion

> The order matters: first determine whether the tensor is empty. If it is not,
> prove that each multiplication fits before performing it. Once unsigned
> multiplication has wrapped, checking afterward is already too late.

### Return to the second TODO: indexing arithmetic

Show the current `at()` loop:

```cpp
for (std::size_t axis = rank(); axis > 0; --axis) {
  const std::size_t current_axis = axis - 1;

  if (idx[current_axis] >= shape_[current_axis]) {
    throw std::out_of_range("tensor index is outside its dimension");
  }

  flat_index += idx[current_axis] * stride;
  stride *= shape_[current_axis];
  // TODO: handle overflow
}
```

### Narration

> It is tempting to add another overflow check to every multiplication and
> addition here. But the constructor has already given us a stronger fact: for
> every non-empty tensor, the product of the complete shape fits in
> `std::size_t` and equals the size of storage.
>
> If every coordinate is also within its dimension, each stride is at most the
> complete element count, and the final flat index is at most `numel() - 1`.
> Under those two invariants, the indexing arithmetic cannot overflow.
>
> The problem is that our current loop validates one coordinate and immediately
> performs arithmetic before validating the remaining coordinates. For an empty
> shape with enormous dimensions, suffix-stride multiplication could overflow
> before the loop reaches the zero-sized axis and rejects the index.

### Live coding: validate before flattening

Separate validation from offset calculation:

```cpp
for (std::size_t axis = 0; axis < rank(); ++axis) {
  if (idx[axis] >= shape_[axis]) {
    throw std::out_of_range("tensor index is outside its dimension");
  }
}

std::size_t flat_index = 0;
std::size_t stride = 1;

for (std::size_t axis = rank(); axis > 0; --axis) {
  const std::size_t current_axis = axis - 1;
  flat_index += idx[current_axis] * stride;
  stride *= shape_[current_axis];
}
```

### Explain why both operations are now safe

> If the tensor has a zero-sized axis, no coordinate can pass the first loop,
> so no flattening arithmetic occurs. If every coordinate passes, the tensor is
> non-empty. Its complete shape product was checked by the constructor, and a
> valid flat index must remain inside that product.
>
> We did not make indexing safe by scattering checks across every arithmetic
> expression. We made it safe by validating the representation once during
> construction, validating all coordinates before calculation, and then relying
> on those established invariants.

Remove the second overflow TODO.

### Indexing overflow assertion

```cpp
const Tensor huge_but_empty(
    {0, std::numeric_limits<std::size_t>::max(),
     std::numeric_limits<std::size_t>::max()},
    {}
);

bool rejected_empty_access = false;

try {
  static_cast<void>(huge_but_empty.at({0, 0, 0}));
} catch (const std::out_of_range&) {
  rejected_empty_access = true;
}

assert(rejected_empty_access);
```

> This test is useful because the old right-to-left loop could multiply the two
> enormous trailing dimensions before reaching the zero-sized leading axis.
> The new validation pass rejects the coordinate before any stride is computed.

---

## 16:00-19:00 - Query one dimension safely

### Motivation

> We can ask for the whole shape, but operations will often need the size of one
> particular axis. Let us give that question a checked public interface.

### Live coding

```cpp
[[nodiscard]] std::size_t dimension(const std::size_t axis) const {
  if (axis >= rank()) {
    throw std::out_of_range("tensor axis is outside its rank");
  }

  return shape_[axis];
}
```

### Discussion

- `rank()` reports the number of axes.
- `dimension(axis)` reports the size of one axis.
- A rank-zero scalar has no valid axis.
- An empty tensor can still have valid axes. For `[2,0,3]`, dimensions zero,
  one, and two exist even though the tensor stores no values.
- Zero-sized and nonexistent axes are different.

### Assertions

```cpp
const Tensor tensor({2, 0, 3}, {});
assert(tensor.dimension(0) == 2);
assert(tensor.dimension(1) == 0);
assert(tensor.dimension(2) == 3);

bool rejected_axis = false;

try {
  static_cast<void>(tensor.dimension(3));
} catch (const std::out_of_range&) {
  rejected_axis = true;
}

assert(rejected_axis);
```

Briefly explain `static_cast<void>` as an explicit statement that the result is
being discarded intentionally.

---

## 19:00-26:30 - Support checked mutation without exposing storage

### Motivation

Show the Chapter 1 API:

```cpp
double value = tensor.at({1, 2});
```

Then show the desired use:

```cpp
tensor.at({1, 2}) = 42.0;
```

### Narration

> A trainable tensor must eventually change. The narrowest useful capability is
> not exposing the entire vector for arbitrary resizing. It is allowing callers
> to update one already-valid element through checked tensor coordinates.

### First design question

> What must `at()` return for an assignment through the function call to update
> the stored value?

Show:

```cpp
double at(...) const;  // returns a copy
double& at(...);       // returns the stored object
```

### Narration

> Returning `double` produces a separate value. Assigning to that temporary
> cannot update the vector. Returning `double&` gives the caller another name
> for the selected stored element.

### Avoid duplicated validation

Move coordinate validation and flattening into a private helper:

```cpp
[[nodiscard]] std::size_t flat_index(
    const std::vector<std::size_t>& indices
) const {
  if (indices.size() != rank()) {
    throw std::invalid_argument(
        "number of indices must match tensor rank"
    );
  }

  for (std::size_t axis = 0; axis < rank(); ++axis) {
    if (indices[axis] >= shape_[axis]) {
      throw std::out_of_range("tensor index is outside its dimension");
    }
  }

  std::size_t result = 0;
  std::size_t stride = 1;

  for (std::size_t axis = rank(); axis > 0; --axis) {
    const std::size_t current_axis = axis - 1;

    result += indices[current_axis] * stride;
    stride *= shape_[current_axis];
  }

  return result;
}
```

### Connect to the overflow section

> This helper preserves the two-pass structure we just established: validate
> every coordinate first, then calculate the flat index. We are moving that
> already-safe logic, not changing its behavior.

### Live coding: overload `at()`

```cpp
[[nodiscard]] const double& at(
    const std::vector<std::size_t>& indices
) const {
  return data_[flat_index(indices)];
}

[[nodiscard]] double& at(
    const std::vector<std::size_t>& indices
) {
  return data_[flat_index(indices)];
}
```

### Important discussion
... write tests...


> Cool, now let’s scroll back up to our function and unpack a few important things.
> First, we just implemented an overload. Function overloading means defining multiple functions with the same name but different parameter lists or, for member functions, different const qualifications. When we call that name, the compiler examines the arguments and the object involved, then selects the matching version.
> Overloads cannot differ only by return type. In our case, these functions differ because one member function is const and the other is not:

- Calling `at()` on a const tensor selects the const overload.
- Calling it on a mutable tensor selects the mutable overload.
- A const reference allows reading without permitting assignment.
- A mutable reference allows mutation of the selected element.
- Neither overload allows the caller to resize `data_`, so the central
  shape-storage invariant remains protected.
- The reference remains valid only while its tensor and relevant vector storage
  remain alive and unmoved.

### Scalar and empty indexing

```cpp
const Tensor scalar({}, {7.0});
assert(scalar.at({}) == 7.0);
```

### Narration

> A scalar has rank zero, so it requires zero coordinates. The indexing loop
> performs no iterations and returns flat position zero, the scalar's only
> value.

For an empty tensor:

```cpp
const Tensor empty({0}, {});
```

any rank-correct coordinate must include an index for its sole axis, but no
index can be smaller than zero. Therefore every attempted element access throws
before touching storage.

### Assertions

```cpp
Tensor mutable_tensor(
    {2, 3},
    {1.0, 2.0, 3.0, 4.0, 5.0, 6.0}
);

mutable_tensor.at({1, 2}) = 42.0;
assert(mutable_tensor.at({1, 2}) == 42.0);
assert(mutable_tensor.shape() == std::vector<std::size_t>({2, 3}));
assert(mutable_tensor.numel() == 6);

const Tensor const_tensor({1}, {9.0});
assert(const_tensor.at({0}) == 9.0);
```

---

## 26:30-32:30 - Introduce the first reduction: `sum()`

## Intentional clip module 3

### Candidate Short title

`Why the Sum of an Empty Tensor Is Zero`

### Clip boundary

Begin with the hook below and end after deriving the empty sum. Define reduction
inside the clip so it does not depend on the rest of the episode.

### Hook

> What should `sum()` return when a tensor contains no values at all?

### Vertical-safe visual

```text
[1, 2, 3]  -> sum -> 6
[]         -> sum -> ?
```

### Subject introduction

> So far every tensor operation has selected one value or one piece of metadata.
> Now we want to ask a question about all stored values together: what is their
> sum?

### Define reduction before using the term

### Visual

```text
[1, 2, 3, 4]  ->  sum  ->  10
 four values                 one value
```

### Narration

> An operation that combines multiple input values into fewer output values is
> called a reduction. Sum, product, minimum, maximum, and mean are all common
> reductions.
>
> Today we will implement only the simplest form: combine every value in the
> tensor into one `double`.

### Why empty sum is zero

Build the sum incrementally:

```text
start = 0
after 1: 0 + 1 = 1
after 2: 1 + 2 = 3
after 3: 3 + 3 = 6
```

### Narration

> Zero is the additive identity. Adding zero leaves the current result
> unchanged. An empty tensor gives the loop no values to add, so the result
> remains at its initial value of zero.
>
> This mirrors the empty product. Products begin at one, the multiplicative
> identity. Sums begin at zero, the additive identity.

### Clip conclusion

> An empty sum performs no additions, so the accumulator remains at the additive
> identity: zero. Returning zero preserves the same summation rule for every
> tensor instead of inventing a special failure for the empty case.

### Live coding

```cpp
[[nodiscard]] double sum() const noexcept {
  double result = 0.0;

  for (const double value : data_) {
    result += value;
  }

  return result;
}
```

### Why `noexcept` is appropriate here

> This implementation performs no allocation, checked indexing, or operation
> that reports failure through a C++ exception. Marking it `noexcept` records
> that contract for callers and allows the compiler and generic library code to
> reason with that guarantee.

Do not claim that `noexcept` automatically makes the loop faster. The important
point here is the API guarantee.

### Assertions

```cpp
assert((Tensor({2, 3}, {1, 2, 3, 4, 5, 6}).sum() == 21.0));
assert((Tensor({}, {7.0}).sum() == 7.0));
assert((Tensor({1}, {7.0}).sum() == 7.0));
assert((Tensor({0}, {}).sum() == 0.0));
assert((Tensor({2, 0, 3}, {}).sum() == 0.0));
```

### Important limitation

> Returning a `double` is enough for today's data-structure lesson, but it stops
> operations from composing entirely in the tensor world. Later, a full
> reduction will return a rank-zero tensor and eventually participate in
> automatic differentiation.

---

## 32:30-34:30 - Review

### Visual recap

```text
Tensor
├── shape_ : vector<size_t>
├── data_  : vector<double>
│
├── scalar shape []       -> one value
├── zero-sized dimension  -> zero values
├── checked shape product -> no silent wraparound
├── dimension(axis)       -> checked metadata query
├── at(indices) const     -> const double&
├── at(indices)           -> double&
└── sum()                 -> full reduction to double
```

### Narration

> Our tensor can now represent scalars, singleton vectors, and empty tensors. We
> protected element counting from unsigned overflow, added checked dimension
> queries, and supported both const reads and mutable writes through overloads.
>
> We also implemented our first reduction by summing every stored value,
> including the empty case through the additive identity.
>
> The tensor is still deliberately small. It stores only doubles, owns only
> contiguous memory, and cannot combine with another tensor. Those limitations
> now give us the next reason to redesign it.

---

## 34:30-36:00 - Chapter 3 setup

### Visual

```text
[1, 2, 3] + [10, 20, 30]
          = [11, 22, 33]
```

### Narration

> Next, we will teach tensors to compute with one another. We will begin with
> elementwise arithmetic, extend those operations to scalars, and combine
> multiplication with reduction to build a dot product.
>
> By the end, we will use those pieces to express a complete linear prediction.
> Our tensor will stop being only a container and become a composable numerical
> object.

---

## 36:00-37:00 - Questions for Chapter 3

> Before the next chapter, pause here and make sure you can answer these
> questions:

1. Why does scalar shape `[]` imply one stored value rather than zero?
2. Why does shape `[2,0,3]` have rank three but contain zero values?
3. Why must shape multiplication be checked before the multiplication occurs?
4. Why does mutable `at()` return `double&` rather than `double`?
5. Why can individual values be mutable while the storage vector remains
   structurally protected?
6. What makes `sum()` a reduction?
7. Why is the sum of an empty tensor zero?
8. If two tensors have the same shape, what must an elementwise addition do to
   produce its output without changing either input?

---

## Clip inventory

### Clip 1

- **Title:** Why a Scalar Tensor Has One Value but No Dimensions
- **Core visual:** comparison of `[]`, `[1]`, and `[0]`
- **Target duration:** 40-60 seconds
- **Bridge:** full episode implements all three representations

### Clip 2

- **Title:** The Unsigned Overflow Bug Hiding in This Tensor Constructor
- **Core visual:** unsafe multiplication followed by division-based precheck
- **Target duration:** 35-55 seconds
- **Bridge:** full episode builds the overflow-safe constructor

### Clip 3

- **Title:** Why the Sum of an Empty Tensor Is Zero
- **Core visual:** accumulator beginning at the additive identity
- **Target duration:** 30-45 seconds
- **Bridge:** full episode introduces tensor reductions

### Recording requirements for all clips

- Keep essential code and diagrams within the centered vertical-safe region.
- Increase editor font size during the designated module.
- Avoid references such as "earlier in this episode."
- Pause briefly before the hook and after the conclusion.
- Record screen and presenter separately when possible.
- Let each clip finish its explanation before mentioning the full episode.
