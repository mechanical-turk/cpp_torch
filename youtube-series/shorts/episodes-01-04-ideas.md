# Native Short Ideas from Episodes 1-4

These are standalone vertical lessons, not clips or episode summaries.

## What the first Short changed

The first Short tried to explain `[]`, `[1]`, and `[0]` in 34 seconds while
showing the completed comparison immediately. Instagram sampled it broadly,
but average viewing time was only 5.44 seconds. That does not prove why people
left, but it gives us a clear next experiment:

- target 18-25 seconds;
- teach no more than two concepts;
- begin resolving the hook within the first few seconds;
- reveal the visual progressively instead of showing the answer immediately;
- finish at the payoff, with either no CTA or one sentence under two seconds.

## Prioritized ideas

### 1. The C++ Reverse Loop That Never Ends

- **Source:** Episode 1
- **Opening line:** "This C++ loop can never finish."
- **Story:** Show `std::size_t i` moving from `1` to `0` to `SIZE_MAX`, then
  replace the loop with the one-past form.
- **Payoff:** An unsigned value can never become negative, so `i >= 0` never
  becomes false.
- **Visual:** Reveal the wrap only after the viewer sees the apparently normal
  loop.
- **Target:** 18-22 seconds.
- **Evidence:** Episode 1 has a small, noisy seek/replay spike around its real
  unsigned-underflow failure. This is an experiment based on that signal, not a
  proven content rule.

### 2. Two Wrong Predictions That Add Up to Zero

- **Status:** Recommended for Short 4.
- **Source:** Episode 6
- **Opening line:** "These two predictions are both wrong, but their errors add
  up to zero."
- **Story:** Show residuals `+1` and `-1`, add them to get zero, then square
  them so both mistakes remain visible.
- **Payoff:** Opposite errors cancel when summed. Squaring them turns both into
  positive contributions, which is why mean squared error starts with squares.
- **Visual:** Reveal two prediction-target pairs, then `+1 + (-1) = 0`, followed
  by `1^2 + (-1)^2 = 2`.
- **Target:** 18-22 seconds with no CTA.

### 3. Why a Dot Product Returns One Number

- **Source:** Episode 3
- **Opening line:** "Why does multiplying two vectors sometimes give you a
  vector, and sometimes give you one number?"
- **Story:** First multiply corresponding values. Then add the products.
- **Payoff:** Elementwise multiplication stops at the product vector; a dot
  product reduces that vector with a sum.
- **Visual:** Reveal the product vector first and the summation second.
- **Target:** 18-22 seconds.

### 4. Matrix Multiplication Is Repeated Dot Products

- **Source:** Episode 4
- **Opening line:** "Matrix multiplication looks like a new operation, but
  every number in the output is just a dot product."
- **Story:** Show one observation producing one prediction. Add two more rows,
  then show that each row performs the same dot product with the weights.
- **Payoff:** Stacking observations as rows turns repeated dot products into
  matrix multiplication.
- **Visual:** Reuse the two Episode 4 observation-to-prediction diagrams, but
  reveal one row and one output at a time.
- **Target:** 20-24 seconds.

### 5. A Zero Input Produces the Bias

- **Source:** Episodes 3 and 4
- **Opening line:** "Feed this layer all zeros and its output is the bias."
- **Story:** Every weighted input contribution vanishes, leaving `0 @ W + b`.
- **Payoff:** The bias is the layer's output at the zero input.
- **Visual:** Zero the input matrix, watch every multiplication disappear, and
  carry the bias directly into each output row.
- **Target:** 15-20 seconds.

### 6. Check Integer Overflow Before Multiplication

- **Source:** Episode 2
- **Opening line:** "If you check for integer overflow after multiplying, the
  evidence may already be gone."
- **Story:** Show a wrapped product passing through later code, then derive the
  safe precondition `product > max / dimension`.
- **Payoff:** Rearrange the unsafe operation into a condition that can be
  checked before executing it.
- **Target:** 20-25 seconds.

### 7. Broadcasting a Bias Does Not Mean Copying It

- **Source:** Episode 4
- **Opening line:** "We need the same bias on every row, but we do not need to
  copy it into a larger tensor."
- **Story:** Show one bias vector reused for three output rows. Each output
  coordinate reads the same corresponding bias coordinate.
- **Payoff:** Broadcasting changes how an operand is indexed, not how much data
  it stores.
- **Target:** 20-25 seconds.

### 8. One Ampersand Makes Tensor Indexing Mutable

- **Source:** Episode 2
- **Opening line:** "This ampersand is what makes `tensor.at(index) = 7` work."
- **Story:** Returning `double` gives the caller a copy. Returning `double&`
  gives the caller access to the selected value inside the tensor.
- **Payoff:** Mutation requires returning the stored object, not a copy of it.
- **Target:** 18-22 seconds.

### 9. Elementwise Multiplication Is Not Matrix Multiplication

- **Source:** Episodes 3 and 4
- **Opening line:** "C++ programmers use the word multiplication for two tensor
  operations that do completely different work."
- **Story:** Elementwise multiplication pairs equal coordinates. Matrix
  multiplication forms each output from a row-column dot product.
- **Payoff:** One preserves coordinates; the other creates new output
  coordinates and sums over a shared dimension.
- **Target:** 22-27 seconds.

### 10. A One-Hot Input Selects One Row of the Weight Matrix

- **Source:** Episode 4
- **Opening line:** "This input contains one `1`, so the whole matrix
  multiplication becomes a lookup."
- **Story:** Multiply a one-hot row vector by a weight matrix. Every zeroed row
  contributes nothing, leaving only the row selected by the `1`.
- **Payoff:** Multiplication by a one-hot vector selects one weight row, which
  foreshadows embedding lookup.
- **Visual:** Dim every weight row except the one aligned with the active input
  coordinate, then slide that row into the output.
- **Target:** 20-24 seconds.

### 11. Why Matrix Multiplication's Inner Dimensions Must Match

- **Source:** Episode 4
- **Opening line:** "Why can we multiply a `[2,3]` matrix by `[3,4]`, but not
  by `[2,4]`?"
- **Story:** Select one row from the left and one column from the right. Their
  lengths must match for their dot product to exist.
- **Payoff:** The shared inner dimension is the length of every dot product.
- **Target:** 18-22 seconds.

### 12. Same Element Count Does Not Mean Same Shape

- **Source:** Episodes 1 and 3
- **Opening line:** "These tensors both contain six numbers, but adding them is
  still undefined in our first implementation."
- **Story:** Compare shapes `[2,3]` and `[3,2]`. The flat storage lengths match,
  but corresponding coordinates do not describe the same structure.
- **Payoff:** Elementwise operations need compatible coordinates, not merely
  equal storage lengths.
- **Visual:** Align both flat buffers, then fold them into visibly different
  grids.
- **Target:** 20-24 seconds.

### 13. A Tensor Does Not Need Nested Vectors

- **Source:** Episode 1
- **Opening line:** "This rank-three tensor is stored in one ordinary C++
  vector."
- **Story:** Show a nested logical tensor flattening into one row-major buffer.
- **Payoff:** Shape and indexing create the multidimensional interpretation;
  the owned storage can remain flat.
- **Visual:** Animate cells leaving a 3D arrangement and snapping into one
  contiguous row.
- **Target:** 18-22 seconds.

### 14. Batch Size Does Not Change the Number of Weights

- **Source:** Episode 4
- **Opening line:** "A thousand observations do not give this layer a thousand
  copies of its weights."
- **Story:** Grow the input from one row to many while keeping the same weight
  matrix fixed beside it.
- **Payoff:** The batch dimension controls how many observations are evaluated;
  the parameter count depends on input and output features.
- **Visual:** Add input rows rapidly while one weight matrix remains anchored.
- **Target:** 18-22 seconds.

### 15. How `[2,1] + [1,3]` Becomes `[2,3]`

- **Source:** Episode 4
- **Opening line:** "Neither of these tensors has shape `[2,3]`, but their sum
  does."
- **Story:** Expand the first operand across columns and the second across rows,
  then add at each crossing.
- **Payoff:** Independent size-one axes can broadcast to form the larger output
  grid.
- **Visual:** Stretch a vertical column and a horizontal row into a `2 x 3`
  grid, revealing sums only where they intersect.
- **Target:** 20-24 seconds.

### 16. Broadcasting Compares Shapes from the Right

- **Source:** Episode 4
- **Opening line:** "Broadcasting reads tensor shapes backwards."
- **Story:** Align `[2,3,4]` and `[3,1]` at their right edges, then compare
  `4` with `1`, `3` with `3`, and treat the missing leading axis as one.
- **Payoff:** Right alignment makes trailing feature dimensions line up while
  allowing operands to omit leading batch dimensions.
- **Visual:** Slide the shorter shape underneath the longer one until their
  right edges lock together.
- **Target:** 20-25 seconds.

### 17. Integer Overflow and Floating-Point Overflow Fail Differently

- **Source:** Episode 2
- **Opening line:** "Overflow does not mean the same thing for these two C++
  numbers."
- **Story:** Contrast an overflowing `std::size_t` wrapping modulo its range
  with a `double` operation producing infinity under normal IEEE 754 behavior.
- **Payoff:** The same word names different numerical behavior, so tensor shape
  arithmetic and tensor values need different safeguards.
- **Visual:** Run identical expanding number counters into a wraparound circle
  and an infinity symbol.
- **Target:** 20-25 seconds.

### 18. What `*this` Means in a C++ Member Function

- **Source:** Episode 3
- **Opening line:** "This asterisk is not multiplying anything."
- **Story:** Inside `Tensor::dot`, `this` is a pointer to the current tensor;
  dereferencing it produces the tensor object used by `operator*`.
- **Payoff:** `(*this * other).sum()` means elementwise-multiply the current
  tensor by `other`, then sum the result.
- **Visual:** Start with the ambiguous expression, isolate `this`, turn the
  pointer into the current object, then restore the full expression.
- **Target:** 20-24 seconds.

### 19. Rank Three Can Still Mean Zero Elements

- **Source:** Episode 2
- **Opening line:** "This tensor has three dimensions and stores absolutely
  nothing."
- **Story:** Reveal shape `[2,0,3]`. Its rank comes from three axes, while the
  zero-length axis makes the shape product zero.
- **Payoff:** Rank describes how many axes exist; `numel` describes how many
  coordinate combinations exist.
- **Visual:** Build three labeled axes, then collapse the middle axis to zero
  and empty the storage.
- **Target:** 18-22 seconds.

### 20. Where Matrix Multiplication's Output Shape Comes From

- **Source:** Episode 4
- **Opening line:** "A `[2,3]` matrix times a `[3,4]` matrix produces `[2,4]`.
  Here is why."
- **Story:** The left operand supplies two selectable rows. The right operand
  supplies four selectable columns. Each row-column pair creates one output.
- **Payoff:** The outside dimensions survive; the shared inner dimension is
  traversed and summed.
- **Visual:** Fade the two inner `3`s together while carrying the outer `2` and
  `4` into a new output grid.
- **Target:** 18-22 seconds.

### 21. What the Bias Does in a Linear Model

- **Source:** Episode 3
- **Opening line:** "A model can have every weight equal to zero and still make
  a nonzero prediction."
- **Story:** Zero out every weighted feature contribution, then add the bias.
- **Payoff:** The bias establishes the model's baseline output independently of
  the current feature values.
- **Visual:** Dim all weighted arrows to zero while one bias block shifts the
  prediction.
- **Target:** 18-22 seconds.

### 22. A Dense Layer Needs One Bias Per Output

- **Source:** Episode 4
- **Opening line:** "A dense layer does not always have one bias. It has one
  bias for every output feature."
- **Story:** A weight matrix with two columns produces two values per
  observation, so the bias has shape `[2]` and is reused across rows.
- **Payoff:** The number of biases follows the output width, not the input
  width or batch size.
- **Target:** 18-22 seconds.

### 23. Why Tensor Indexing Cannot Use the Coordinate Directly

- **Source:** Episode 1
- **Opening line:** "The tensor coordinate `[1,2]` is not an index into this
  vector."
- **Story:** For shape `[2,3]`, map `[1,2]` to `1 * 3 + 2 = 5`.
- **Payoff:** Multidimensional coordinates must be converted into a physical
  flat-storage position.
- **Visual:** Highlight row 1, column 2 in a grid, then trace it to flat cell 5.
- **Target:** 18-22 seconds.

### 24. One Flat Vector Can Represent Several Tensor Shapes

- **Source:** Episode 1
- **Opening line:** "These six values are not enough to tell you the tensor's
  shape."
- **Story:** Reveal the same storage as `[6]`, `[2,3]`, and `[3,2]`.
- **Payoff:** Shape is independent metadata that cannot be recovered from the
  values alone.
- **Target:** 18-22 seconds.

### 25. The Constructor Check That Protects Every Tensor Operation

- **Source:** Episode 1
- **Opening line:** "Shape `[2,3]` with five values should never become a
  tensor."
- **Story:** Compute six required coordinates, compare that with five stored
  values, and reject construction.
- **Payoff:** One representation invariant prevents later indexing and
  arithmetic from operating on a contradictory object.
- **Visual:** Show a six-cell grid with the final cell missing, then stop the
  object at the constructor boundary.
- **Target:** 18-23 seconds.

### 26. A Later Zero Can Make a Huge Tensor Shape Empty

- **Source:** Episode 2
- **Opening line:** "This shape looks large enough to overflow, but it actually
  contains zero elements."
- **Story:** Use `[SIZE_MAX, 2, 0]`. The zero axis means there are no valid
  coordinates regardless of the other dimensions.
- **Payoff:** Detecting zero dimensions before multiplying preserves the true
  element count instead of reporting a false overflow.
- **Visual:** Let the first two dimensions expand dramatically, then have the
  zero axis erase every possible coordinate.
- **Target:** 20-25 seconds.

### 27. Why the Sum of an Empty Tensor Is Zero

- **Source:** Episode 2
- **Opening line:** "What do you get when you add no numbers at all?"
- **Story:** Start an accumulator at zero. An empty tensor performs no updates.
- **Payoff:** Zero is the additive identity, so the empty sum is zero.
- **Target:** 15-20 seconds.

### 28. Matrix Multiplication Is Not Commutative

- **Source:** Episode 4
- **Opening line:** "Swapping these two matrices can change the answer, or make
  the multiplication impossible."
- **Story:** Compare `[2,3] @ [3,4] -> [2,4]` with the reversed shapes, whose
  inner dimensions no longer match.
- **Payoff:** Matrix multiplication has directional row-column structure, so
  `A @ B` is not generally `B @ A`.
- **Visual:** Reverse two matrix blocks; let the first connection resolve and
  the reversed inner dimensions visibly fail to connect.
- **Target:** 20-24 seconds.

### 29. Why a Dense Weight Matrix Has Shape `[inputs, outputs]`

- **Source:** Episode 4
- **Opening line:** "Why does a layer with three input features and two outputs
  need a `[3,2]` weight matrix?"
- **Story:** Each output needs one weight for each of the three input features,
  producing two columns of three weights.
- **Payoff:** Rows index input features; columns index output features under the
  convention used in this series.
- **Visual:** Build one three-weight column for the first output, then add a
  second column for the second output.
- **Target:** 20-24 seconds.

### 30. Why `dot()` Rejects Matrices

- **Source:** Episode 4
- **Opening line:** "Our dot product rejects this matrix, and that is the right
  behavior."
- **Story:** A vector dot product chooses no output coordinate and returns one
  scalar. Two matrices require choosing a row and a column for every output.
- **Payoff:** Matrix multiplication is a grid of dot products, not one larger
  dot product.
- **Visual:** Show one vector pair collapsing to a scalar, then a matrix pair
  demanding several row-column selections.
- **Target:** 20-24 seconds.

### 31. Every Matrix Output Chooses One Row and One Column

- **Source:** Episode 4
- **Opening line:** "To compute this one matrix value, we only need one row and
  one column."
- **Story:** Highlight output coordinate `[i,j]`, trace `i` to a row on the left
  and `j` to a column on the right, then dot them.
- **Payoff:** Output coordinates directly select the two vectors used in their
  dot product.
- **Visual:** Let the output cell cast one horizontal beam to the left operand
  and one vertical beam to the right operand.
- **Target:** 18-22 seconds.

### 32. Matrix Multiplication Reduces Its Inner Dimension

- **Source:** Episode 4
- **Opening line:** "The middle dimension disappears from matrix
  multiplication because we add over it."
- **Story:** Walk `k` across matching row and column entries while accumulating
  their products into one output cell.
- **Payoff:** The inner dimension is a reduction axis, so it is traversed but
  does not appear in the output shape.
- **Visual:** Fade each consumed `k` position into a running sum while the outer
  dimensions remain visible.
- **Target:** 18-23 seconds.

### 33. A Scalar Can Broadcast Across Any Tensor Shape

- **Source:** Episode 4
- **Opening line:** "One stored number can participate in every element of this
  tensor without being copied first."
- **Story:** Right-align scalar shape `[]` with a matrix. Every missing scalar
  axis behaves like one, so every output coordinate reads the same scalar.
- **Payoff:** Scalar broadcasting is the rank-zero case of the same general
  indexing rule.
- **Visual:** Keep one scalar cell fixed while arrows fan out to a matrix one
  output cell at a time.
- **Target:** 18-22 seconds.

### 34. Broadcasting Zero with One Must Stay Empty

- **Source:** Episode 4
- **Opening line:** "Broadcasting dimensions zero and one does not produce one
  element. It produces none."
- **Story:** Compare `[0,3]` with `[1,3]`. The empty operand has no coordinate
  that can be expanded into a real output row.
- **Payoff:** A compatible `0` and `1` axis produces output size zero, not the
  numerical maximum of the dimensions.
- **Visual:** Offer one reusable row to an output axis with no positions; leave
  the result visibly empty.
- **Target:** 20-25 seconds.

### 35. A Broadcast Axis of Size One Always Reads Coordinate Zero

- **Source:** Episode 4
- **Opening line:** "This tensor expands across an axis without moving through
  its storage."
- **Story:** Let an output coordinate advance along an axis where the operand's
  dimension is one. Every output position maps back to operand coordinate zero.
- **Payoff:** Broadcasting reuses the sole available value rather than creating
  new stored values.
- **Visual:** Move an output cursor across several cells while every arrow
  returns to the same source cell.
- **Target:** 18-22 seconds.

### 36. A Missing Broadcast Axis Behaves Like Size One

- **Source:** Episode 4
- **Opening line:** "This vector has no batch axis, but we can still add it to
  every row of a matrix."
- **Story:** Right-align `[3]` under `[2,3]` and insert an effective leading
  dimension of one.
- **Payoff:** Missing leading axes behave like size-one axes for broadcasting.
- **Visual:** Reveal an implicit `1` to the left of `[3]`, then reuse the vector
  across both matrix rows.
- **Target:** 18-22 seconds.

### 37. Matrix Multiplication with an Empty Inner Dimension Returns Zeros

- **Source:** Episode 4
- **Opening line:** "This matrix multiplication performs zero multiplications
  and still returns a nonempty matrix."
- **Story:** Multiply shapes `[2,0]` and `[0,3]`. The output has shape `[2,3]`,
  and every output cell is an empty sum.
- **Payoff:** The outside dimensions determine the output grid; the empty inner
  reduction makes every value zero.
- **Visual:** Build a `2 x 3` output grid, attempt to send product terms into
  each cell, then reveal that every accumulator remains zero.
- **Target:** 22-26 seconds.

### 38. A Matrix of Observations Is Not Batched Matrix Multiplication

- **Source:** Episode 4
- **Opening line:** "These rows form a data batch, but this is still ordinary
  matrix multiplication."
- **Story:** Label a rank-two matrix `[observations, features]` and multiply it
  by one shared weight matrix. Contrast it with rank-three tensors containing
  several separate matrices.
- **Payoff:** Data batching and batched matmul use the word batch at different
  structural levels.
- **Visual:** Compare many rows on one sheet with many independent sheets.
- **Target:** 20-25 seconds.

### 39. Why Our First `matmul()` Accepts Only Rank-Two Tensors

- **Source:** Episode 4
- **Opening line:** "This `matmul()` handles a batch of rows, but it is not
  batched matrix multiplication."
- **Story:** Show one rank-two input matrix multiplied by one rank-two weight
  matrix. Then show a rank-three stack of independent matrix problems that
  would need another batch rule.
- **Payoff:** A matrix can contain many observations as rows without making the
  operation rank-N batched matmul.
- **Visual:** Keep the supported two matrices on one plane, then stack several
  planes to reveal the deferred operation.
- **Target:** 22-26 seconds.

### 40. A Forward Pass Is Not Training

- **Source:** Episodes 3 and 4
- **Opening line:** "We built a layer that makes predictions. It has not learned
  anything yet."
- **Story:** Show inputs flowing through fixed weights to predictions, then
  reveal the missing loss, gradients, and parameter update.
- **Payoff:** A forward pass evaluates current parameters; training requires a
  feedback process that changes them.
- **Visual:** Let the forward arrow complete, then outline the absent return
  path in a different color.
- **Target:** 20-24 seconds.

### 41. A Linear Layer Does Not Include an Activation Function

- **Source:** Episode 4
- **Opening line:** "This is a complete dense linear layer even though there is
  no ReLU."
- **Story:** Separate `Wx + b` from an optional activation applied afterward.
- **Payoff:** The affine transformation and activation are distinct operations;
  neural networks compose them explicitly.
- **Visual:** Finish one `Wx + b` block, then place an unconnected ReLU block
  beside it before optionally joining them.
- **Target:** 18-22 seconds.

### 42. Why the Bias Repeats Across Rows

- **Source:** Episode 4
- **Opening line:** "The bias repeats across observations, not across output
  features."
- **Story:** Give the bias shape `[outputs]` and right-align it with
  `[observations, outputs]`. Its coordinates change across columns and reset for
  each row.
- **Payoff:** Broadcasting reuses the same output-specific offsets for every
  observation in the batch.
- **Visual:** Move the same colored bias row down the output matrix without
  changing its values.
- **Target:** 20-24 seconds.

### 43. Weight Columns Correspond to Output Features

- **Source:** Episode 4
- **Opening line:** "Each column in this weight matrix builds a different
  output."
- **Story:** Dot one input row with the first weight column, then the second,
  placing the two results beside each other.
- **Payoff:** Under this layout, adding a weight column adds another output
  feature.
- **Visual:** Highlight one column at a time and let each illuminate its matching
  output cell.
- **Target:** 18-22 seconds.

### 44. Every Observation Uses the Same Weights

- **Source:** Episode 4
- **Opening line:** "Every row in this batch passes through the exact same
  model."
- **Story:** Hold one weight matrix fixed while selecting each input row in
  turn and producing its output row.
- **Payoff:** Batching repeats the computation across observations; it does not
  create observation-specific parameters.
- **Visual:** Cycle the highlighted input row while the weight matrix remains
  visually locked.
- **Target:** 18-22 seconds.

### 45. Reordering a Batch Only Reorders Its Outputs

- **Source:** Episode 4
- **Opening line:** "Swap these two observations and the model's answers swap
  with them."
- **Story:** Evaluate two independent rows, exchange their order, and show the
  corresponding output rows exchanging positions without changing values.
- **Payoff:** A dense layer acts independently on each batch row when no
  cross-observation operation is present.
- **Visual:** Give both rows stable colors and animate the same color swap in
  the output.
- **Target:** 18-22 seconds.

### 46. One Tensor Loop Can Implement Three Operators

- **Source:** Episode 3
- **Opening line:** "Addition, subtraction, and multiplication were repeating
  the same tensor loop."
- **Story:** Keep one traversal and swap only the scalar operation passed into
  it.
- **Payoff:** Separate the invariant traversal from the arithmetic that varies.
- **Visual:** One conveyor belt processes tensor pairs while `+`, `-`, and `*`
  cards take turns controlling the output.
- **Target:** 20-25 seconds.

### 47. A Scalar Tensor Is Not Just a `double`

- **Source:** Episodes 2 and 3
- **Opening line:** "This tensor contains one number, but it is not merely a
  `double`."
- **Story:** Compare a raw scalar with a rank-zero tensor carrying shape and
  tensor behavior.
- **Payoff:** The value is scalar, while the tensor wrapper keeps it inside the
  same shape and operation system as every other tensor.
- **Visual:** Place the same `7` first alone, then inside a tensor object with
  `shape = []` and `rank = 0` appearing around it.
- **Target:** 18-23 seconds.

### 48. One `at()` Call, Two Different Contracts

- **Source:** Episode 2
- **Opening line:** "C++ can choose whether tensor indexing is mutable from the
  object you call it on."
- **Story:** Call `at()` on a mutable tensor and a `const` tensor. Reveal the
  `double&` and `const double&` overloads only after each call.
- **Payoff:** A member function's `const` qualifier participates in overload
  resolution.
- **Visual:** Split one tensor into mutable and locked states, then illuminate
  the selected overload.
- **Target:** 20-25 seconds.

### 49. Why `std::move` Does Not Move Your Original Tensor Here

- **Source:** Episode 3
- **Opening line:** "This `std::move` looks dangerous, but the input tensors are
  untouched."
- **Story:** The operation first creates a local output vector. Only that
  completed local vector is moved into the returned tensor.
- **Payoff:** Moving a disposable local avoids another vector copy without
  stealing storage from either operand.
- **Visual:** Keep both input buffers anchored while a newly built output buffer
  changes ownership.
- **Target:** 20-25 seconds.

### 50. Why `a + b` Should Not Change Either Tensor

- **Source:** Episode 3
- **Opening line:** "After `c = a + b`, which tensor should own the answer?"
- **Story:** Show `a` and `b` remaining intact while a third allocation fills
  with their elementwise sums.
- **Payoff:** Ordinary binary operators conventionally return a new value;
  mutation belongs to a separate operation such as `+=`.
- **Visual:** Keep both operand buffers fixed and grow a distinct output buffer
  between them.
- **Target:** 20-24 seconds.

### 51. Rows Are Observations; Columns Are Features

- **Source:** Episode 4
- **Opening line:** "If you have three observations with four features each,
  which tensor shape should you use?"
- **Story:** Place each observation on one row and each feature in one column.
- **Payoff:** The conventional batch layout is `[observations, features]`, so
  the shape is `[3,4]`.
- **Target:** 15-20 seconds.

### 52. What a Reduction Actually Reduces

- **Source:** Episode 2
- **Opening line:** "Why is `sum()` called a reduction instead of just an
  addition?"
- **Story:** Show six independent tensor values flowing into one accumulator.
- **Payoff:** A reduction collapses one or more axes by combining many values
  into fewer values.
- **Visual:** Six cells converge into one cell while the shape changes from
  `[2,3]` to `[]`.
- **Target:** 18-22 seconds.

### 53. Mutable Elements, Protected Storage

- **Source:** Episode 2
- **Opening line:** "Our tensor lets you change this value, but it still will
  not let you resize its storage."
- **Story:** `at()` exposes one `double&`; the vector itself remains private.
- **Payoff:** An API can permit value mutation without exposing structural
  mutations that would break its invariants.
- **Visual:** Open a small gate to one cell while keeping the vector boundary
  locked.
- **Target:** 18-22 seconds.

### 54. Why Our First Elementwise Operations Require Equal Shapes

- **Source:** Episode 3
- **Opening line:** "Before broadcasting, tensor addition has one brutally
  simple rule."
- **Story:** Pair each coordinate in `[2,3]` with the same coordinate in the
  other operand; then show why a missing or differently organized coordinate
  breaks that pairing.
- **Payoff:** Equal shapes make one-to-one coordinate traversal unambiguous.
- **Visual:** Connect matching cells across two identical grids, then break the
  links when one grid changes shape.
- **Target:** 18-22 seconds.

### 55. The Dot Product of Two Empty Vectors

- **Source:** Episode 3
- **Opening line:** "What should the dot product of two empty vectors be?"
- **Story:** There are no pairwise products, so the intermediate product is
  empty and its sum is zero.
- **Payoff:** Defining the empty dot product as zero follows directly from the
  empty-sum identity.
- **Visual:** Show two empty brackets producing no product terms, then a scalar
  zero.
- **Target:** 15-20 seconds.

### 56. Elementwise Operations Preserve Shape

- **Source:** Episode 3
- **Opening line:** "Elementwise addition changes every value and none of the
  coordinates."
- **Story:** Pair two equal-shaped tensors coordinate by coordinate and place
  each result back at the same coordinate.
- **Payoff:** With equal-shape elementwise arithmetic, the output shape is the
  operand shape.
- **Visual:** Keep one grid fixed while only the numbers inside its cells
  change.
- **Target:** 15-20 seconds.

### 57. Summing a Scalar Returns the Scalar

- **Source:** Episodes 2 and 3
- **Opening line:** "What happens when you reduce a tensor that already contains
  one scalar?"
- **Story:** Show a rank-zero tensor entering `sum()` with no axes or additional
  values to combine.
- **Payoff:** The sum of one value is that value, and the result remains a
  scalar tensor.
- **Visual:** Pass one scalar cell through the reduction funnel unchanged.
- **Target:** 15-18 seconds.

### 58. Tensor Subtraction Remembers Operand Order

- **Source:** Episode 3
- **Opening line:** "These two tensor subtractions use the same values and
  produce opposite answers."
- **Story:** Compute `a - b` and `b - a` at one coordinate before expanding the
  result across the tensors.
- **Payoff:** Shared traversal does not make the operation commutative; the
  scalar function still determines operand order.
- **Visual:** Reverse two colored operands and flip every output sign.
- **Target:** 18-22 seconds.

### 59. Dot Products Require Vectors of the Same Length

- **Source:** Episode 3
- **Opening line:** "A three-value vector cannot take a dot product with a
  four-value vector."
- **Story:** Pair corresponding coordinates until one vector has an unmatched
  value.
- **Payoff:** Every term in a dot product needs one value from each operand, so
  the vector lengths must match.
- **Visual:** Draw pairwise links that stop when the extra fourth cell appears.
- **Target:** 15-20 seconds.

### 60. Why Tensor Functions Take `const Tensor&`

- **Source:** Episodes 3 and 4
- **Opening line:** "This tiny C++ signature avoids copying an entire tensor."
- **Story:** Contrast passing a tensor by value with passing `const Tensor&`.
  The reference observes the existing object, and `const` blocks mutation.
- **Payoff:** A const reference provides read-only access without duplicating
  the tensor's storage.
- **Visual:** Show the by-value path cloning a large buffer while the reference
  path draws one pointer-like connection.
- **Target:** 20-24 seconds.

### 61. Why Shape Accessors Return `const std::vector&`

- **Source:** Episode 1
- **Opening line:** "Returning this shape by value would copy a vector on every
  call."
- **Story:** Return a const reference to the tensor's existing shape instead,
  then show that the caller can inspect but not resize it.
- **Payoff:** The accessor avoids a copy while protecting the representation
  invariant.
- **Visual:** Contrast a duplicated shape buffer with a read-only viewing
  window into the original.
- **Target:** 20-24 seconds.

### 62. Why Mark a Tensor Accessor `[[nodiscard]]`

- **Source:** Episodes 1 and 2
- **Opening line:** "This C++ attribute asks the compiler to flag a suspicious
  call that computes a value and throws it away."
- **Story:** Show `tensor.rank();` as a discarded query and then assign or use
  its result.
- **Payoff:** `[[nodiscard]]` communicates that ignoring the returned value is
  probably a mistake; it does not change runtime behavior.
- **Visual:** Let the unused result fall into a warning icon, then route the
  used result into an expression.
- **Target:** 18-22 seconds.

## Hold until later evidence exists
### The Clear Dot Product That Allocates Memory It Does Not Need

`(left * right).sum()` is a useful reference implementation, but claiming a
meaningful performance cost requires the planned benchmark. Record this only
after the series measures the intermediate allocation against a fused loop.

### How a Rank-Three Coordinate Becomes a Flat Index

The row-major calculation is valuable, but a full `[2,3,4]` stride derivation
is difficult to resolve in 25 seconds without turning into hurried arithmetic.
Revisit it once a visual proves that it can remain legible and conversational.
