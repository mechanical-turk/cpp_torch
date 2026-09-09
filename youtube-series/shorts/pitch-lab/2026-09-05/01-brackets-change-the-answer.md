# 01: These brackets change the answer

Proposed MP4: `cpp-floating-point-addition-order-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Start with a named, visible change rather than the vague phrase 'this optimization'. This directly addresses the preceding rejected pitch.

### Script gate

Claim: changing the grouping of these three double additions changes the computed result. Belief: regrouping addition is harmless. Expected objection: 'Floating point is not associative; this is expected.' Omit: bit layouts, rounding-mode taxonomy, compensated summation. Keep visible: double, the exact inputs, and the two groupings.

### First frame and edit

Frame one: two short expressions with identical inputs and different brackets; one result is 1, the other is ?. Callout: 'Same sum?' Circle the changed brackets, with matching highlighted hook captions. 0-4s: sweep a hand across the shared inputs. 4-11s: move the circle to the large-plus-small addition; use pinched fingers for the lost unit. 11-15s: reveal 0 and point to both results. 15-19s: the next-test question over the unchanged proof. No output is concealed after its explanation has already made it obvious.

### Narration

> These brackets change the answer. Add a huge number to its negative, then add one. You get one. Move the brackets, and the one gets rounded away before the large numbers cancel. Now you get zero. Can we recover that missing one? I'll test a different summation method next.

### Technical gate

Use a=1e16, b=-1e16, c=1.0 with binary64 double, default rounding and no fast-math: (a+b)+c gives 1; a+(b+c) gives 0. Mechanism: T1 in evidence.md. Compile the exact camera example before selection. No speed claim. This round does not claim a compiled demo exists.

Candidate search language: C++ floating point, addition order, rounding error. Platform demand and hashtags unresearched.

## Analyst's critique

1. E1 supports shortening the opening, but does not establish that a floating-point puzzle interests the performance audience. This changes the subject from speed to numerical accuracy.
2. The contrast is visible, yet scientific notation creates a reading tax. Simplifying the narration does not remove the need to understand the input magnitudes.
3. Many experienced viewers know the result. The anticipated correction concerns terminology more than a contested engineering decision, so discussion may be shallow.
4. The first example and second example still require tracking two evaluation histories. A 19-second read can fit while the explanation remains cognitively dense.
5. The continuation is concrete but introduces summation methods without a practical workload. Viewers may enjoy the puzzle without expecting a useful series.

## Decision and learning

Keep as an accuracy follow-up, not the leading next-short candidate. Test a phone-size opening before developing it further.

P01: Name the visible change and its consequence in the hook; do not make viewers decode an unnamed optimization.

