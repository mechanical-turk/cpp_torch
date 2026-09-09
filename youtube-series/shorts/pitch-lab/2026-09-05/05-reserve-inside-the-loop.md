# 05: Reserving memory made this loop slower

Proposed MP4: `cpp-vector-reserve-growth-performance-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P04: a speed headline requires timed evidence, while allocation traces explain the visible work. Unlike round 4, this pitch explicitly remains conditional on a real runtime result.

### Script gate

Claim: reserving one extra slot before every append slows this tested vector build compared with its normal growth. Belief: reserve is always the performance choice. Expected objection: 'You called it in the wrong place; reserve the final size once.' Omit: allocator internals and growth-factor survey. Keep visible: reserve inside the loop, final-size knowledge unavailable to that version, identical produced contents.

### First frame and edit

Frame one: the reserve line inside a three-line append loop is circled. Callout: 'Helpful reserve?' Show a growing bar repeatedly being replaced, not a full allocator diagram. 0-6s: point to the reserve call on successive iterations. 6-11s: arrows track relocation of the same element blocks, with a hand sweep on each rebuild. 11-15s: remove the line and reveal measured time plus allocation counts. 15-19s: one up-front allocation block appears for the follow-up.

### Narration

> Reserving memory made this loop slower. I reserve one extra slot before every append. On this library, that keeps reallocating and moving the old elements. Remove that call, and the vector grows in bigger steps. Here are the timings. What if we reserve everything once? I'll measure that next.

### Technical gate

T3. Verify the actual library's capacity trace; do not assume reserve must allocate exactly the requested size. Compare normal growth, per-append reserve and up-front reserve outside camera timing setup. Use identical final data, interleaved medians, optimized builds and allocation counts. If no meaningful slowdown appears, do not record this script. Avoid an enormous quadratic run solely for drama.

Candidate search language: C++ vector reserve, vector reallocation, dynamic array performance. Platform demand and hashtags unresearched.

## Analyst's critique

1. The setup is plausible but visibly poor usage. If the presentation pretends this is idiomatic reserve, discussion will question competence rather than compare meaningful tradeoffs.
2. The title withholds the decisive location until the second sentence. Keep the loop containing reserve visible on frame one, as planned.
3. Allocation counts plus median times risk becoming two competing payoffs. Use allocations as the causal visual and time as the final result, with no extra table columns.
4. E2 suggests viewers will supply the up-front reserve correction, but the script already announces it. That may leave less to discuss than the author expects.
5. The shared under-20-second limit leaves little room to explain unknown final size. The follow-up must not imply a size known all along was deliberately ignored for bait.

## Decision and learning

Reserve candidate. Useful warning, but weaker as the next release because the conflict can collapse into correcting a conspicuous misuse.

P05: Do not manufacture the objection with obviously poor setup; show a credible engineering choice worth debating.

