# Short 5: One Extra Variable Made This C++ Loop Significantly Faster

Target runtime: 20 to 25 seconds

## Script

### 00:00-00:04

Open on:
`/Users/keremkazan/code/short-05-instruction-dependencies/scenes/scene_1.cpp`

Keep `ONE EXTRA VARIABLE` visible from the first frame.

> How much faster can you make this loop with one extra variable?

### 00:04-00:09

Highlight `a += arr[i]`, then connect several additions into one chain. Do not
reveal the second accumulator yet.

> Right now, every addition has to wait for the one before it.

### 00:09-00:15

Open:
`/Users/keremkazan/code/short-05-instruction-dependencies/scenes/scene_2.cpp`

Reveal `b`, then highlight `a` and `b` as separate lanes.

> Add `b`, split the values between them, and now the processor has two
> independent sums to work on.

### 00:15-00:20

Reveal:

```text
accumulators    median (s)
1                    5.881
2                    4.233   1.39x faster
```

> On my machine, that cut the runtime from 5.881 seconds to 4.233.

Keep this compact footer visible but do not narrate it:

```text
Apple M1 Pro · Apple Clang 21 · median of 3
vectorization and loop unrolling disabled
controlled test: four loads and additions per loop
8,192 cached values × 3,000,000 passes
```

### 00:20-00:25

Add the final row:

```text
4                    3.696   1.59x faster
```

> Two is faster. Four is faster again. No SIMD. No loop unrolling. So what is
> the CPU doing differently?

Cut immediately after **differently**. No CTA.

## Recording notes

- No greeting, context, or setup before the hook.
- Record only from the numbered snippets in `scenes/`; do not show the benchmark
  harness.
- Keep the tested OBS keyboard ducking active while narrating.
- The first frame and first sentence must establish the one-variable challenge.
- The main lesson is complete before the final question: independent chains
  can expose more work for the processor to overlap.
- Do not claim that more accumulators are always faster or that these exact
  ratios apply to other machines.
