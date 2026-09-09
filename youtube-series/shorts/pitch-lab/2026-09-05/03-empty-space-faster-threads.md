# 03: Empty space made these threads faster

Proposed MP4: `cpp-false-sharing-cache-line-padding-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P02: connect the memory change to an observable task outcome. Keep P01's concrete edit, but invert the familiar preference for compact data.

### Script gate

Claim: separating these independent counters improves this measured two-thread workload. Belief: nearby data is always faster. Expected objection: 'Use local counters; you should not hammer shared atomics.' Omit: cache protocol states, alternative reductions, NUMA. Keep visible: two threads, different atomic counters, same update count and memory ordering.

### First frame and edit

Frame one: two counters packed together and two visibly separated, with the same update task. Callout: 'Wasted space wins?' Circle the added gap; emphasize 'empty space' in captions. 0-5s: two hands identify the workers. 5-11s: a red arrow bounces between workers around one shared cache-line box. 11-15s: split into two boxes, show actual median bars and point to the winner. 15-19s: bring hands together for the next test. Use a conceptual cache-line drawing, not a claim about the exact byte size.

### Narration

> Empty space made these threads faster. Each thread updates its own counter, but both counters sit in one cache line. Their writes keep fighting over that line. Separate the counters, and this run finishes sooner. Should we keep the counters local instead? I'll test that next.

### Technical gate

Measurement-dependent: do not record this claimed win until a reproducible optimized benchmark shows it. Use atomic counters to avoid a data race, match memory order, synchronize starts, verify distinct-core execution where possible, check addresses and target cache-line size, and exclude thread startup. Repeated interleaved runs plus coherence evidence are needed for the mechanism claim; timing alone is weaker. See the Linux kernel false-sharing documentation.

Candidate search language: C++ false sharing, cache line padding, multithreading performance. Platform demand and hashtags unresearched.

## Analyst's critique

1. The hook contains a useful contradiction, but the counter diagram can look like decorative spacing unless it clearly represents memory. That ambiguity sits exactly in E1's vulnerable opening window.
2. Explaining threads, cache lines, and ownership introduces three unfamiliar ideas. A clean animation may handle them; miniature source code plus a benchmark will not.
3. A win is not yet measured. Hardware placement or thread startup could dominate, and timing alone cannot identify coherence traffic as the cause.
4. The local-counter objection is substantive, which fits E2. However, the video must frame shared counters as the experiment, not as the best implementation of a sum.
5. The next test stays inside the same task, but the current payoff needs to show the measured separation effect before asking about a better architecture.

## Decision and learning

High-interest benchmark candidate, on hold for reproducible measurements and a readable cache-line animation.

P03: Separate a real timing result from its proposed cause; a benchmark winner alone does not prove the mechanism.

