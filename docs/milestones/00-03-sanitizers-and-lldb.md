# Milestone 0.3 — Sanitizers and LLDB

## Motivation

Make memory-safety and undefined-behavior failures observable before tensor
storage introduces ownership, indexing, and lifetime complexity. Learn the tools
through real failing programs rather than flag memorization.

## Dependencies and diagnostic

- Milestones 0.1 and 0.2 complete
- No prior AddressSanitizer, UndefinedBehaviorSanitizer, or LLDB experience
- Hands-on-first sequence required

## Learning objectives

- Trigger, read, and explain an AddressSanitizer report.
- Trigger, read, and explain an UndefinedBehaviorSanitizer report.
- Distinguish memory errors from broader undefined behavior.
- Build with debug information and useful stack frames.
- Launch under LLDB, set a breakpoint, step, inspect variables/pointers, and read
  a backtrace.
- Add target-scoped sanitizer instrumentation to the Debug testing workflow.
- Explain why compilation and linking both need compatible sanitizer options.
- Restore and verify a clean passing build.

## Hands-on sequence

1. Disposable heap-use-after-free program compiled manually with ASan.
2. Disposable signed-overflow or invalid-shift program compiled with UBSan.
3. LLDB investigation of one failing program.
4. CMake sanitizer option applied to project/test targets.
5. CTest verification under instrumentation.

## Acceptance criteria

- Learner identifies the bug category, allocation/free/use sites, and relevant
  stack frames from ASan output.
- Learner explains the UBSan violation and why ordinary execution is unreliable.
- Learner demonstrates basic LLDB process and state inspection.
- Sanitizer-enabled CTest passes for correct project code.
- One temporary project defect is caught by the expected sanitizer and restored.
- Sanitizer flags do not leak unintentionally into unrelated configurations.
- Working tree finishes clean and evidence is recorded.

## Evidence, review, mastery, and retrospective

### Evidence

- Manually compiled a heap-use-after-free program with ASan.
- Read allocation, deallocation, invalid-read, region-size, shadow-memory, and
  termination sections of the ASan report.
- Manually compiled signed overflow with UBSan and observed the exact operands,
  source location, violated type constraint, and forced abort.
- Used LLDB to set a source breakpoint, run, inspect the pointer and pointee,
  step over `delete`, continue, and print a backtrace.
- Before deletion, LLDB observed `*value == 42`; after deletion, the pointer
  address remained while the stale bytes read as `147`, directly demonstrating
  that address retention does not preserve object lifetime or value.
- Added an opt-in `CPP_TORCH_ENABLE_SANITIZERS` CMake option backed by an
  `INTERFACE` usage-requirement target.
- Verified ASan/UBSan compile instrumentation on the library and consumers and
  runtime link options on executables.
- Sanitized CTest passed for correct code.
- A temporary heap-use-after-free inside `cpp_torch::add` was caught through the
  real sanitized test target and then restored.
- Ordinary Debug CTest remained passing with the sanitizer option disabled.

### Review and mastery

Demonstrated understanding:

- ASan instruments memory operations and maintains shadow metadata describing
  addressability and allocation lifetime.
- UBSan detects executed operations that violate selected C++ semantic rules.
- Instrumentation is inserted at compilation, while violations are detected only
  on executed runtime paths.
- Passing sanitizer runs do not prove absence of defects; coverage matters.
- Sanitizers are normally excluded from shipped binaries due to runtime, memory,
  binary-size, and dependency costs, but should be run proactively rather than
  only after suspicion.
- Sanitizer builds may use optimization and debug symbols; "sanitized" is not
  synonymous with the ordinary Debug configuration.
- The interface target packages non-artifact compiler/linker requirements, and
  propagation ensures consumers of an instrumented static library link the
  required runtime.

Milestone passed.

### Retrospective

The disposable failures made sanitizer output and debugger state concrete before
CMake abstraction. The most important observation was that LLDB could still read
the same pointer address after `delete` while the bytes had already changed;
neither an address nor readable physical memory proves a live C++ object exists.

Deferred topics include allocator internals, ASan quarantine details, recovery
modes, sanitizer compatibility, optimized-debugging behavior, and debugger
watchpoints. They should return when tensor storage and indexing make them useful.

