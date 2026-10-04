# Chapter 13 preparation and review

Recording script: [script.md](script.md). Research: [keyword-research.md](keyword-research.md).
Verifier: [verify-script.mjs](verify-script.mjs), report: [verification-run.json](verification-run.json).

## History of this script

The first draft was scrapped for clerical and formatting errors (banned
"last time" wording, displayed outputs that did not match the program, unclear
directions) and an abrupt cold open. The second draft opened with momentum and
ended with residual connections. The creator then reordered the episode: build
a Sequence and abstracted layer classes, stack them, train a deeper network, and
only then introduce momentum and velocity as the fix. A third draft did that
with a type-erased `Layer` wrapper (`Concept` and `Model`). After discussing
what type erasure buys and costs, the creator chose a plain base class for now.

The creator then asked for networks to be built by explicitly listing their
layers, never through a depth parameter or loop, so the script does not frame
the layer list as a way to make depth "just a number". A braced variadic
`Sequence` constructor was then built and verified, but the creator set it
aside because of how it interacts with `unique_ptr` (each layer is built as a
temporary and then moved onto the heap). The interface is `push_back` taking a
`unique_ptr<Layer>` again, and the creator asked why the list holds pointers at
all; the answer is now in the narration and in decision 1 below.

The creator later asked that the first deeper network tried be a sensible one
that can raise accuracy, so Section C now tries four hidden layers first (a
small improvement) before doubling to eight (the stall).

Residual connections are no longer in the episode; they appear only in the
closing next-episode list. Chapter 12's on-screen closing list is not carried
forward, by creator direction, and the script does not refer to it.

## Scope and checklist plan

Continue in the actual recorded Chapter 12 main.cpp. `MLP`, `train_xor`, the
regression trainers and the old one-argument `gradient_step` are untouched.
`Linear` and `Tanh` are edited to inherit from the new base class; their
behavior does not change. New code: an abstract `Layer` (two pure-virtual
functions and a virtual destructor), `Tanh::parameters()`, `Sequence` (owns its
layers through `std::unique_ptr<Layer>` and grows through `push_back`), a
`train_mnist()` model built by explicit `push_back` calls (first the same
shape as `MLP`, then eight hidden layers written out one by one), and a
`gradient_step` overload with velocity.

- **Opening promise:** make the MNIST network deeper by stacking layers, see
  what breaks, and fix part of it with momentum.
- **Curiosity question:** why does a deeper network do worse, and what can an
  optimizer change? Payoff: the stalled 63.85% run, then the 75.05% run with
  momentum.
- **Distinctive viewer benefit:** a reusable layer list built with ordinary
  inheritance, a refactor proven to compute exactly the same numbers, a
  measured failure, and a measured partial fix, all in hand-written C++.
- **First useful action:** begin the first edit, the `Layer` base class, after
  about 29 seconds.
- **First payoff:** `Linear` and `Tanh` working as layers, then `Sequence`,
  then the first measured result. See the runtime estimate for times.

| ID | Intended treatment |
| --- | --- |
| L01 | Concrete promise, curiosity question and boundary above; the cold open says what will break and what will be fixed. |
| L02 | First two sentences name the C++ network, MNIST, the current 88.2%, the goal (deeper) and the fix (momentum). The title overlay is specified for the first five seconds. No greeting, series recap or roadmap. Thumbnail alignment is pending until packaging exists. |
| L03 | Existing `MLP` and the accuracy line are on screen from frame zero; the first edit starts after 72 spoken words, about 0:29. |
| L04 | Audited as partial. The requested order builds the layer list before any run, so the first measured result is a few minutes in. |
| L05 | A: a network can be built from any layers. B: the rebuilt network matches `MLP` exactly. C: four hidden layers help a little, then doubling to eight stalls training. D: momentum gets it moving. |
| L06 | The base class appears when a list of layers is the goal; the reason for pointers is given where the vector is introduced; each edit has a one or two sentence preview; momentum arrives only after the stall has been measured. |
| L07 | Why a list needs a common base class; why the destructor is virtual; why `override` is used; why the deep network stalls (measured); why small agreeing steps add up under momentum. |
| L08 | Eleven literal Before/After edits replayed by the verifier against the frozen Chapter 12 source; five checkpoints compiled and run. |
| L09 | Each run answers a question that decides the next step: does the refactor preserve behavior, do more layers help, and where do they stop helping, does momentum help. |
| L10 | Directions name the exact function, line or output lines to point at. Rendered highlighting is a production check. |
| L11 | 1,059 spoken words; see the runtime estimate. |
| L11a | Estimated 10.5 to 12 minutes, inside the target. |
| L12 | Ends with a measured, honest partial fix and a concrete continuation; the deeper network still trails the shallow one, and the script says so. |
| L13 | Itemized recap, three next-episode items, exact sign-off, clean tail. No Q&A. |
| L14 | script.md holds the filename, one canonical `>` narration, exact edits and expected output only. |
| L15 | Keyword research precedes the draft; the spoken-keyword map is checked below. |
| L16 | Evidence, conditions and limits stated below; no reach prediction or release approval. |

## Starting point and verification

- Frozen source: `verification/episode-12-baseline.cpp`, SHA-256
  `9b0d23f4e87fe88b5d8a9f46c1dda2a359e2a4f13bd7784eb4c2f4413e173ea7`.
  Byte-identical (ignoring trailing newline) to the live recording `main.cpp`
  and to public commit `c9918e8`.
- Replay with `node youtube-series/chapter-13/verify-script.mjs` from the
  Content HQ root. It never modifies the recording source and checks that it is
  unchanged afterward. The latest run (Apple clang 21) is in
  [verification-run.json](verification-run.json). It passed:
  - narration lint: no em or en dashes, no reference to a previous episode, no
    "imagine" or "picture this", no canned contrasts, no trailing whitespace or
    tabs anywhere in the script;
  - all 11 edits replay in order; each Before block exists and is unique in the
    evolving source;
  - all five checkpoints compile and run at `-O2`; all 26 displayed output lines
    appear verbatim in real program output;
  - `TensorNode` unchanged from the baseline;
  - compile-time checks: `Layer` is abstract, has a virtual destructor, and both
    `Linear` and `Tanh` derive from it; `MLP` does not;
  - a supplementary sanitizer-enabled test program: hand-computed two-step
    momentum values; momentum 0 equals the old update; the old `gradient_step`
    is unchanged; a `Sequence` of `Linear`, `Tanh`, `Linear` equals `MLP`
    exactly, output and every parameter, bit for bit; finite-difference checks
    of every parameter in a `Sequence` with three hidden layers; parameter
    handles reach the model; empty and Tanh-only sequences; `Linear` and `Tanh`
    reached through `std::unique_ptr<Layer>`; `parameters()` on a const
    `Sequence`; the eight-hidden-layer model, built with explicit `push_back`
    calls exactly as in the script, has 18 parameter tensors;
  - the complete final program, including every Chapter 12 assertion and the
    five-epoch training run, under AddressSanitizer and UBSan.
- Compiling the final program with `-Wall -Wextra` gives the same three
  unused-variable warnings as the Chapter 12 file and no new warnings, so the
  virtual destructor introduces no new diagnostics.
- The outputs in the script (seed 42, first 10,000 training images, five
  epochs, batch size 64, 2,000-image test subset):
  - Chapter 12 network: epoch 5 loss 0.271741, 88.2% (1764/2000);
  - the same network built as a `Sequence`: identical losses in every epoch and
    identical accuracy;
  - four hidden layers, plain gradient descent: losses 1.777, 0.741658,
    0.450117, 0.342193, 0.278237; 89.25% (1785/2000);
  - eight hidden layers, plain gradient descent: losses 2.30029, 2.24043,
    1.64858, 1.22419, 1.03331; 63.85% (1277/2000);
  - eight hidden layers with momentum 0.9, learning rate 0.1: losses 1.79133,
    0.917755, 0.80852, 0.797441, 0.685964; 75.05% (1501/2000).
  These are identical to the run made with the earlier type-erased design, as
  expected: the layers and the random draws are the same.
- **Why the deep network stalls.** Measured at the starting weights on a real
  64-image MNIST batch and asserted by the verifier on every run:
  - the initial loss is 2.30285, against ln 10 = 2.30259, the loss of guessing;
  - activations at the last hidden layer are 0.0153 of the first layer's size,
    and the gradient reaching the first hidden layer is 0.0174 of the last's,
    about 0.56 per layer;
  - the overall weight-gradient norm is 0.0136, against 0.873 for the
    one-hidden-layer network, 64 times smaller; the narration says "more than
    fifty times";
  - over the first 100 plain-gradient-descent batches, consecutive gradients of
    the first weight matrix have a mean cosine of 0.49, so they tend to point
    the same way; the narration says "tend to";
  - arithmetic consistency, not a proved cause: uniform weights in
    +/- 1/sqrt(n) have variance 1/(3n), which scales the signal by about 0.577
    per layer, close to the measured 0.56. The script does not name a cause and
    does not blame tanh.
- **Why four hidden layers is the first deeper step.** Plain gradient descent
  with the same budget gave (hidden layers: accuracy): 1: 88.2%; 2: 88.35%; 3:
  88.95%; 4: 89.25%; 5: 87.3%; 6: 80.4%; 8: 63.85%. Four is the best of the
  depths tried and the last one that improves on the start. The gain is 21 more
  correct answers out of 2,000 on one seed, so the script says "a little" and
  does not call it a reliable improvement.
- **What momentum does and does not do.** The same sweep with momentum gave
  (hidden layers: plain, momentum): 1: 88.2%, 91.15%; 2: 88.35%, 89.35%; 3:
  88.95%, 90.55%; 4: 89.25%, 88.4%; 6: 80.4%, 83.0%; 8: 63.85%, 75.05%. Momentum is not a universal accuracy gain (it was slightly lower at
  four layers). The script therefore claims only that momentum fixes the slow
  start of the stalled eight-layer run, and that the deeper network still trails
  the shallow one.
- `std::uniform_real_distribution` need not give identical samples on every
  standard library; re-run the verifier if the toolchain changes.

## Runtime estimate

1,059 spoken words is about 7.1 minutes at 150 words per minute. The edits type
about 64 lines that are new or changed (the seven repeated hidden-layer pairs are
mostly copy and paste); at roughly 3 seconds per line that is up to about 3.2
minutes, much of it overlapping narration spoken while typing. Five checkpoints
(four training runs and the existing result shown at the start) add about 1.3
minutes. The upper bound is about 11.9 minutes and overlap lowers it, so the
estimate is about 10.5 to 12 minutes before cuts, with training waits cut from the
edit. This is arithmetic from the draft, not a timed read.

| Milestone | Upper-bound elapsed (speech + typing, no overlap) |
| --- | --- |
| First edit begins | about 0:29 |
| `Layer`, `Linear` and `Tanh` working together | about 1.8 min |
| `Sequence` complete | about 3.8 min |
| First measured result: `Sequence` matches `MLP` | about 5.3 min |
| Four hidden layers, a small improvement | about 5.8 min |
| The eight-layer network stalls | about 6.4 min |
| Momentum result | about 9.4 min |

| Section | Spoken words | Edits | Lines typed | Checkpoints |
| --- | ---: | ---: | ---: | ---: |
| A. List of layers | 360 | 5 | 35 | 1 |
| B. Stack the layers | 117 | 1 | 4 | 1 |
| C. Make it deeper | 150 | 2 | 7 | 2 |
| D. Momentum | 332 | 3 | 18 | 1 |
| E. Recap | 100 | 0 | 0 | 0 |

## Architecture and scope decisions

1. `Layer` is an ordinary abstract base class, the first runtime polymorphism
   in the series. Type erasure (a `Concept` and `Model` wrapper) was built,
   verified and then set aside at the creator's direction: the code base owns
   `Linear` and `Tanh`, so intrusive inheritance costs nothing here, and the
   base class removes about 30 lines of template code and the densest
   narration in the episode. The price is that call sites say
   `std::make_unique<Linear>(...)` and that the list holds pointers.
   **Why pointers.** Measured here: `sizeof(Layer)` is 8, `sizeof(Tanh)` is 8 and
   `sizeof(Linear)` is 40, and `std::vector<Layer>` does not compile because
   `Layer` is abstract. Even if it were concrete, a vector of `Layer` objects
   would slice each layer down to its base part. Elements of one vector must
   have one size, and a virtual call needs the real object, so the list holds
   same-sized pointers that lead to the real layers. The alternative that owns
   layers by value is `std::vector<std::variant<Linear, Tanh>>` with
   `std::visit`; it was built as a scratch check, works on this code, and
   matches `MLP` exactly (48 bytes per element). Its cost is a closed set of
   layer types, edited in one place whenever a layer is added, and no base class.
2. `parameters()` is `const` in the base class, because it only returns tensor
   handles. `Linear::parameters()` already was, so `Linear` needed no signature
   change. `MLP::parameters()` is not const and is left alone; `MLP` is not a
   `Layer`.
3. `Linear` and `Tanh` are edited in place, using `override` so the compiler
   checks the signatures. Their behavior is unchanged, and the exact-match run
   proves it.
4. `Sequence` stores `std::vector<std::unique_ptr<Layer>>` and owns its layers.
   Its only way in is `push_back(std::unique_ptr<Layer>)`. A constructor taking
   `std::initializer_list<std::unique_ptr<Layer>>` cannot work, because elements
   of an initializer list cannot be moved from. A variadic constructor that
   takes the layers by value (`Sequence model{Linear(...), Tanh()}`) was built
   and passed verification; it was set aside because it builds each layer as a
   temporary and then moves it onto the heap, and it is unconstrained (a
   non-`Layer` argument fails with a long template error). `Sequence` is not
   itself a `Layer`; nesting is not needed in this episode.
5. Rebuilding the existing network as a `Sequence` is a deliberate behavior
   check. The playbook asks that a refactor's preserved behavior be
   distinguished from intended behavior changes. The run must match the old
   numbers, and the verifier proves it exactly.
6. The old `gradient_step` stays for the regression and XOR call sites. Only
   `train_mnist` uses the momentum overload.
7. Networks are built by explicitly listing their layers. There is no depth
   parameter, loop or helper, and the script says nothing that frames the layer
   list as a way to vary depth. The eight-hidden-layer network is written out as
   17 `push_back` lines in all, which is repetitive on screen but is what the
   creator asked for. It was chosen because it is the clearest stall, not the best shape, and the
   script does not present it as a good network.
8. The first deeper network is four hidden layers, not eight. Four was the best
   of the plain-gradient-descent depths tried (88.2%, 88.35%, 88.95%, 89.25%,
   then 87.3% at five), so the narrative is "more layers help a little, so try
   twice as many" and then the stall. The four-layer run also shows the first
   epoch starting slower (loss 1.78 against 0.99), which the narration notes once
   and does not over-interpret. The improvement is 21 answers out of 2,000 on a
   single seed and is described as "a little".

## Checklist audit

| ID | Status | Points | Evidence and remaining risk |
| --- | --- | ---: | --- |
| L01 | PASS | 10/10 | Concrete promise and a question (what breaks, what momentum fixes) in the first two sentences; the scope boundary is explicit. |
| L02 | PASS | 10/10 | Subject, dataset, current result, goal and fix in the first two sentences; overlay specified. Thumbnail and title alignment is pending until packaging exists. |
| L03 | PASS | 8/8 | 72 spoken words before the first edit, about 0:29, an estimate inside the 30-second target. Needs rehearsal. |
| L04 | PARTIAL | 4/8 | The requested order builds the layer list before any run. Working layers land at up to about 1.8 minutes, `Sequence` at about 3.8, and the first measured result at up to about 5.3 minutes, past the one-minute target. Repairs inside the requested order: tighten the Section A narration, or accept the cost of the order. |
| L05 | PASS | 8/8 | Each section adds a capability and a check: a layer list, a proven equivalent refactor, a deeper explicitly listed network that first improves and then stalls, and momentum with a measured recovery. |
| L06 | PASS | 8/8 | Each new type appears at its use with a preview, and momentum follows the measured stall. |
| L07 | PASS | 8/8 | The reasons for the base class, the pointers in the list, the virtual destructor and `override`, the small gradients and the velocity are spoken beside the code, and the gradient claims are measured. |
| L08 | PASS | 10/10 | The verifier replays all 11 edits against the frozen source, runs every checkpoint, and matches all 26 displayed output lines. |
| L09 | PASS | 6/6 | Every run answers a real question; gradient, equivalence and correctness checks stay off camera. |
| L10 | PASS | 5/5 | Directions point at specific functions, lines and output lines. Rendered highlighting is unverified. |
| L11 | PARTIAL | 2.5/5 | Dense but connected narration, longest in Sections A and D. Actual cadence, hold times and pace across ten edits need a timed read. |
| L11a | PARTIAL | included in L11 | Estimated 10.5 to 12 minutes, inside the range. A timed read is still required. |
| L12 | PASS | 4/4 | The episode delivers what it promised, states plainly that momentum only partly fixes the deep network, and ends with a concrete continuation. |
| L13 | PASS | 4/4 | Recap, three next-episode items, exact sign-off, clean tail. No Q&A. |
| L14 | PASS | 2/2 | script.md contains only recording material; this review and the keyword research are separate. |
| L15 | PASS | 2/2 | Keyword research precedes the draft. Spoken terms: C++ neural network, MNIST, deeper, momentum, layers, base class, Sequence, Layer, vanishing gradient, velocity, gradient descent all appear in the narration at their point of use; residual connections appear only in the closing list, as planned. |
| L16 | PASS | 2/2 | Evidence, conditions and limits are stated; no reach claim, analytics refresh or publication step is implied. |

Total: 93.5/100.

## Critique

The base class is the right weight for this episode. It reads the way most C++
viewers expect, and the editing stays small: `Linear` gains a base class and
two `override` marks, and `Tanh` gains one function. The first working layers
arrive around 1.8 minutes, against 3.8 for the type-erased draft.

The list of pointers needed an explanation that the earlier drafts did not
give. The narration previously said only that each layer "keeps its real type".
It now says why a vector of `Layer` objects cannot work (`Layer` is abstract and
each kind of layer has a different size) and why pointers do, which matches what
was measured: `Layer` and `Tanh` are 8 bytes and `Linear` is 40. A pointer-free
design with `std::variant` works on this code and is recorded in the decisions,
but it needs a closed list of layer types, so it was not adopted.

The step from `Tanh` to `Sequence` was abrupt in the earlier draft: the narration
went straight from the last `Layer` edit to "one type can stand for any layer".
It now stops on `MLP` first. `MLP` already holds three layers, passes the input
through them in order and joins their parameters, and the narration says that
is the job wanted for any list of layers, so `Sequence` repurposes `MLP`'s
design. It says `MLP` itself stays for the XOR example, which is true (`MLP`
is not edited), and it keeps the reason for pointers as its own beat. The cost
is about 77 spoken words: Section A is now the longest section at 360 words and
the first measured result moves to up to about 5.3 minutes, which makes the L04
gap slightly larger. If time must be recovered, shorten the second paragraph
of that transition (the pointer reasoning) before the first.

Section C was restructured so the first deeper network is a sensible one. The
earlier draft jumped straight to eight hidden layers, which made depth look like
a mistake from the start. It now tries four, which improves accuracy slightly
(89.25%), and only then doubles to eight, which stalls. That is a more honest
shape for the story (depth helps up to a point), it gives the stall a "what
changed" contrast, and it makes the later "momentum fixes the slow start" claim
easier to read. The costs are one more run and edit and about 67 more spoken
words, which push the estimate to 10.5 to 12 minutes and the first measured
result to up to about 5.3 minutes with the four-layer result at about 5.8.

The deeper network is written out as 17 `push_back` lines with no loop or depth
parameter, as requested. Seven identical Linear and tanh pairs are repetitive
on screen, but they are mostly copy and paste, and they make the network
exactly what it says it is. Nothing in the script frames the list of layers as
a way to vary depth. The call sites carry `std::make_unique` noise, which is the
price of the simpler `Sequence`, and the script explains `make_unique` once,
where it first appears.

Rebuilding the existing network as a `Sequence` and getting identical numbers
still gives the abstraction a concrete proof before it is used, and the stall
in the deeper network then gives momentum a visible problem to solve, so the
optimizer arrives as a fix rather than as a topic.

The main weakness is L04. Building the layer list before any run puts the first
measured result a few minutes in, and nothing in the requested order removes
that. It is better than the type-erased draft (first result at up to about 5.3
minutes instead of 6.6), but still well past one minute. The cheapest repair is
to tighten the Section A narration. The new explanation of why the list holds
pointers is the newest passage there, so it is the first candidate if a cut is
needed, though it answers a question viewers will reasonably have.

The costs of the base class are modest. It edits two classes viewers already
have, though behavior is unchanged and the exact-match run shows it. The list
holds pointers, so every layer is a separate heap allocation; that is not a
concern at this scale. If a later episode needs layers the code base does not
own, or layers with different `forward` signatures, type erasure becomes worth
revisiting.

The explanation of the stall is deliberately restrained. The usual textbook
account blames activation slopes, but the measurement shows the signal already
shrinking by about 0.56 per layer at these starting weights, so the narration
says only that each layer makes what passes through it smaller, that the weight
gradients end up more than fifty times smaller, and that successive gradients
tend to agree. Nothing claims a cause beyond that. The next episode's first
item, why signals shrink in deep networks, is where the cause belongs.

Momentum is presented honestly. It rescues the stalled run, from 63.85% to
75.05% and from a slow start to an early one, and the script says the network
still trails the shallow one. The earlier sweep shows momentum does not always
raise accuracy, which is why the script does not generalize.

Unverified: spoken pacing, actual runtime, rendered overlays and highlights,
thumbnail and title alignment, and the recording itself.

## Final score

93.5/100. Decision: rework. L04 is a mandatory check and is partial, so the
rubric does not let the total average it away. The gap comes from the requested
order and is repairable by tightening Section A or by accepting the later first
payoff as a recorded tradeoff. L11 and L11a await a timed read. This is
sequential self-review against a verified implementation, not audience
validation. No thumbnail, recording, publication or release is approved by
this score.
