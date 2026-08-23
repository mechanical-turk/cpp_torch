# Content Ideas

This is the durable backlog for possible videos, Shorts, posts, and other
content. Ideas belong here before they are promoted into a production script or
release plan.

## Video ideas

### I built a chess AI that trash talks while crushing you

- **Status:** Seed idea
- **Format:** To be decided
- **Notes:** Preserve the title and premise for later development.

## Short ideas

### How two wrong predictions add up to zero

- **Status:** Strong candidate for Short 4
- **Source:** Episode 6
- **Hook:** "These predictions are both wrong. But if we add their errors, the
  model looks perfect."
- **Story:** Show errors of `+1` and `-1` cancelling to zero. Square them and
  show that both mistakes now contribute.
- **Payoff:** This gives an intuitive reason for the square in mean squared
  error without requiring prior ML terminology.
- **Target:** 18-22 seconds with no CTA.

## Performance video ideas

### The better Big O matrix multiplication that runs slower

- **Status:** Selected Short concept, blocked on real benchmark results
- **Working title:** Big O Matters Way Less Than You Think
- **Hook:** "This matrix multiplication algorithm has better Big O. It also ran
  slower."
- **Format:** Native Short
- **Premise:** Benchmark ordinary cubic matrix multiplication against a
  lower-complexity algorithm such as Strassen's algorithm. Show that the
  asymptotically better algorithm can be slower at practical matrix sizes,
  especially when compared with a hardware-aware cubic implementation.
- **Topics:** asymptotic complexity, crossover points, constant factors,
  temporary allocations, recursion, locality, SIMD, and why Big O does not
  predict the fastest implementation at a particular input size.
- **Constraint:** Do not claim a winner before measuring multiple matrix sizes.
  Report the crossover point if one appears.
- **Closing point:** Big O matters, but it does not tell us which implementation
  will be faster for a particular input on a particular machine.

### How fast can we make the ordinary cubic matmul?

- **Status:** Seed idea requiring benchmarks
- **Format:** Progressive optimization video, with possible Short extracts
- **Premise:** Begin with the clearest triple-loop matrix multiplication and
  improve its measured runtime without changing its cubic complexity.
- **Progression:** baseline build, optimized build, loop reordering, contiguous
  access, cache blocking, vectorization, architecture-specific compiler flags,
  and finally an explicitly labeled fast-math experiment where applicable.
- **Payoff:** The algorithm remains `O(n^3)`, but hardware utilization changes
  dramatically.
- **Constraint:** Separate code changes that improve cache behavior from
  compiler flags. Fast-math must be presented with its numerical tradeoffs, not
  as a free optimization.
