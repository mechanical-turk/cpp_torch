# 04: This move adds work

Proposed MP4: `cpp-return-std-move-copy-elision-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P03: prefer an observable operation count over an unexplained timing. P01 keeps the changed token visible from the first frame.

### Script gate

Claim: explicit move in this local-return example causes a move where the tested plain return elides it. Belief: writing move avoids extra work. Expected objection: 'NRVO is optional; the warning already tells you this.' Omit: every value category, all implicit-move rules. Keep visible: return of the same named local and an instrumented move constructor.

### First frame and edit

Frame one: 'return move(result);' with move circled and callout 'Extra work?' The plain-return move count is 0; the other count waits for execution. 0-5s: point at move. 5-10s: delete the call with a hand swipe while an arrow follows the returned object straight to its destination. 10-15s: show the two observed move counts, then point between them. 15-19s: a small const label enters for the next question. Caption emphasis follows 'move' and 'work'.

### Narration

> This move adds work. Return this local object normally, and the compiler builds it straight into the destination. Add move, and now our move constructor runs. Remove it, and that extra move disappears. What if the original object is const? I'll test that next.

### Technical gate

T2. Run an instrumented class with and without return std::move(local), under C++23 and normal optimization. Do not disable copy elision to manufacture the contrast. Check the warning and actual constructor trace; NRVO is optional. Constructor counts establish semantic work for this example, not a meaningful wall-time penalty for every type.

Candidate search language: C++ return std::move, copy elision, NRVO. Platform demand and hashtags unresearched.

## Analyst's critique

1. The token is recognizable to C++ viewers, but 'adds work' gives little sense of the consequence. The counter must make that consequence concrete immediately.
2. The apparent contradiction is strong, yet a trivial move can be nearly free. Counting a move must not become an unsupported claim that the application is slower.
3. 'Builds straight into the destination' compresses object lifetime into one sentence. A single object animation is essential; a second source window would overload the scene.
4. The expected NRVO correction could become a vocabulary dispute unless the visible trace makes this explicitly a tested local-return case.
5. The const follow-up is adjacent, but it is a second language rule rather than a continuation of the same return experiment. Returning-viewer intent remains a hypothesis, not an E2 result.

## Decision and learning

Shortlist for a compact, testable C++ contradiction. Keep the headline about extra work, not a fabricated speedup.

P04: A counted operation is not a measured slowdown; choose the headline that the actual evidence can support.

