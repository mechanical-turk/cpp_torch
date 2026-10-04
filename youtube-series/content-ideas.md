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

### Counting distinct numbers: sorting versus hashing

- **Status:** Revived September 15, 2026. Reframed to name `std::unordered_set`
  specifically (the container a C++ programmer reaches for by default) rather
  than hashing in general. Script drafted the same day:
  [short-08-unordered-set-vs-sort/script.md](shorts/short-08-unordered-set-vs-sort/script.md),
  93/100, decision rework (two mandatory production-verification checks
  open: phone-size render, timed read).
- **Premise:** Expected O(n) `std::unordered_set` -- the ordinary, default
  choice, not a claim about hashing as an algorithm family -- loses to
  O(n log n) sorting plus a distinct-value scan for large, high-cardinality
  integer batches.
- **Resolved framing decision:** Do not claim hashing loses; name
  `std::unordered_set` explicitly in the hook and narration. Use the
  mandatory "next test" beat (S10) to name the flat-hash-table counterexample
  as the specific next experiment, rather than disclosing it inside this
  script. This was explored September 15, 2026 across matrix multiplication
  and big-integer multiplication as alternative "worse Big O wins" hooks;
  neither produced a margin close to this one (best alternative was ~1.8x;
  this is 7.52x), so this is the strongest candidate found.
- **Evidence:** `aliases/01-screen-short-form/deduplication/README.md` preserves
  the original 1M-100M grid. Its 100M / 1% duplicates case measured 7.52x in
  sorting's favor. This refers specifically to the reserved standard table.
- **New control evidence:** See
  [optimization investigation](../aliases/01-screen-short-form/deduplication/optimization-notes.md).
  O2/O3, native CPU tuning, LTO, PGO, load factor, power-of-two reservation,
  an allocation arena and Abseil flat_hash_set were tested without disabling
  optimization. At 10M / 1% duplicates, the tuned node-based set still lost
  by 3.09x; the flat table was within 4% of sorting. At 100M / 1%, the flat
  table took 3.02 seconds versus sorting's 2.58 seconds, a much smaller gap.
  At 1M / 1%, the flat table beat sorting by 3.56x.
- **Required framing:** The original result is real, but does not establish
  that sorting beats hashing generally or that Big O is wrong. Do not call
  the 7.52x result the best hash-table implementation. Theoretical crossover
  under fixed-cost models need not occur within practical memory limits.
- **Next script:** Preserve the result-before-solution order and two distinct
  audience questions. Decide how to disclose the flat-table counterexample
  before writing a categorical hash-set hook. No script or upload approved.

### One character crosses a string performance cliff

- **Status:** Selected by the creator for a future recording on September 10,
  2026. Pending benchmark and script; not recorded or scheduled.
- **Hook:** "This character made my code slower."
- **Premise:** Benchmark constructing and destroying `std::string` objects at
  successive lengths around the recording library's small-string optimization
  boundary. One extra character can change inline storage into a separate
  allocation. The central payoff is runtime, not memory usage alone.
- **Opening:** Two almost identical strings, the extra character circled in
  red, and the callout "One character?". Introduce the actual timing comparison
  without exposing every result before its reveal.
- **Progression:** Show the character change, the inline buffer filling, the
  separate allocation, and the measured runtime difference. Immediately ask
  "Why does allocating that tiny amount cost so much?" Then propose testing
  whether reusing the string recovers the speed, and cut.
- **Benchmark handoff:** Use normal optimized builds, runtime-provided inputs,
  the same iteration count and benchmark boundaries, and prevent discarded
  work. Sweep nearby lengths rather than choosing only two favorable points.
  Check allocations separately from the timing run. Confirm the threshold for
  the actual standard library; do not assume 15, 22, or another universal size.
  Keep all timings and speedup factors unknown until measured. Abandon or
  revise the speed-cliff claim if the experiment does not support it.
- **Creative rationale:** Apply Short 5's familiar-code, tiny-change, measured
  payoff structure and its opening-retention lesson. Show the meaningful change
  immediately. Preserve the post-reveal why-question and specific continuation;
  neither treatment has an isolated causal effect on reach or follows.
- **Open critique:** Easy to understand and visually compact, but more
  surprising than opinionated. Experienced C++ viewers may recognize SSO
  immediately. Do not turn one construction benchmark into "strings are slow."
- **Candidate search language:** C++ string performance, small string
  optimization, heap allocation, string benchmark. Platform-specific SEO and
  hashtags remain unresearched; these are topic labels, not approved copy.
- **Technical reference:** [Microsoft's string implementation explanation](https://devblogs.microsoft.com/oldnewthing/20230803-00/?p=108532).

### More optimization made this slower: -O2 versus -O3

- **Status:** Saved at the creator's request on September 10, 2026 as a
  lower-priority exploratory benchmark. Creator considers the idea weak and
  too platform-dependent for a recording commitment. No regression found yet.
- **Hook direction:** "More optimization made this slower." Avoid "maximum"
  because -O3 is not a universal maximum-performance configuration.
- **Premise:** Build the same C++ source with the same compiler version,
  target settings and inputs, changing only -O2 to -O3. Investigate a
  substantial, repeatable runtime regression and the transformation behind it.
- **Visual:** Circle the 2 in the compiler command and change it to 3. Keep
  source unchanged, show the relevant generated-code change, then reveal two
  measured runtime bars. Ask why the more optimized version lost, then propose
  testing optimization for size.
- **Proof handoff:** Alternate run order, verify identical correct outputs,
  repeat across inputs and sizes, and record compiler/CPU details. Larger
  assembly does not establish instruction-cache causation. Do not disable
  individual optimizations in the headline comparison or manufacture bad code
  to force a result. Keep any pass-isolation experiments separate diagnostics.
- **Reason for deferral:** The effect can change with compiler version, CPU,
  workload and input size; finding and explaining a strong example may cost
  more production time than its entertainment value warrants. Promote only
  after a clear mechanism and visually meaningful regression emerge.
- **Technical reference:** [Clang optimization-level documentation](https://clang.llvm.org/docs/CommandGuide/clang.html).

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

- **Status:** Real single-threaded benchmark obtained September 15, 2026.
  A crossover exists, but it is modest and arrives earlier than folklore
  suggests; needs a decision on whether the margin clears the bar before a
  script is written.
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
- **Measured evidence:** `~/code/matmul-complexity` (`matmul.cpp`,
  `benchmark.cpp`). Square double matrices, single-threaded, Clang -O3
  -mcpu=native -flto, i-k-j loop order for cubic (contiguous inner access,
  no SIMD intrinsics), Strassen with a practical recursion cutoff rather
  than pure recursion to 1x1 (a pure cutoff is computationally infeasible
  to measure past a few hundred and would be a misleading setup). Verified
  against a naive reference for every tested size.
  - The crossover point depends heavily on the Strassen cutoff, which is
    itself a real tuning choice, not a fixed fact: cutoff 64 already ties
    or beats cubic starting around n=128-256; cutoff 16 keeps cubic ahead
    through roughly n=1024, but only by 1.16x-1.83x, not a blowout.
  - Cache blocking the cubic side (tiling, still no SIMD intrinsics) did
    not reliably help on this machine at the block sizes tried (16-256);
    it was sometimes slower than the unblocked i-k-j loop. A genuinely
    hardware-aware cubic likely needs real SIMD/register blocking to push
    the crossover meaningfully higher -- untested here.
  - No result approaches the original dedup Short's 7.52x headline. The
    largest clean cubic win found is roughly 1.8x, at small matrices
    (n<=128) against an aggressively-cut-off Strassen.
  - **Open question before scripting:** is a ~1.3x-1.8x margin a strong
    enough disagreement for S01, or does this need a stronger hardware-aware
    cubic (SIMD/register blocking) before the hook is worth recording?

### Worse-Big-O-wins candidates explored and rejected (September 15, 2026)

- **Status:** Explored and rejected; recorded so this ground is not
  re-benchmarked without a new angle.
- **Why explored:** Looking for another "asymptotically worse algorithm
  wins in practice" hook after the sorting-vs-hashing Short (above) turned
  out to be specific to `std::unordered_set`, not hashing in general.
- **Insertion sort (`O(n^2)`) vs `std::sort` (`O(n log n)`) for small `n`:**
  Dead. Measured single-threaded, `n` from 4 to 512: insertion sort's best
  margin was 1.13x at `n=8` and it loses outright above `n=64`. libc++'s
  `std::sort` already falls back to insertion sort internally for small
  partitions, so there is no real gap to show.
- **`std::vector` linear scan (`O(n)`) vs `std::set` lookup (`O(log n)`):**
  Dead. Linear scan loses by 100x+ at `n=32768` and never wins. A
  cache-friendly `std::vector` + `std::binary_search` does beat `std::set`
  by roughly 2-2.5x, but that is a same-complexity-class win from container
  internals (pointer-chasing tree vs. contiguous array) -- the same
  mechanism as the discarded `std::unordered_set` lesson under a different
  API name. Rejected under S18 without a materially new angle.
- **Schoolbook (`O(n^2)`) vs Karatsuba (`O(n^1.585)`) big-integer
  multiplication:** Deferred, not dead. Real crossover exists around 64-128
  limbs (roughly 2048-4096 bits) depending on Karatsuba's recursion cutoff,
  which lands near recognizable RSA key sizes -- a promising relatable
  framing. But margins near the crossover were thin (roughly 1.0x-1.2x) and
  the exploratory benchmark (`/tmp/karat_sweep2.cpp`, not preserved) used
  too few repetitions to trust. Worth a properly built benchmark
  (`~/code/karatsuba-complexity` has the correctness-checked
  `schoolbook_multiply`/`karatsuba_multiply` implementation already) before
  deciding if it clears S01.

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
