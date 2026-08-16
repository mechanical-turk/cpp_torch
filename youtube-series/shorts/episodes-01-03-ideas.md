# Native Short Ideas from Episodes 1-3

These are standalone 9:16 lessons derived from the first three long-form
episodes. They are not clips or condensed episode summaries. Each Short should
resolve one question completely, use one dominant visual, and end immediately
after the payoff.

## Recording priority

### 1. `[]` Is Not an Empty Tensor

- **Source:** Episode 2
- **Hook:** "This tensor has no dimensions, but it still contains one value."
- **Core visual:** Compare `[]`, `[1]`, and `[0]` in a three-row table showing
  rank and element count.
- **Story:** `[]` has no coordinate choices because it represents a scalar;
  `[1]` is a one-element vector; `[0]` is an empty vector.
- **Payoff:** Rank and element count describe different properties.
- **Target length:** 35-45 seconds
- **Related video:** Episode 2

### 2. The C++ Reverse Loop That Never Ends

- **Source:** Episode 1
- **Hook:** "This completely normal-looking C++ loop can never terminate."
- **Core visual:** Start with `for (std::size_t i = n - 1; i >= 0; --i)` and
  animate `2, 1, 0, SIZE_MAX`.
- **Story:** `std::size_t` is unsigned, so `i >= 0` is always true and
  decrementing zero wraps to the largest representable value.
- **Payoff:** Use the one-past form: `for (std::size_t i = n; i > 0; --i)` and
  access `i - 1` inside the loop.
- **Target length:** 35-50 seconds
- **Related video:** Episode 1

### 3. Why a Dot Product Returns One Number

- **Source:** Episode 3
- **Hook:** "You multiply two vectors. Why doesn't the dot product return a
  vector?"
- **Core visual:** `[0.5, -1, 2] * [4, 3, 2] = [2, -3, 4]`, followed by
  `2 - 3 + 4 = 3`.
- **Story:** Elementwise multiplication creates the individual weighted
  contributions; summation reduces those contributions to one scalar.
- **Payoff:** A dot product is elementwise multiplication followed by a full
  sum.
- **Target length:** 30-40 seconds
- **Related video:** Episode 3

## Strong follow-ups

### 4. One Flat Vector Can Represent Many Tensor Shapes

- **Source:** Episode 1
- **Hook:** "These six numbers do not tell you the tensor's shape."
- **Core visual:** Animate the same six values becoming `[6]`, `[2,3]`,
  `[3,2]`, and `[1,2,3]`.
- **Payoff:** Shape is indispensable metadata; the values alone cannot recover
  their multidimensional organization.
- **Target length:** 30-40 seconds

### 5. How `[1,2,3]` Becomes One Flat Index

- **Source:** Episode 1
- **Hook:** "A tensor coordinate is not a memory address. So how do we find the
  value?"
- **Core visual:** For shape `[2,3,4]`, reveal strides `[12,4,1]` and compute
  coordinate `[1,2,3]` as `1*12 + 2*4 + 3*1 = 23`.
- **Payoff:** In row-major storage, each coordinate is weighted by the size of
  the block to its right.
- **Target length:** 40-55 seconds

### 6. Check Overflow Before You Multiply

- **Source:** Episode 2
- **Hook:** "If you check for integer overflow after multiplying, you are
  already too late."
- **Core visual:** Contrast `product *= dimension` followed by a check with
  `product > max / dimension` before multiplication.
- **Payoff:** The division rearranges the unsafe multiplication into a check
  that can be evaluated safely.
- **Target length:** 35-50 seconds

### 7. Why the Sum of an Empty Tensor Is Zero

- **Source:** Episode 2
- **Hook:** "What should you get when you add no numbers at all?"
- **Core visual:** Accumulator begins at `0`; each value would be added, but an
  empty tensor performs no updates.
- **Payoff:** Zero is the additive identity, so defining the empty sum as zero
  makes summation coherent for every tensor size.
- **Target length:** 25-35 seconds

### 8. Elementwise Multiplication Is Not Matrix Multiplication

- **Source:** Episode 3
- **Hook:** "These two tensor multiplications use the same English word and do
  completely different work."
- **Core visual:** Compare `[1,2] * [3,4] = [3,8]` with one matrix output cell
  formed from a row-column dot product.
- **Payoff:** Elementwise multiplication preserves coordinates and shape;
  matrix multiplication contracts an inner dimension.
- **Target length:** 35-50 seconds

### 9. The Clearest Dot Product Allocates Memory It Does Not Need

- **Source:** Episode 3
- **Hook:** "This dot product is mathematically perfect and computationally
  wasteful."
- **Core visual:** Compare `(left * right).sum()` with one fused loop that
  accumulates `left[i] * right[i]` directly.
- **Payoff:** Composition is an excellent reference implementation, but it
  creates and traverses an intermediate tensor. This establishes an
  optimization hypothesis, not a benchmark result.
- **Target length:** 40-55 seconds

### 10. A Linear Model in One Tensor Expression

- **Source:** Episode 3
- **Hook:** "This one line contains an entire linear model prediction."
- **Core visual:** `weights.dot(features) + bias`, expanded into three weighted
  contributions and one constant offset.
- **Payoff:** The dot product combines feature contributions; the bias supplies
  the baseline prediction.
- **Target length:** 40-55 seconds

## Recommended first batch

Record ideas 1, 2, and 3 first. Together they test three audience entry points:

1. tensor semantics and a counterintuitive fact;
2. practical modern C++ and a concrete bug; and
3. mathematical intuition connected directly to model computation.

Publish them separately rather than on consecutive days. Use their retention,
view-source, and related-video results to decide whether the next batch should
lean more toward C++, tensor representation, or ML mathematics.

