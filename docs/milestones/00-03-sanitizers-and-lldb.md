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

Pending implementation.

