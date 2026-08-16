# Chapter 1 — The Smallest Possible Tensor

## Video brief

- **Working title:** Building a Tensor from Scratch in One C++ File
- **Target runtime:** 31–34 minutes
- **Viewer promise:** build a small tensor data structure, understand why it
  needs shape and flat storage, enforce its central invariant, retrieve values
  using multidimensional coordinates, and test it using ordinary assertions
- **Only code file:** `main.cpp`

Compile and run with:

```sh
clang++ -std=c++23 -Wall -Wextra -Wpedantic main.cpp -o main
./main
```

Expected output:

```text
All assertions passed.
rank: 2
elements: 6
shape: [2, 3]
flat data: 1 2 3 4 5 6
value at [1, 2]: 6
```

---

## 00:00–01:15 — Series cold open

### Rapid visual sequence

Open on a complete training step:

```cpp
Tensor prediction = model(input);
Tensor loss = cross_entropy(prediction, target);

optimizer.zero_grad();
loss.backward();
optimizer.step();
```

Then visually descend through the implementation behind those lines:

1. `model(input)` becomes `input.matmul(weights) + bias`;
2. `matmul` becomes three nested CPU loops;
3. a multidimensional tensor lookup becomes an index into one flat
   `std::vector<double>`;
4. `loss.backward()` becomes a computation graph with accumulated gradients;
5. the CPU matrix loop becomes a CUDA kernel launch:

   ```cpp
   matmul_kernel<<<grid, block>>>(left, right, output);
   ```

6. show a grid of GPU thread blocks, global-memory loads, and a profiler
   timeline comparing the CPU and GPU kernels;
7. return to a falling training-loss curve, an attention matrix, and a small
   transformer producing tokens.

The sequence should feel like opening a finished machine and zooming through
its layers until only a flat allocation remains—not like advancing through a
list of vocabulary words.

### Narration

> Welcome to *Deep Learning, All the Way Down*—a journey into deep learning,
> built from first principles in C++.
>
> This series is for you if you have trained a few models and found
> yourself getting increasingly increasingly curious about the low-level 
> systems that power modern machine-learning frameworks.
>
> A modern deep-learning framework can train a model in a handful of lines. That
> convenience is powerful—but it hides almost everything that makes the model
> work.
>
> In this series, we are going to open that black box and rebuild its essential
> machinery in modern C++, using nothing but the standard library. 
> 
> We will follow a structured and systematic process where every session, the code we write will be self-contained and functional. We will depend on unit tests and benchmarks to justify our decisions.
>
> We will start with numbers in memory and turn them into tensors. We will teach
> those tensors to track gradients, assemble them into neural networks, and
> train models of our own.
>
> Then we will push the same ideas further—through attention, transformers, and
> language models.
>
> When the CPU becomes the bottleneck, we will cross into GPU programming,
> write CUDA kernels ourselves, and measure what the hardware is actually doing.
>
> The clone will be part of our methodology but it won't be the main goal. Througout this journey, our main goal will remain the same: to build deep, intuitive udnerstanding on the mathematics, data structures, systems decisions, and performance tradeoffs involved in deep learning systems.
>
> That's what this series is all about. And that brings us to the first episode. It all begins with one object: a tensor. By the end of this episode, we will have a simple, rudimentary implementation of a tensor, which we will be refinining, extending and optimizing over the next few episodes. 
>
> Let's dive in!

### Transition

Cut directly from the final word “tensor” to the scalar/vector/matrix visual.
Do not insert a title-card biography or channel introduction between them.

---

## 01:15–02:45 — Very short tensor introduction

### Visual 1: numbers gain dimensions

Put these on screen one at a time:

```text
scalar                 vector                 matrix

  7                   [1 2 3]              [1 2 3]
                                             [4 5 6]

shape: []              shape: [3]           shape: [2,3]
rank:  0               rank:  1             rank:  2
```

### Narration

> A tensor is a multidimensional collection of numbers. A scalar has no axes,
> a vector has one, and a matrix has two. Higher-rank tensors continue the same
> idea rather than introducing a fundamentally different kind of object.

### Visual 2: logical form versus physical storage

Animate the matrix flattening:

```text
logical tensor                    physical storage

[1 2 3]                           [1 2 3 4 5 6]
[4 5 6]

shape = [2,3]                     one flat allocation
```

### Narration

> The shape tells us how to interpret the values. The values themselves do not
> need to be stored in nested C++ vectors. We can keep one flat allocation and
> preserve the multidimensional meaning separately as shape metadata.
>
> Today we will implement exactly that—and nothing more—in one `main.cpp` file.

### Presenter note

Keep this introduction under ninety seconds. Do not discuss strides, devices,
dtypes, autograd, or PyTorch internals yet.

---

## 02:45–04:15 — State the deliberately small contract

### On screen

```text
Chapter 1 Tensor

✓ stores double values
✓ stores one or more positive dimensions
✓ owns one flat vector
✓ reports shape, rank, and number of elements
✓ rejects mismatched shape and data
✓ reads values using checked multidimensional coordinates

Later: scalars, empty tensors, mutation, operations, generic types, autograd
```

### Narration

> This is not our final tensor. It supports `double`, requires at least one
> positive dimension, and owns contiguous flat storage. These limitations let
> us isolate the central representation before edge cases and abstractions begin
> competing for attention.
>
> Scalars and empty tensors are real and useful. We are postponing them, not
> declaring them invalid.

---

## 04:15–06:45 — Start with the state

### Live coding

```cpp
#include <cstddef>
#include <vector>

class Tensor {
private:
  std::vector<std::size_t> shape_;
  std::vector<double> data_;
};
```

### Narration

> Our tensor owns two vectors. `shape_` stores the extent of every axis. For a
> two-by-three matrix it contains `{2, 3}`. `data_` stores the six numerical
> values in one flat sequence.
>
> We use `std::size_t` for dimensions because dimensions describe sizes and
> indices. We use `double` only to keep this first implementation concrete.

### Discussion prompts

- Why is `[2,3]` insufficient without the values?
- Why are six flat values insufficient to determine the unique shape?
- Could the same six values represent `[6]`, `[2,3]`, or `[1,2,3]`?

---

## 06:45–11:15 — Construct a valid tensor

### Live coding

First add the constructor signature:

```cpp
public:
  Tensor(
      std::vector<std::size_t> shape,
      std::vector<double> data
  )
      : shape_(std::move(shape)), data_(std::move(data)) {
  }
```

Add:

```cpp
#include <utility>
```

### Narration

> The constructor receives both vectors by value and moves those local vectors
> into the object. We will examine copies and moves carefully later. For now,
> the important point is that the tensor owns its shape and data after
> construction.

Then establish the chapter's dimensional restrictions:

```cpp
if (shape_.empty()) {
  throw std::invalid_argument(
      "chapter 1 tensors must have at least one dimension"
  );
}

std::size_t expected_elements = 1;
for (const std::size_t dimension : shape_) {
  if (dimension == 0) {
    throw std::invalid_argument(
        "chapter 1 tensor dimensions must be positive"
    );
  }
  expected_elements *= dimension;
}
```

Add:

```cpp
#include <stdexcept>
```

### Narration

> The number of elements required by a shape is the product of its dimensions.
> Shape `[2,3]` requires two times three, or six, values.
>
> The product begins at one because one is the multiplicative identity. We will
> revisit why this matters when scalar tensors enter the design.

Complete the invariant:

```cpp
if (expected_elements != data_.size()) {
  throw std::invalid_argument("tensor shape does not match its data");
}
```

### Narration

> This is the class's central invariant: the product of the dimensions must
> equal the number of stored values. If construction succeeds, every later
> method can rely on that fact.

### Important limitation

Point at:

```cpp
expected_elements *= dimension;
```

Say:

> This multiplication can overflow for enormous shapes. Chapter 1 is restricted
> to small examples. We will later reproduce the failure and implement checked
> shape arithmetic rather than quietly pretending this is production-safe.

---

## 11:15–14:45 — Expose read-only metadata

### Live coding

```cpp
[[nodiscard]] const std::vector<std::size_t>& shape() const noexcept {
  return shape_;
}

[[nodiscard]] const std::vector<double>& data() const noexcept {
  return data_;
}

[[nodiscard]] std::size_t rank() const noexcept {
  return shape_.size();
}

[[nodiscard]] std::size_t numel() const noexcept {
  return data_.size();
}
```

### Narration

> Rank is the number of axes, so it is the number of entries in the shape.
> `numel`—short for number of elements—is the number of stored values.
>
> The two vector accessors return const references. Returning references avoids
> copying the vectors. Making them const prevents callers from resizing them and
> breaking the invariant we just established.
>
> The member functions are const because they do not change the tensor.
> 
> `noexcept` makes a second promise: these functions will not let an exception
> escape. Knowing that a call cannot throw may let the compiler simplify its
> exception-handling paths, and it lets other C++ code safely choose operations
> that rely on that guarantee. If an exception does escape anyway, the program
> terminates, so we should use `noexcept` only when we can uphold the promise.
> `[[nodiscard]]` asks the compiler to warn when a caller requests a result and
> then ignores it.

### Discussion topic

Privacy alone does not establish correctness. The constructor establishes the
invariant; private fields and read-only access help preserve it afterward.

---

## 14:45–21:15 — Add checked multidimensional indexing

### Visual

```text
tensor coordinate                 flat storage position

[0,0]  →  0                      [1 2 3 4 5 6]
[0,2]  →  2
[1,0]  →  3
[1,2]  →  5

For shape [2,3]:
flat index = row × 3 + column
```

Then show the distance moved by each axis:

```text
shape:   [2,3]
strides: [3,1]
```

### Narration

> Shape gives the flat values multidimensional meaning, but we need a rule that
> converts a tensor coordinate into a flat-vector index.
>
> In row-major storage, the final axis changes one element at a time. Moving one
> column advances one flat value. Moving to the next row skips an entire row of
> three values. For shape `[2,3]`, coordinate `[row,column]` therefore maps to
> `row times three plus column`.

### Visual derivation with a rank-three tensor

Before writing the loop, use a shape large enough to reveal the general rule:

```text
shape = [2, 3, 4]

2 blocks
└── each block contains 3 rows
    └── each row contains 4 values

flat storage:

block 0                              block 1
┌──────────────────────────────┐     ┌──────────────────────────────┐
 0  1  2  3 | 4  5  6  7 | 8  9 10 11 | 12 13 14 15 | 16 17 18 19 | 20 21 22 23
└──────────────────────────────┘     └──────────────────────────────┘
```

Reveal the distance moved by increasing each coordinate by one:

```text
coordinate: [block, row, column]

increase column by 1 → skip 1 value
increase row    by 1 → skip 4 values
increase block  by 1 → skip 3 × 4 = 12 values

shape:   [ 2, 3, 4]
strides: [12, 4, 1]
```

Now map coordinate `[1,2,3]`:

```text
block contribution  = 1 × 12 = 12
row contribution    = 2 ×  4 =  8
column contribution = 3 ×  1 =  3
                                  ──
flat index                       = 23
```

### Narration

> Each coordinate contributes its index multiplied by the number of flat values
> one step along that axis must skip. The final axis skips one value. The axis
> before it skips one complete final-axis row. The axis before that skips one
> complete block formed by both axes to its right.
>
> This gives us the general formula: the flat index is the sum of each
> coordinate multiplied by its stride. We can discover those strides while
> walking from the final axis toward the first. We begin with stride one, use
> it for the current axis, and then multiply it by the current dimension to
> obtain the stride of the next axis to the left.

### First attempt: the natural reverse loop

Write the loop in the form many C++ programmers try first:

```cpp
for (std::size_t axis = rank() - 1; axis >= 0; --axis) {
  flat_index += indices[axis] * stride;
  stride *= shape_[axis];
}
```

Compile with warnings enabled:

```sh
clang++ -std=c++23 -Wall -Wextra -Wpedantic main.cpp -o main
```

Depending on the compiler and surrounding code, point out the warning that an
unsigned comparison against zero is always true. Do not run the broken program
unless the demonstration is isolated and controlled.

### Walk through the failure

For rank three:

```text
axis = 2  → condition 2 >= 0 is true
axis = 1  → condition 1 >= 0 is true
axis = 0  → condition 0 >= 0 is true
--axis
```

At this point, `axis` does not become `-1`:

```text
std::size_t range:
0, 1, 2, ... , SIZE_MAX

0 - 1 wraps to SIZE_MAX
```

Therefore:

```text
axis = SIZE_MAX → condition axis >= 0 is still true
```

The loop continues and attempts to index the vectors with an enormous invalid
axis.

### Narration

> `std::size_t` is unsigned: it cannot represent negative numbers. The condition
> `axis >= 0` is therefore true for every value the type can hold. Decrementing
> zero wraps around to the largest representable `std::size_t`; it does not
> produce negative one.
>
> We need a loop whose condition is checked before performing the subtraction
> that produces the actual axis.

### Derive the safe reverse-loop form

```cpp
for (std::size_t axis = rank(); axis > 0; --axis) {
  const std::size_t current_axis = axis - 1;

  flat_index += indices[current_axis] * stride;
  stride *= shape_[current_axis];
}
```

Trace it for rank three:

```text
axis = 3 → 3 > 0 → current_axis = 2
axis = 2 → 2 > 0 → current_axis = 1
axis = 1 → 1 > 0 → current_axis = 0
axis = 0 → 0 > 0 is false → stop
```

### Narration

> The loop variable now represents one past the axis we intend to process. Its
> values are three, two, and one, all of which safely satisfy `axis > 0`. Inside
> the body, subtracting one produces the real axes two, one, and zero. Once the
> loop variable reaches zero, the condition fails before another subtraction can
> happen.

### Why not `rbegin()` and `rend()`?

Show the valid iterator-based alternative:

```cpp
auto index = indices.rbegin();
auto dimension = shape_.rbegin();

for (; index != indices.rend(); ++index, ++dimension) {
  flat_index += *index * stride;
  stride *= *dimension;
}
```

### Narration

> Reverse iterators would also work, and they avoid unsigned countdown
> arithmetic entirely. We are not avoiding them because they are slower or
> incorrect.
>
> Here, however, we must traverse two vectors in lockstep: the coordinate and
> the shape. That means maintaining two reverse iterators and advancing both on
> every iteration. A numeric axis lets one value address both vectors, and it
> makes the relationship `indices[axis]` against `shape_[axis]` explicit—which
> is useful while teaching tensor coordinates and bounds.
>
> In production code, either form can be reasonable. We are choosing the index
> form because it makes this particular algorithm easier to read, while also
> exposing an important C++ lesson about unsigned reverse loops.

### Live coding

```cpp
[[nodiscard]] double at(
    const std::vector<std::size_t>& indices
) const {
  if (indices.size() != rank()) {
    throw std::invalid_argument("number of indices must match tensor rank");
  }

  std::size_t flat_index = 0;
  std::size_t stride = 1;

  for (std::size_t axis = rank(); axis > 0; --axis) {
    const std::size_t current_axis = axis - 1;

    if (indices[current_axis] >= shape_[current_axis]) {
      throw std::out_of_range("tensor index is outside its dimension");
    }

    flat_index += indices[current_axis] * stride;
    stride *= shape_[current_axis];
  }

  return data_[flat_index];
}
```

### Walk through coordinate `[1,2]`

```text
Start: flat_index = 0, stride = 1

axis 1:
flat_index += 2 × 1  → 2
stride *= 3          → 3

axis 0:
flat_index += 1 × 3  → 5
stride *= 2          → 6

data_[5] = 6
```

### Narration

> We walk from the final axis toward the first because the final axis has stride
> one. After processing an axis, multiplying the running stride by that axis's
> size tells us how many flat values the next axis skips.
>
> The method first verifies that the number of coordinates equals the rank. It
> then checks every coordinate against its dimension before reading storage.
>
> This version recalculates strides for every lookup. It is simple and correct,
> but not necessarily efficient. We can store strides as tensor metadata in a
> later redesign after their purpose is concrete.

### Important C++ details

- The reverse loop uses `axis > 0`. Writing `axis >= 0` would never terminate
  because `std::size_t` is unsigned.
- Returning a `double` by value is inexpensive and avoids introducing borrowed
  element references yet.
- Mutable indexing and checked arithmetic for enormous shapes remain deferred.

---

## 21:15–23:45 — Use the tensor

### Live coding in `main()`

```cpp
const Tensor matrix(
    {2, 3},
    {
        1.0, 2.0, 3.0,
        4.0, 5.0, 6.0,
    }
);

std::cout << "rank: " << matrix.rank() << '\n';
std::cout << "elements: " << matrix.numel() << '\n';
std::cout << "value at [1, 2]: " << matrix.at({1, 2}) << '\n';
```

Add the short loops from the completed `main.cpp` to print shape and flat data.

Compile:

```sh
clang++ -std=c++23 -Wall -Wextra -Wpedantic main.cpp -o main
./main
```

### Narration

> The tensor has rank two because its shape contains two axes. It contains six
> elements because the constructor verified that the two-by-three shape agrees
> with the six stored values.
>
> Coordinate `[1,2]` means row one, column two. It maps to flat position five
> and returns six. The tensor can now be read through its logical
> multidimensional interface rather than behaving like a decorated vector.

---

## 23:45–28:15 — Test with ordinary assertions

### Narration

> We are keeping Chapter 1 to one file, so we will use ordinary assertions
> instead of introducing a testing dependency. The assertions are not a
> production test architecture; they are enough to make today's claims
> executable.

### Live coding

Add:

```cpp
#include <cassert>
```

Create `run_tests()` before `main()`:

```cpp
void run_tests() {
  const Tensor matrix(
      {2, 3},
      {1.0, 2.0, 3.0, 4.0, 5.0, 6.0}
  );

  assert(matrix.rank() == 2);
  assert(matrix.numel() == 6);
  assert((matrix.shape() == std::vector<std::size_t> {2, 3}));
  assert(matrix.data()[0] == 1.0);
  assert(matrix.data()[5] == 6.0);
  assert(matrix.at({0, 0}) == 1.0);
  assert(matrix.at({0, 2}) == 3.0);
  assert(matrix.at({1, 0}) == 4.0);
  assert(matrix.at({1, 2}) == 6.0);
}
```

Explain the extra parentheses:

> The expression contains a comma inside the vector initializer. The extra
> parentheses ensure the assertion macro receives the entire comparison as one
> argument.

Add the rejection check:

```cpp
bool rejected_invalid_tensor = false;

try {
  const Tensor invalid({2, 3}, {1.0, 2.0});
} catch (const std::invalid_argument&) {
  rejected_invalid_tensor = true;
}

assert(rejected_invalid_tensor);
std::cout << "All assertions passed.\n";
```

Call `run_tests()` at the beginning of `main()`.

Use the completed `main.cpp` to add two indexing failure checks:

```text
wrong number of coordinates → std::invalid_argument
coordinate outside dimension → std::out_of_range
```

### Important discussion

- Assertions can be disabled when `NDEBUG` is defined.
- This is an intentionally lightweight teaching harness.
- Later chapters can introduce a proper test executable and framework when the
  growing behavior makes them worthwhile.
- Tests should verify public behavior rather than inspect private fields.

---

## 28:15–30:45 — Review and retrieve

### Visual recap

```text
Tensor
├── shape_ = [2,3]
└── data_  = [1,2,3,4,5,6]

Invariant:
product(shape_) == data_.size()

Indexing:
flat_index = Σ(indices[axis] × stride[axis])
```

### Narration

> We now have a tensor in one C++ file. It owns flat numerical storage and shape
> metadata. Its constructor prevents the shape and storage from contradicting
> each other. Its public queries expose metadata without allowing callers to
> resize the internal vectors. Checked indexing maps multidimensional
> coordinates into the flat vector. And a small assertion suite verifies the
> behavior every time we run the program.

Ask viewers to pause and answer:

1. What are the rank and element count of shape `[2,3,4]`?
2. Why do six values not uniquely determine shape `[2,3]`?
3. What invariant does the constructor establish?
4. Why does `data()` return a const reference?
5. For shape `[2,3]`, why does coordinate `[1,2]` map to flat position five?

---

## 30:45–31:45 — Chapter 2 setup

### Visual

```text
[]   scalar?
[1]  one-element vector?
[0]  empty vector?
```

### Narration

> Our small contract currently rejects all three interesting edge cases. In the
> next chapter, we will distinguish a scalar, a singleton vector, and an empty
> vector. That will force us to understand rank zero, the empty product, and why
> reductions need mathematical identity values.

## Optional viewer exercises

1. Construct a rank-three tensor with shape `[2,2,3]` and verify its metadata.
2. Add a `dimension(axis)` query that rejects an out-of-range axis.
3. Deliberately change one assertion and observe the failure.
4. Explain why mutable access to the entire data vector could violate the
   tensor's invariant.
