# Short 2: This Loop Can Never Finish

## Script

### 00:00-00:04

Show the loop immediately, no greeting, no series intro.

```cpp
for (std::size_t i = n - 1; i >= 0; --i) {
  // ...
}
```

> This loop can never finish.

### 00:04-00:09

#### Narration

> Watch `i` count down. Nine, eight, seven... all the way to zero. Looks
> completely normal.

#### Visual

Tick a counter down on screen in sync: `n-1 -> ... -> 2 -> 1 -> 0`. Keep the
loop code visible above it, unchanged.

### 00:09-00:15

#### Narration

> `size_t` is unsigned, so it
> can never go negative. Zero minus one wraps all the way around to the
> largest number the type can hold.

#### Visual

Freeze on `i = 0`. Show `--i` firing. Reveal the wrapped value large and
centered:

```text
i = 18446744073709551615
```

### 00:15-00:19

#### Narration

> And `i >= 0`? That's still true. It was always going to be true. An
> unsigned number can't fail that check, so this loop's exit condition can
> never become false.

#### Visual

Highlight `i >= 0` in the original loop. Stamp it `ALWAYS TRUE` in red.

### 00:19-00:22

#### Narration

> Check before you decrement, not after.

#### Visual

Cut to the fix, same size and position as the original loop:

```cpp
for (std::size_t i = n; i-- > 0;) {
  // ...
}
```

> Follow for more C++ and deep learning systems from first principles.

Cut immediately after **principles**.
