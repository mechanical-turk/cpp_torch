# Evidence available to this pitch exercise

## Owned-account observations

- E1: [Short 5 creative and retention review](../../../analytics/reports/2026-09-02-short-05-instagram-retention-and-creative-analysis.md).
  The inspected Instagram master ran 19.77 seconds. The screenshot suggests
  roughly a third of viewers left within four seconds; 43% remained at 0:19.
  The opening promise took about 3.7 seconds. These intermediate retention
  readings are estimates, not exported measurements.
- E2: [September 4 comment review](../../../../docs/logs/analytics-observations.md#2026-09-04-short-5-disagreement-and-intentional-omissions).
  Compiler and boundary objections received substantial discussion. The review
  observed 286 likes / ten replies on one thread, 162 / three on another, and
  13 / eight on a floating-point thread. This qualitative sample supports
  designing worthwhile disagreement; it does not prove controversy caused reach.
- E3: The same creative review records synchronized code changes, red circles
  and arrows, selective caption emphasis, gestures, a measured payoff, and an
  immediate ending after a technical question. Preserve this coherent treatment
  as a working choice, without attributing lift to any isolated component.
- E4: [Short 5 YouTube underdistribution report](../../../analytics/reports/2026-09-02-short-05-underdistribution.md).
  Instagram success is not a YouTube result. Evaluate each platform separately.

No new audience snapshot was requested or pulled for this creative exercise.
The shared evidence supports review questions, not topic-specific forecasts.
Do not claim an unposted pitch will achieve a particular retention or follow rate.

## Technical source register

Sources establish mechanisms and limits, not the performance of an unbuilt demo.
Current draft wording can differ from the recording toolchain's C++23 behavior;
verify every selected demo with the actual compiler and library.

- T1: [Clang floating-point controls](https://clang.llvm.org/docs/UsersManual.html#controlling-floating-point-behavior).
  Reassociation and fast-math change the permitted transformations. Round 1
  uses ordinary binary64 rounding, without fast-math.
- T2: [C++ copy elision](https://eel.is/c++draft/class.copy.elision).
  A named local can qualify for NRVO; an explicit move expression does not
  meet that named-local condition. NRVO remains optional.
- T3: [Vector capacity](https://eel.is/c++draft/vector.capacity) and
  [modifiers](https://eel.is/c++draft/vector.modifiers).
  Capacity changes, relocation, and invalidation matter independently of size.

- T4: [C++ alignment](https://eel.is/c++draft/basic.align) and
  [alignment specifiers](https://eel.is/c++draft/dcl.align). Actual field offsets
  and object sizes require a target-specific check.
- T5: [Linux kernel false-sharing guide](https://www.kernel.org/doc/html/latest/kernel-hacking/false-sharing.html).
  Independently written objects can interfere through one cache line. Padding
  has costs and is not automatically useful for every workload.
- T6: [LLVM auto-vectorization](https://llvm.org/docs/Vectorizers.html).
  If-conversion, reductions, alias checks, and cost models can change the machine
  code. Source syntax alone cannot prove which optimization explains a timing.

- T7: [C++ vector bool](https://eel.is/c++draft/vector.bool) and
  [C++23 draft](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/n4950.pdf).
  An element reference can be a proxy whose assignment changes the stored bit.
- T8: [Unordered-map element access](https://eel.is/c++draft/unord.map.elem).
  Subscript access can insert a missing key; it is not a non-mutating lookup.
- T9: [Output manipulators](https://eel.is/c++draft/ostream.manip).
  endl writes a newline and flushes the stream. Flushing is not a disk-durability
  guarantee, and a newline can also trigger device-dependent buffering behavior.
- T10: [C++ async](https://eel.is/c++draft/futures.async).
  Explicit launch policy and the lifetime of the associated future matter when
  demonstrating overlap. Default-policy behavior is not necessarily asynchronous.

- T11: [C++ range-for expansion](https://eel.is/c++draft/stmt.ranged).
  Each iteration initializes the declared loop variable from the element.
  The declaration determines value versus reference behavior.
- T12: [C++ string views](https://eel.is/c++draft/string.view).
  A view refers to a character sequence; it does not own or freeze that storage.
- T13: [Usual arithmetic conversions](https://eel.is/c++draft/expr.arith.conv).
  Mixed signed/unsigned comparison follows promotion and rank rules; not every
  mixed pair converts to unsigned in the same way.

- T14: [C++ move helpers](https://eel.is/c++draft/forward), the exception
  requirements in T3, and [libc++ relocation implementation](https://github.com/llvm/llvm-project/blob/main/libcxx/include/__memory/uninitialized_algorithms.h).
  The move-if-noexcept choice distinguishes potentially throwing moves from
  non-throwing moves when copying is available. Check the actual library version.

- T15: [Google Benchmark user guide](https://google.github.io/benchmark/user_guide.html).
  DoNotOptimize constrains optimization around an expression but is not proof
  that the original computation remains intact. Inspect generated code.
- T16: [C++ shared ownership](https://eel.is/c++draft/util.smartptr.shared) and
  [libc++ shared_ptr implementation](https://github.com/llvm/llvm-project/blob/main/libcxx/include/__memory/shared_ptr.h).
  Copies share ownership state. Counter implementation and contention costs
  need library-specific inspection and measurement.
- T17: [C++ binary-search algorithms](https://eel.is/c++draft/alg.binary.search).
  Comparison complexity does not establish wall time. The actual input and
  query contracts must match in any linear-versus-binary comparison.

Additional checked primary sources will be appended as their topics enter the loop.
