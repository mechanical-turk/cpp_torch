# 10: These unused fields are slowing the loop

Proposed MP4: `cpp-data-layout-hot-cold-fields-performance-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P09: keep timing uninstrumented and use layout inspection separately. Retain the familiar loop while changing what memory it must traverse.

### Script gate

Claim: isolating a frequently scanned field improves this measured scan over large records. Belief: fields not read by the source loop cannot affect its speed. Expected objection: 'This is structure-of-arrays; the compiler may also vectorize it differently.' Omit: a full data-oriented-design lesson and every cache level. Keep visible: one field read, identical values, same result, layout change rather than deleted information.

### First frame and edit

Frame one: a one-line sum points into repeated records with a narrow colored value and broad grey fields. Callout: 'Unused, but expensive?' Circle the grey span; highlight 'unused fields'. 0-5s: sweep past the grey data. 5-11s: arrows pull the values into one compact lane while the grey data remains stored separately; compress the lane with both hands. 11-15s: show real median bars and point at the compact scan. 15-19s: hand moves toward the other fields for the next workload.

### Narration

> These unused fields are slowing the loop. We only add this one number from each object, but those numbers sit far apart in memory. Put them together, and this scan finishes sooner. The other fields still exist. What happens when we need those too? I'll test that next.

### Technical gate

Measure array-of-structs versus separated hot-field storage with a realistic large working set, identical data and safe accumulation. Preserve the cold fields rather than remove the task's data. Inspect generated code and cache or bandwidth evidence before attributing all gains to cache behavior; contiguous layout may also enable SIMD. T5/T6 support possible mechanisms, not this unmeasured result.

Candidate search language: C++ data layout, structure of arrays, cache locality. Platform demand and hashtags unresearched.

## Analyst's critique

1. This has a strong visible target and stays close to our performance audience, but the opening can imply the CPU reads every unused byte. The actual issue is layout and cache-line traffic, not a source-level read of every field.
2. The conversion visual must preserve the cold data. If it disappears, the speedup looks like we removed work or information rather than changed layout.
3. A clean scan may improve for multiple reasons, including vectorization. Show the speed claim first and only name a cause supported by the generated code and counters.
4. The follow-up is a genuine workload tradeoff, which is stronger than a terminology correction. It also signals a broader performance-testing series without asking for a follow.
5. E1 favors the short concrete hook; whether data-layout diagrams retain cold viewers better than source edits is still untested.

## Decision and learning

Strong benchmark-first candidate. Its practical disagreement and clear sequel justify investing in a fair experiment.

P10: Show what stayed the same when demonstrating a win; viewers must see that the edit did not quietly remove required work.

## Benchmark follow-through, September 5, 2026

The user authorized implementation and measurement after selection. The
[benchmark and dated evidence](../../../../aliases/01-screen-short-form/data-layout/RESULTS.md)
now exist in the shorts code workspace. Two normal optimized runs at 4,194,304
players measured score-only speedups of 15.90x and 16.50x; histories were retained.
The scalar control measured 2.75x. Assembly confirms the normal packed-score
loop also gains SIMD, so the whole improvement must not be attributed to cache
misses. Hardware counters were not collected.

The all-field loop lost the large advantage and had no stable winner at the
largest size across the two runs. This supports a real access-pattern tradeoff
for the outro. Timings exclude layout conversion and describe repeated scans
of already-organized data. The original pitch above remains a historical draft;
production and upload checks are still pending.

## ID-lookup follow-through, September 5, 2026

After the user requested a comparison without disabling vectorization, the
[ID-lookup experiment](../../../../aliases/01-screen-short-form/data-layout/LOOKUP-RESULTS.md)
tested the same 25% active subset under ordered, clustered, and shuffled IDs.
Both compiled kernels use scalar integer loads and four scalar accumulators
under normal `-O3`; no vectorization-disabling flags or pragmas were used.

For 1,048,576 active IDs among 4,194,304 players, two runs measured 12.26x/12.54x
ordered, 3.86x/3.83x clustered, and 3.43x/3.62x shuffled speedups. All histories
remain present. SIMD does not explain these gains in this build, but address
generation and memory-system effects are not individually quantified.

This changes the proposed demonstration from a sequential scan to an active-ID
lookup. A future script must show that actual workload and name the measured
size/order. Do not silently put these new timings over the old sequential-scan
code. The earlier measurements and draft remain preserved above.
