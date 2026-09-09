# 09: One missing character copies every object

Proposed MP4: `cpp-range-loop-auto-reference-copy-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P08: both loops read the same collection without mutation and produce the same checksum. A single character changes incidental copying, not the required task.

### Script gate

Claim: this by-value range loop copies each buffer-owning object; the reference loop does not. Belief: a short read-only loop is necessarily cheap, or the compiler always erases copies. Expected objection: 'Use const auto&; trivial values should be copied.' Omit: all reference categories and scalar counterexamples. Keep visible: buffer-owning items and a read-only loop.

### First frame and edit

Frame one: 'for (auto item : items)' with a red arrow at the missing & position, plus copy counter 0 waiting to run. Callout: 'Copying the whole thing?' Highlight 'one character'. 0-5s: hand indicates one item and its buffer. 5-11s: repeated copy stamps follow each iteration; a hand beat matches them. 11-15s: insert &, circle it, rerun and reveal zero copies. 15-19s: point to the inline operation that might permit optimization.

### Narration

> One missing character copies every object. This loop only reads the items, but each item owns a buffer. Auto makes a fresh copy on every iteration. Add an ampersand, and we read the original instead. The copies disappear. Could the compiler remove them anyway? I'll inspect the optimized version next.

### Technical gate

Instrument a nontrivial copy constructor and verify equal checksums and copy counts. Use normal compilation; do not call scalar register moves deep copies. The observation is about this object type. In the actual read-only example prefer const auto& if it fits; the spoken focus can remain on &. Instrumentation makes copies observable, so remove that instrumentation for the compiler-elimination follow-up.

Candidate search language: C++ range based for loop, auto reference, unnecessary copies. Platform demand and hashtags unresearched.

## Analyst's critique

1. The hook closely matches the successful tiny-change structure, but copied buffers are a more familiar issue than dependency chains. Familiarity can reduce curiosity even when clarity improves.
2. The ordinary declaration should be 'const auto&' for this read-only use. Reducing the visible edit to one character must not hide that both const and reference semantics matter to the recommended form.
3. An instrumented copy counter prevents some optimizations. The follow-up question is valid only if we explicitly separate the trace demo from an uninstrumented optimized build.
4. The copy counter supplies a complete payoff without a speed ratio. Do not pad the ending with timings unless the next test produces them.
5. E2 makes the compiler objection credible for our audience. It still cannot predict the reach of another compiler-themed clip.

## Decision and learning

Shortlist as a low-production-cost fallback. Verify buffer ownership and instrumentation boundaries before recording.

P09: Check whether the measurement tool makes work observable; instrumentation can change the optimization being discussed.

