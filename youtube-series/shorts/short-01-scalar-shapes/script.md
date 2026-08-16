# Short 1: `[]` Is Not an Empty Tensor

## Script

### 00:00-00:07

Begin with the arrow visible and pointing to the scalar.

> Shape empty brackets has zero dimensions, but it contains one value.

Move the arrow to the empty vector.

> Shape bracket zero has one dimension, but contains nothing.
    
Hide the arrow.

> If that sounds backwards, here's why.

### 00:07-00:13

#### Narration

> Rank counts axes. 
> 
> Empty brackets has no axes, so its rank is zero.

#### Arrow

1. Show, pointing to the scalar's `rank 0`.
2. Hide after **rank is zero**.

### 00:13-00:25

#### Narration

> Element count comes from multiplying the dimension sizes, starting at one.
> Empty brackets has no dimensions to multiply, so the count stays one. It
> represents a scalar.

#### Arrow

1. Keep hidden until **the count stays one**.
2. Show, pointing to the scalar's `elements 1`.
3. Hide after **It represents a scalar**.

### 00:25-00:34

#### Narration

> Bracket one has one axis of length one, so it contains one value. Bracket zero
> has one axis of length zero, so its element count becomes zero.

#### Arrow

1. Show, pointing to the singleton's `elements 1`.
2. Move to the empty vector's `elements 0`.
3. Hide before the payoff.

### 00:34-00:41

#### Narration

> No axes and an axis of length zero are not the same thing.
>
> Follow for more C++ and deep learning systems from first principles.

Keep the arrow hidden. Cut immediately after **principles**.
