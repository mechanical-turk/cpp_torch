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

### Stop sharing this counter

- **Status:** Saved at the creator's request on September 8, 2026; not selected
  for recording. [Script, S01-S20 audit and critique](shorts/pitch-lab/2026-09-08/01-local-counter-reduction.md).
- **Hook:** "Stop sharing this counter."
- **Premise:** Compare two workers updating a shared atomic count repeatedly
  with private counts merged after both workers finish. Same items and exact
  final answer; intermediate progress is deliberately not part of the contract.
- **Payoff:** Measured before/after runtime, immediately followed by a question
  about the counter's cost, then a proposed live-progress batching experiment.
- **Connection:** Follows Short 7's proposed final-totals investigation, but
  shared-counter contention is distinct from its false-sharing layout test.
- **Open critique:** Standard reduction may be too familiar. Find a recognizable
  practical counting workload without manufacturing a bad implementation.
  Editorial score 92.5/100, rework; missing timings are not the score deduction.
- **Proof handoff:** Normal optimized builds, relaxed atomic baseline,
  data-dependent input, correct joins and timed final merge. No measurements,
  code changes, recording or release schedule have been approved by saving it.

### Instruction dependency and its impact on performance

- **Status:** Selected for Short 5; controlled benchmark validated on Apple M1
  Pro with Apple Clang 21
- **Premise:** Sum the same `std::uint64_t` array with one accumulator, then
  repeat with `2`, `4`, `8`, `16`, and `64` independent accumulators.
- **Core comparison:** `sum_with_accumulators<1>` creates one loop-carried
  dependency chain. Larger accumulator counts create independent chains that an
  out-of-order CPU may overlap.
- **Provided variants:** `dependent_sum`, `independent_sum`, `sum_4`, `sum_8`,
  `sum_16`, and `sum_64`.
- **Hook direction:** Show two loops that perform the same number of additions
  and ask why one can finish sooner.
- **Story:** Begin with the single accumulator. Each addition needs the previous
  sum before it can continue. Split the work across several accumulators, show
  the independent chains, then reveal the measured runtimes.
- **Payoff:** Big O and operation count do not describe the instruction
  dependency graph. Independent work can expose instruction-level parallelism.
- **Visual:** Contrast one long addition chain with several shorter parallel
  lanes that merge only at the end.
- **Benchmark sweep:** Measure every accumulator count over several input sizes,
  preserve the result from optimization, inspect optimized assembly, and report
  the recording machine and compiler flags.
- **Accuracy constraint:** Do not promise that more accumulators are always
  faster. The compiler may already unroll or vectorize the loop. Large inputs
  may become memory-bound, while too many accumulators may increase register
  pressure or spill to memory.
- **Seed implementation:** Use the supplied `sum_with_accumulators<N>` template
  with the accumulator sweep exactly as proposed.
- **Target:** 20-25 seconds, with the benchmark winner withheld until the end.
- **Measured scalar result:** With `-O3 -fno-vectorize
  -fno-slp-vectorize`, the median CPU time for 4,096 cached `uint64_t` values
  fell from 1,336 ns with one accumulator to 393 ns with 16 accumulators,
  approximately 3.4x faster. The one-million-value case showed almost the same
  ratio: 400,875 ns versus 117,947 ns.
- **Over-splitting result:** The 64-accumulator version regressed to 1,406 ns
  for 4,096 values and 361,326 ns for one million values. The Short can use
  this reversal to introduce finite execution resources and likely register
  pressure without claiming that accumulator count alone determines runtime.
- **Normal optimization caveat:** Under ordinary `-O3`, vectorization changed
  the generated program and the two-accumulator version won this particular
  source-level sweep. The Short must label its headline result as a controlled
  scalar benchmark. A later follow-up can show how compiler vectorization
  changes the comparison again.
- **Working hook:** "I made this sum 3.4 times faster by adding 15 extra
  variables."

### This billion-iteration loop takes zero time

- **Status:** Approved candidate, but not yet selected for Short 5
- **Hook:** "How did one billion C++ loop iterations take zero time?"
- **Opening code:** Sum the integers in a billion-iteration loop without using
  the result. Put the implausible optimized-build measurement on screen within
  the first few seconds.
- **Story:** Show the generated assembly containing no loop. The computation
  has no observable effect, so the optimizer can delete it under the as-if
  rule. Make the result observable or pass it through a benchmark barrier and
  measure again.
- **Payoff:** A benchmark can measure work that never executes unless its
  result is protected from optimization.
- **Visual:** Move directly from the loop to the timing result, then replace the
  source with the nearly empty generated assembly before rerunning the fixed
  benchmark.
- **Constraint:** Use a real optimized build and report the measurements and
  assembly produced on the recording machine. If the result is not literally
  zero, say "almost no time" instead.
- **Ending:** "Now that the loop actually exists, we can start optimizing the
  work inside it."
- **Target:** 20-24 seconds. Reveal the impossible result early, but withhold
  both the explanation and the corrected measurement until later.

### This `push_back` turns a valid pointer into a use-after-free

- **Status:** Strong memory-lifetime candidate
- **Hook:** "This `push_back` frees the memory that this pointer still points
  to."
- **Opening code:** Reserve capacity for one integer, save a pointer to the
  first element, then insert a second element and dereference the old pointer.
- **Story:** Exceeding the known capacity forces a new allocation. The elements
  move, the old allocation is released, and the saved pointer still contains
  the abandoned address.
- **Payoff:** Vector growth can invalidate pointers, references, and iterators
  into its storage even though the vector object itself remains alive.
- **Visual:** Move the first element from a one-cell allocation into a larger
  buffer while leaving the pointer attached to the released buffer.
- **Verification:** Compile the demonstration with AddressSanitizer and reveal
  the resulting use-after-free report.
- **Target:** 20-25 seconds with no CTA.

### This lock unlocks before it protects anything

- **Status:** Strong concurrency and object-lifetime candidate
- **Hook:** "This mutex is unlocked before the protected code even begins."
- **Opening code:** Construct an unnamed temporary
  `std::lock_guard<std::mutex>{mutex};` immediately before incrementing a
  shared counter.
- **Story:** The guard locks in its constructor, reaches the semicolon, is
  destroyed, and unlocks the mutex before the next statement runs. Give the
  guard a name and show that its lifetime now covers the critical section.
- **Payoff:** RAII protects a scope only when the guard object itself remains
  alive for that scope.
- **Visual:** Animate lock, semicolon, destructor, unlock, then the unprotected
  increment. Repeat with a named guard whose lifetime extends to the closing
  brace.
- **Target:** 18-22 seconds with no CTA.

### I moved one line and saved 8 MB

- **Status:** Strong candidate requiring a local size check
- **Hook:** "I moved one line of C++ and made a million objects use 8 megabytes
  less memory."
- **Opening code:** Compare a struct ordered as `char`, `double`, `char` with
  one ordered as `double`, `char`, `char`.
- **Story:** Print both `sizeof` results and reveal the invisible padding added
  to satisfy the `double` field's alignment.
- **Payoff:** Field order can change object size without changing the fields or
  their values. A denser layout also lets more objects fit into each cache line.
- **Constraint:** Measure both sizes with the recording compiler. C++ does not
  guarantee that every target ABI produces `24` and `16` bytes.
- **Visual:** Draw every byte of both object layouts, including padding, then
  multiply the size difference across one million objects.
- **Target:** 18-22 seconds with no CTA.

### I made this faster by adding wasted space

- **Status:** Strong systems-performance candidate requiring a benchmark
- **Hook:** "I made this multithreaded C++ program faster by adding empty
  space."
- **Opening code:** Run two threads that repeatedly update two separate atomic
  counters stored next to each other.
- **Story:** The counters do not logically interact, but they may occupy the
  same cache line and force that line to bounce between CPU cores. Separate
  them with cache-line alignment and benchmark both layouts.
- **Payoff:** Independent variables can still interfere through the memory
  hierarchy. Padding can improve performance by preventing false sharing.
- **Constraint:** Measure the effect on the recording machine before stating a
  speedup. Do not hard-code `64` without clearly identifying it as the measured
  or assumed cache-line size for the experiment.
- **Visual:** Two counters inside one cache line, the line bouncing between
  cores, then one counter per line after alignment.
- **Target:** 20-25 seconds with no CTA.

### Two million increments, wrong answer

- **Status:** Strong concurrency candidate
- **Hook:** "Two threads increment this counter one million times each. The
  answer should be two million. It isn't."
- **Opening code:** Launch two `std::jthread` workers that both increment the
  same ordinary integer one million times.
- **Story:** Reveal the incorrect result, then show both threads reading the
  same value and overwriting one another's increment.
- **Payoff:** `++counter` is not one indivisible operation. The unsynchronized
  program has a data race; replacing the counter with `std::atomic<int>` makes
  the final count reliable.
- **Visual:** Show one lost update as two parallel read-modify-write sequences,
  then rerun with the atomic counter and reveal `2,000,000`.
- **Target:** 20-25 seconds with no CTA.

### `std::move` does not move anything

- **Status:** Strong language-semantics candidate; deferred behind the
  quantified performance follow-up
- **Hook:** "This line does absolutely nothing."
- **Opening code:** Construct a `std::string`, call `std::move(name)` without
  using its result, and print the unchanged string.
- **Story:** Contrast the discarded cast with constructing another string from
  `std::move(name)`.
- **Payoff:** `std::move` does not transfer data. It casts an expression so a
  move constructor or move assignment operator may consume it.
- **Target:** Approximately 20 seconds with no CTA.

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
