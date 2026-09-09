# 17: Checking every number beat binary search

Proposed MP4: `cpp-linear-scan-binary-search-small-array-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P16: the current Short contains the actual head-to-head result; only the crossover remains open. This revisits the previously deferred search idea as an unselected candidate, not a change to the production schedule.

### Script gate

Claim: a verified linear membership scan beats binary search for this small sorted array and query set. Belief: fewer comparisons necessarily means less time. Expected objection: 'Small arrays are the exception; binary search wins as size grows.' Omit: a Big O lecture and every search variant. Keep visible: array size, same queries, sorted input, correct hit/miss semantics.

### First frame and edit

Frame one: one straight sweep versus interval jumps on the same short array; callout 'Fewer checks, slower?' Circle the two routes and emphasize 'every number'. 0-5s: sweep one hand straight across. 5-11s: the other hand jumps between candidate intervals while arrows show dependencies. 11-15s: show real medians, same successful-result check, and the linear winner. 15-19s: expand the array visually as the question begins. Do not display two entire implementations.

### Narration

> Checking every number beat binary search. This array is small. The straight scan moves through nearby values, while binary search keeps narrowing the range. Fewer comparisons didn't mean less time in this test. Where does binary search take the lead? I'll grow the array and find out.

### Technical gate

Benchmark normal optimized implementations on the same sorted array and randomized pre-generated queries. Match membership semantics and hit/miss rates; exclude query generation, prevent elimination, vary sizes and cache conditions, inspect SIMD and branch behavior. No win or crossover is assumed. The visual is conceptual, not an exact count of executed machine comparisons.

Candidate search language: C++ linear search versus binary search, small array performance, algorithm benchmarks. Platform demand and hashtags unresearched.

## Analyst's critique

1. This has a strong real disagreement and a coherent crossover question. However, the channel has already considered this topic and deferred it; a better pitch does not remove the benchmark work.
2. The opening presumes viewers know binary search. The two routes help, but both algorithm names and the comparison count may be too much text for the first second.
3. A tiny cherry-picked array can make the win obvious to experts. Show the chosen size and a nearby-size check, while keeping the broader sweep outside the Short.
4. The explanation lists access patterns without proving the measured cause. SIMD, branches and overhead can all matter, so do not attribute the full difference to nearby memory alone.
5. E1/E2 make the challenge-and-proof structure plausible, but there is no causal evidence that a Big O contradiction will repeat the Instagram breakout.

## Decision and learning

Strong concept, benchmark backlog. Keep deferred until a robust normal-build comparison makes the story worth its production cost.

P17: Treat production effort and prior deferrals as selection constraints; a strong hook does not make an unverified experiment ready.

