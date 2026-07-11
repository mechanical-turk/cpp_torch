# Sanitizers and LLDB

## Milestone connection

- Phase 0 — Engineering baseline
- Milestone 0.3 — Sanitizers and LLDB
- Status: passed

## ASan lifecycle model

The heap-use-after-free experiment produced the complete lifecycle:

```text
new int{42}       allocation site
    ↓
delete value      deallocation and shadow poisoning
    ↓
*value            instrumented invalid four-byte read
    ↓
ASan report       use, free, and allocation stacks
```

ASan inserts runtime checks around relevant memory operations and maintains
compact shadow metadata. In the report, one shadow byte represented eight
application bytes and `fd` identified a freed heap region. Redzones and other
poison states allow related out-of-bounds and lifetime violations to be detected.

The pointer remained numerically unchanged after deletion. LLDB read `42` before
deletion and `147` afterward. The debugger's ability to read physical bytes did
not make the C++ dereference valid: the allocated object's lifetime had ended.

## UBSan model

The signed-overflow experiment evaluated:

```text
2147483647 + 1
```

The result cannot be represented by `int`, and signed overflow is undefined in
C++. UBSan reported the operands, type, and exact source expression at runtime.
`-fno-sanitize-recover=undefined` converted the report into an immediate abort.

## LLDB commands exercised

```text
breakpoint set --file ... --line ...
run
frame variable ...
expression ...
next
continue
bt
quit
```

The ASan-aware stop reason was `Use of deallocated memory`. The backtrace showed
the application load flowing into ASan's report and termination machinery.

## CMake integration

An opt-in interface target packages:

```text
compile: -fsanitize=address,undefined -fno-omit-frame-pointer
link:    -fsanitize=address,undefined
```

The interface target emits no library artifact. It carries usage requirements.
When enabled, `cpp_torch` consumes and publicly propagates them so its own object
is instrumented and executables linking the static archive also link the
sanitizer runtime.

Separate build trees preserve distinct configurations:

```text
build/debug       ordinary Debug
build/sanitized   ASan + UBSan Debug
build/release     optimized Release
```

## Retrieval topics

- Why does a passing sanitizer run not prove safety?
- Why must an executable link the sanitizer runtime if a static archive contains
  instrumented code?
- How is object lifetime different from pointer value and readable bytes?
- What does ASan shadow state encode?
- Why should sanitized builds run proactively in CI?

