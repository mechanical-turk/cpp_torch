# Episode 5 - Broadcasting in C++

## Video brief

* **Working title:** Implementing Broadcasting in C++: One Rule for Every
  Compatible Shape | Deep Learning, All the Way Down #5
* **Target runtime:** 12-16 minutes. This is more mechanism than a
  scalar-only fix would need: a real shape-alignment rule, per-operand
  effective strides, and an N-D walk over the output. Don't force it back
  down to a narrower scope to hit a smaller number.
* **Viewer promise:** implement the actual broadcasting rule — the one that
  lets a `[3]` tensor combine with a `[2,3]` tensor, not just a special case
  for scalars — and use it for something real: centering a batch of
  observations by subtracting a per-feature offset.
* **Starting point:** the reference implementation at
  `/Users/keremkazan/Documents/Projects/deep-learning-all-the-way-down/main.cpp`,
  exactly as Episode 4 leaves it (commit `022c750`, "chapter 04 - matmul").
  `main()` ends on the `// broadcasting.` placeholder comment right after
  `pred_23`; pick up from there. The code still carries scratch
  test-numbered names — `matmul_23`, `pred_23` — since Episode 4 never
  cleaned them up. The first live-coding beat below renames them on screen.
* **Only code file:** `main.cpp`
* **In scope:** general N-D broadcasting between any two tensors whose
  shapes are compatible under the align-from-the-right, size-one-stretches
  rule, applied to every existing elementwise operation through one shared
  code path.
* **Deferred further out:** broadcasting a batch dimension through
  `matmul()` itself, tensors that store their own strides as reusable views
  instead of computing them per call, a loss function, gradients, autograd,
  dtypes, dependencies, and build tooling.

## 00:00-00:45 - One rule, not a special case

### On screen

Begin speaking immediately with
[`assets/shapes-still-rejected.png`](assets/shapes-still-rejected.png). Keep
it visible through this entire beat; both examples on screen are the two
cases the narration walks through in one breath.

```text
input [2,1]  +  bias [2,1]   <- accepted today, same shape
input [2,1]  +  bias []      <- still rejected today, not the same shape
```

### Narration

> Welcome back to *Deep Learning, All the Way Down*.
>
> Right now, every elementwise operation on our tensor expects both sides to
> have exactly the same shape. So a `[2,1]` input plus a `[2,1]` bias works
> fine, though that's just a hack we added to manually scale the scalar up
> to the correct shape.
> If we don't do that hack, and just work with the bias in its original scalar form, the addition fails, even though it shouldn't. There's no reason why our library shouldn't deduce that our intention is to treat this scalar as if it were a 2x1 vector here.
> 
> So today, we're going to fix that by implementing broadcasting.

---

## 00:45-01:30 - Pick up where Episode 4 left off

### Live coding

Episode 4 ends on:

```cpp
const Tensor matmul_23 = inputs.matmul(weights);

// ...

const Tensor expanded_bias(
    {2, 1},
    {
      0.5,
      0.5
    }
);
const Tensor pred_23 = matmul_23 + expanded_bias;

// broadcasting.
```

Two cleanups before touching broadcasting itself. `matmul_23` and `pred_23`
were scratch names left over from testing — rename them to `linear` and
`predictions`. And `expanded_bias` only exists because `linear + bias`
doesn't work yet; delete it. `main()` already has a scalar `bias` from the
dot-product prediction earlier in the function, so use that directly:

```cpp
const Tensor linear = inputs.matmul(weights);

const Tensor invalid = linear + bias;
```

Compile and run.

```text
elementwise operations require equal shapes
```

Delete the deliberate failure before continuing.

### Narration

> When the shapes don't match exactly, our current check rejects them. 
> To fix that, we need to answer two questions. 
> 
> First, when are two different shapes 
> compatible? And second, once we determine they are, how do we align them and make them work?

---

## 01:30-03:15 - The alignment rule

### On screen

```text
align from the right, pad missing axes with 1

linear   [2, 1]              inputs   [2, 3]
bias     [   ]  ->  [1, 1]   offset   [   3]  ->  [1, 3]

compare each aligned pair: equal, or one of them is 1

[2,1] vs [1,1]:  2 vs 1 -> stretch to 2   1 vs 1 -> equal
result: [2, 1]

[2,3] vs [1,3]:  2 vs 1 -> stretch to 2   3 vs 3 -> equal
result: [2, 3]
```

### Narration

> Start by lining the two shapes up from the right, just like we did with the
> shared inner dimension in matrix multiplication. If one shape is missing an
> axis, treat that axis as having size 1. Then compare each pair. They're
> compatible if the sizes match, or if one of them is 1. In that case, the 1
> can stretch to match the other side. The output takes the larger size at each
> axis.
>
> A rank-zero tensor is the simplest case. It has no axes at all, so every
> missing axis behaves like a 1. That means a scalar can broadcast against any
> shape using the exact same rule.

### On screen: the rejection case

```text
[2] vs [3]

dimension 0: 2 vs 3 -> neither equal nor 1 -> incompatible
```

> Of course, not every pair of shapes is compatible. If the sizes differ and
> neither side is 1, there's no valid way to line them up, so we reject the
> operation.

---

## 03:15-08:45 - Implement the general rule

### Narration: what has to change

> `elementwise_binary` currently does two things: it checks that the shapes
> match exactly, then walks both tensors in lockstep. Broadcasting changes that.
> We need to figure out the output shape for two compatible inputs, and we need
> a way for an operand to reuse the same value as the output moves along an
> axis it doesn't really have. To do that, we need each tensor's strides: how
> far we move in flat storage when we advance by one position along an axis.
> `matmul()` already does this kind of arithmetic by hand with `row * cols +
> column`. Let's pull the general version into its own method.

### Live coding: compute this tensor's own strides

```cpp
[[nodiscard]] std::vector<std::size_t> strides() const {
  std::vector<std::size_t> result(shape_.size());
  std::size_t stride = 1;

  for (std::size_t axis = shape_.size(); axis-- > 0;) {
    result[axis] = stride;
    stride *= shape_[axis];
  }

  return result;
}
```

### Narration

> This is the same row-major indexing math, computed once for however many
> dimensions the tensor has.

### Narration: the alignment rule as code

> Now let's turn the alignment rule into code. We already know the output
> has `rank` axes, and each shape is missing however many of those axes it's
> shorter by. Work that out once per operand, then walk the output's axes
> left to right, using that offset to find each operand's real axis, if it
> has one there.
>
> One thing to flag before the code: this is going to be a `static` member
> function, and so is the next one we write. Everything we've written on
> `Tensor` so far has worked on a specific instance — reading its `shape_`,
> its `data_`. This function doesn't. It only ever looks at the two shape
> vectors it's handed; it has no tensor to be a method of yet. `static`
> marks that honestly: it's a function that lives on `Tensor` because it's
> about tensor shapes, not because it needs a `this`.

### Live coding: the alignment rule as code

```cpp
[[nodiscard]] static std::vector<std::size_t> broadcast_shape(
    const std::vector<std::size_t>& left,
    const std::vector<std::size_t>& right
) {
  const std::size_t rank = std::max(left.size(), right.size());
  std::vector<std::size_t> result(rank);

  const std::size_t left_offset = rank - left.size();
  const std::size_t right_offset = rank - right.size();

  for (std::size_t axis = 0; axis < rank; ++axis) {
    const bool left_has_axis = axis >= left_offset;
    const bool right_has_axis = axis >= right_offset;

    std::size_t left_dim = 1;
    if (left_has_axis) {
      const std::size_t left_axis = axis - left_offset;
      left_dim = left[left_axis];
    }

    std::size_t right_dim = 1;
    if (right_has_axis) {
      const std::size_t right_axis = axis - right_offset;
      right_dim = right[right_axis];
    }

    const bool sizes_match = left_dim == right_dim;
    const bool left_can_stretch = left_dim == 1;
    const bool right_can_stretch = right_dim == 1;

    if (!sizes_match && !left_can_stretch && !right_can_stretch) {
      throw std::invalid_argument(
          "cannot broadcast - shape mismatch at dimension " +
          std::to_string(axis)
      );
    }

    result[axis] = std::max(left_dim, right_dim);
  }

  return result;
}
```

### Narration

> `left_offset` and `right_offset` are each shape's missing-axis count —
> how many axes `rank` has that the shape itself doesn't. Compute those once,
> then walk the output's axes left to right.
>
> `left_has_axis` asks the direct question: has the walk reached `left`'s
> real axes yet? While `axis` is still less than `left_offset`, we're still
> in the padding region — that's the implicit 1 "align from the right"
> described. Once `axis` reaches `left_offset`, `left_axis` converts the
> output axis back into `left`'s own indexing, and `left_dim` reads the real
> value. Same for the right operand, against its own offset.
>
> Notice this loop runs left to right even though the rule aligns from the
> right — that's fine, because `left_offset` and `right_offset` already
> encode the alignment. Every axis's answer only depends on those two
> numbers, not on any neighboring axis, so unlike `strides()`, the order we
> visit them in doesn't matter.
>
> Once we have both dimensions, `sizes_match`, `left_can_stretch`, and
> `right_can_stretch` are the three ways a pair is allowed to combine, named
> instead of buried in one compound condition. If none of them hold, we
> throw and report the axis that failed. Otherwise the larger of the two —
> which is just the non-1 one, when they don't already match — becomes the
> output size at this axis.

### Narration: reusing a value without copying it

> At this point we know the output shape, but we still need to map an output
> coordinate back to each operand. That's where strides become useful. On an
> axis that gets broadcast, we give the operand an effective stride of zero.
> So as the output coordinate changes along that axis, multiplying by the
> stride still contributes zero to the input index. The input keeps reading the
> same element over and over. That handles both missing axes and size-one axes,
> because in both cases we want to reuse a value instead of advancing.
>
> Same reason this one's `static` too — it only works from a shape, a
> stride list, and a target rank, all passed in. No instance required.

### Live coding: effective strides against the broadcast rank

```cpp
[[nodiscard]] static std::vector<std::size_t> effective_strides(
    const std::vector<std::size_t>& shape,
    const std::vector<std::size_t>& own_strides,
    const std::size_t target_rank
) {
  std::vector<std::size_t> result(target_rank, 0);
  const std::size_t offset = target_rank - shape.size();

  for (std::size_t axis = 0; axis < shape.size(); ++axis) {
    if (shape[axis] != 1) {
      result[offset + axis] = own_strides[axis];
    }
  }

  return result;
}
```

### Narration

> We start every effective stride at zero, which means the index stays put
> along that axis. Then, for any real axis with more than one element, we copy
> in the tensor's actual stride. A scalar has an empty shape, so this loop does
> nothing and every effective stride stays zero. The scalar case comes out of
> the same code automatically.
>
> Worth asking: for a size-one axis, wouldn't the tensor's real stride have
> worked anyway? Its own coordinate can only ever be 0 there, so any stride
> times 0 is still 0. True — but this function never learns what coordinate
> it's about to be handed. It only knows this operand's own shape and the
> output's rank, not the other operand's shape, so it can't tell whether
> this axis is about to stay size one in the output or get stretched to
> match something bigger on the other side. If it stays one, the coordinate
> is always 0 and the real stride would've been harmless. If it gets
> stretched, the coordinate ranges past 0, and the real stride — valid only
> for a single position — starts reading into memory that was never part of
> this axis. Zero is correct either way. The real stride is only correct in
> one of those two futures, and this function has to commit to an answer
> before it knows which one it's in.

### Narration: walking the output

> Now we have the output shape and one effective stride per output axis for
> each operand. What's left is to visit every output position, find the
> matching element from each operand, and apply the operation. That's two
> separate jobs — "given a coordinate, which flat index does it map to" and
> "given a coordinate, what's the next one" — so let's write each as its own
> small function before we wire them together.

### Live coding: coordinate to flat index

```cpp
[[nodiscard]] static std::size_t stride_offset(
    const std::vector<std::size_t>& coordinate,
    const std::vector<std::size_t>& effective_strides
) {
  std::size_t index = 0;
  for (std::size_t axis = 0; axis < coordinate.size(); ++axis) {
    index += coordinate[axis] * effective_strides[axis];
  }
  return index;
}
```

### Narration

> This is the same idea as the `at()` we already have, just generalized:
> multiply each coordinate by its matching stride and add them up. `at()`
> always uses a tensor's own strides for its own coordinate. This version
> takes the strides as an argument instead, so we can hand it either
> operand's *effective* strides — real or zeroed — for the same output
> coordinate.

### Live coding: advancing the coordinate

> Second function: given a coordinate and the shape it's walking, move to
> the next one. Increment the rightmost axis. If that overflows its size,
> reset it to zero and carry into the axis to its left — a car odometer,
> one digit per axis.

```cpp
static void advance_coordinate(
    std::vector<std::size_t>& coordinate,
    const std::vector<std::size_t>& shape
) {
  for (std::size_t axis = coordinate.size(); axis-- > 0;) {
    if (++coordinate[axis] < shape[axis]) {
      return;
    }
    coordinate[axis] = 0;
  }
}
```

### Narration

> `++coordinate[axis]` increments that axis and immediately gives back its
> new value, so the `if` is checking the axis *after* incrementing it. If
> that's still in bounds, we're done — return. If not, this axis rolled
> over: reset it to zero and let the loop continue to the axis on its left,
> which is the carry. Walking `axis` from the last one down to the first is
> what makes the rightmost axis the one that changes fastest, same as
> `strides()`.
>
> Trace one operand through a `[2,3]` output where its effective strides are
> `[0, 1]` — axis 0 broadcast, axis 1 real. `coordinate` walks `[0,0]`,
> `[0,1]`, `[0,2]`, giving indices `0`, `1`, `2`. Then axis 1 overflows and
> carries: `coordinate` becomes `[1,0]`. Axis 0 just advanced from `0` to
> `1`, but its stride is `0`, so `stride_offset` comes out as `0` again —
> the same element we read at the very first position. That's the entire
> payoff: this operand only has 3 real elements, the output has 6
> positions, and the zero stride is what sends the second half of the walk
> back over the same 3 elements instead of reading past the end of the
> array.

### Live coding: rewrite the shared traversal

Replace `elementwise_binary` entirely:

```cpp
[[nodiscard]] Tensor elementwise_binary(
    const Tensor& other,
    const auto& operation
) const {
  const std::vector<std::size_t> result_shape =
      broadcast_shape(shape_, other.shape_);

  const std::vector<std::size_t> left_strides =
      effective_strides(shape_, strides(), result_shape.size());
  const std::vector<std::size_t> right_strides =
      effective_strides(other.shape_, other.strides(), result_shape.size());

  std::size_t result_numel = 1;
  for (const std::size_t dim : result_shape) {
    result_numel *= dim;
  }

  std::vector<double> result_data(result_numel);
  std::vector<std::size_t> coordinate(result_shape.size(), 0);

  for (std::size_t flat = 0; flat < result_numel; ++flat) {
    const std::size_t left_index = stride_offset(coordinate, left_strides);
    const std::size_t right_index = stride_offset(coordinate, right_strides);

    result_data[flat] = operation(data_[left_index], other.data_[right_index]);

    advance_coordinate(coordinate, result_shape);
  }

  return Tensor(result_shape, std::move(result_data));
}
```

### Narration

> With both helpers written, the loop just says what it means: for every
> flat position, look up where each operand's data actually lives, combine
> the two values, then step to the next coordinate. `coordinate` itself
> starts at all zeros — the very first output position — and
> `advance_coordinate` walks it through every position exactly once before
> `flat` reaches `result_numel`.
>
> And that's all the elementwise operators need. `operator+`, `operator-`, and
> `operator*` already go through `elementwise_binary`, so they all pick up
> broadcasting from this one change.

---

## 08:45-10:45 - Verify against a real case, not just the bias

### Live coding: the bias case still works

```cpp
const Tensor predictions = linear + bias;

assert((
    predictions.data() ==
    std::vector<double>{3.5, 0.0}
));
```

> These are the same values we got in Episode 4 by copying the bias into a
> full column, except now there's no copy. That's the scalar case. Next let's
> try something a scalar-only implementation couldn't handle.

### Live coding: centering a batch by a per-feature offset

```cpp
const Tensor feature_offset({3}, {1.0, 1.0, 0.5});

const Tensor centered = inputs - feature_offset;

assert((
    centered.data() ==
    std::vector<double>{3.0, 2.0, 1.5, 0.0, 1.0, 0.0}
));
```

### On screen

```text
inputs                    feature_offset      centered

[4.0, 3.0, 2.0]                                [3.0, 2.0, 1.5]
[1.0, 2.0, 0.5]    -      [1.0, 1.0, 0.5]  =    [0.0, 1.0, 0.0]

offset [3] aligns as [1,3], stretches to [2,3]: the same three values
subtract from every row.
```

### Narration

> `feature_offset` has shape `[3]`, while `inputs` has shape `[2,3]`. The
> offset lines up with the last axis, and its missing leading axis behaves like
> a 1, so that row is reused for both observations. We subtract the same three
> feature offsets from every row without writing a loop over rows or expanding
> the offset into a full `[2,3]` tensor first.

### Live coding: confirm the incompatible case still rejects

```cpp
bool rejected_incompatible_shapes = false;

try {
  const auto invalid =
      Tensor({2}, {1.0, 2.0}) + Tensor({3}, {1.0, 2.0, 3.0});
} catch (const std::invalid_argument&) {
  rejected_incompatible_shapes = true;
}

assert(rejected_incompatible_shapes);
```

> Two and three can't broadcast together because the sizes differ and neither
> side is 1. Broadcasting can reuse an existing value across an axis, but it
> can't invent a compatible shape when there isn't one.

---

## 10:45-11:30 - Review and next episode

### Visual recap

```text
same-shape-only elementwise check
            |
            v
broadcast_shape() -- which shapes are compatible, and what shape results
            |
            v
effective_strides() -- real stride on a real axis, zero on a broadcast one
            |
            v
stride_offset() + advance_coordinate() -- walk every output position once
            |
            v
elementwise_binary() rewritten -- +, -, and * all broadcast for free
```

### Narration

> Five small pieces, and each one answers exactly one question.
> `broadcast_shape` decides whether two shapes are compatible, and what
> shape they produce together. `effective_strides` turns one operand's real
> shape into a stride per output axis, real where it has a position, zero
> where it needs to reuse one. `stride_offset` turns a coordinate and a
> stride list into a flat index — the same arithmetic `at()` already did,
> generalized. `advance_coordinate` walks that coordinate through every
> output position once, like an odometer. And `elementwise_binary` just
> wires those four together, so `operator+`, `operator-`, and `operator*`
> all get broadcasting for free without changing a line of their own code.

### On screen

```text
align from the right, pad missing axes with 1
equal, or one side is 1 -> compatible; stretch the 1
stride zero on a broadcast axis -> reuse the same element

linear [2,1] + bias []    -> [2,1]   (Episode 4's case, now free)
inputs [2,3] - offset [3] -> [2,3]   (a real per-feature operation)

next: a loss function -- how wrong is a prediction, and what do we do about it
```

### Narration

> So that's broadcasting. We line shapes up from the right, let size-one axes
> stretch, and use a stride of zero on any stretched axis so the same value can
> be reused without copying it.
>
> So far, everything we've built is still forward computation. Inputs, weights,
> and a bias go in, and we get predictions out. But we still have no way to
> measure how good those predictions are, or to use that measurement to improve
> the weights. That's what we'll tackle next with a loss function and the first
> step toward learning.

---

## 11:30-12:00 - Questions for Episode 6

### Narration

> Three questions for you. Answers are in the pinned comment.

1. `effective_strides` gives a broadcast axis a stride of zero. Why does that alone guarantee every coordinate along that axis reads the same underlying element, without any extra special-casing?
2. Before today, `linear + bias` only worked by manually copying `bias` into a full `[2,1]` tensor. Why does the general version delete that copy entirely instead of keeping it as a scalar-specific optimization?
3. `broadcast_shape` and `effective_strides` both compute an offset to figure out how many leading axes are missing.  What would go wrong if we padded missing axes on the right instead of the left?

End the episode after the questions.
