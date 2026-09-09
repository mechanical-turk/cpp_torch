# 15: These parallel jobs run one at a time

Proposed MP4: `cpp-async-future-destructor-serial-execution-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P14: reveal serialization early, then reserve the explanation and demonstrated overlap for the payoff. The mystery is why two explicit asynchronous launches fail to overlap.

### Script gate

Claim: discarded futures from these separate std::async(launch::async, ...) statements make each full expression wait for its task. Belief: asynchronous launch syntax alone guarantees overlapping jobs. Expected objection: 'You threw away the futures; retain them or use a pool.' Omit: coroutine schedulers and all launch policies. Keep visible: explicit async policy and unnamed returned futures.

### First frame and edit

Frame one: two async calls and a real event timeline showing job B starts after A ends. Callout: 'Parallel, really?' Circle the statement endings; emphasize 'one at a time'. 0-5s: sequential hand beats match the traces. 5-11s: arrows identify the discarded futures and the waiting boundaries. 11-15s: retain both handles, show a verified overlapping timeline and spread both hands. 15-19s: point to small-job blocks for the next test. Use compact calls; implementation code stays off screen.

### Narration

> These parallel jobs run one at a time. Each async call returns a future. We throw it away immediately, and its destruction waits for that job. Keep both futures alive, and the jobs can overlap. Here they do. Would a thread pool help with smaller jobs? I'll test that next.

### Technical gate

T10. Force launch::async, not the default async/deferred choice. Record task start/end times and thread IDs without racing the logger. Join/get both retained futures before stopping the measurement. Use sufficiently long independent tasks; claiming overlap needs actual overlapping intervals, not only a shorter total. No claim that two hardware cores necessarily run simultaneously.

Candidate search language: C++ std async future destructor, asynchronous tasks, thread pool. Platform demand and hashtags unresearched.

## Analyst's critique

1. The timeline communicates a real failure of expectation without requiring viewers to parse every template, which is a strength. The raw async calls must still fit the viewport at phone size.
2. The missing future is a genuine lifetime trap, but calling these 'parallel jobs' is intent, not observed execution. The first frame correctly exposes serialization instead of pretending concurrency occurred.
3. Two task timelines, statement lifetimes and handle storage can exceed 19 seconds if explained in source and animation separately. Synchronize each event rather than replay the whole story twice.
4. The thread-pool question opens a larger scheduling topic. It is coherent for small tasks, but needs a concrete workload when chosen for production.
5. E2 supports worthwhile corrections about implementation choices. We have no measured channel demand for concurrency, so this is a topic expansion, not a proven growth move.

## Decision and learning

Shortlist for a strong behavioral surprise. The production test is trace-based and should be cheaper than a hardware-counter benchmark.

P15: A genuine state or execution trace can make the opening credible before the viewer understands the source code.

