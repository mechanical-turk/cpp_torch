# 18: This billion-iteration loop never runs

Proposed MP4: `cpp-benchmark-dead-code-elimination-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P17: choose an inexpensive assembly-verification experiment instead of a hardware-sensitive speed contest. Frame it as a benchmark audit from the opening.

### Script gate

Claim: the tested optimized build removes this loop because its result has no observable use. Belief: source-level iterations must appear in a benchmark's executed work. Expected objection: 'Use the result; the compiler is doing its job.' Omit: every as-if-rule exception and all barrier APIs. Keep visible: 'Benchmark audit', unused result and actual generated function.

### First frame and edit

Frame one: a simple unsigned sum loop with a billion bound and callout 'Did this even run?' Circle the unused result; emphasize 'never runs'. 0-5s: gesture from the loop toward an empty output slot. 5-11s: replace code with the actual short generated function and circle the absence of a loop, using a sweeping-away gesture. 11-15s: show a corrected observable-result build and whether work remains, with its own actual assembly excerpt. 15-19s: point to a benchmark barrier for the next question.

### Narration

> This billion-iteration loop never runs. We calculate a sum, then never use it. The optimized function has no loop at all. Make the result observable, and check the generated code again. A fast timing doesn't prove the work happened. Which benchmark barriers actually preserve it? I'll test those next.

### Technical gate

T15 plus compiler assembly. Use defined unsigned arithmetic and inspect normal optimized output; do not claim a timing of literally zero. An observable result can still be constant-folded or computed by a closed form, so the corrected demonstration must use runtime inputs and assembly verification. Do not claim DoNotOptimize guarantees the original source operations execute.

Candidate search language: C++ benchmark dead code elimination, compiler optimization, DoNotOptimize. Platform demand and hashtags unresearched.

## Analyst's critique

1. The billion-iteration framing is attention-grabbing but risks overstating work that exists only in source. The 'Benchmark audit' context must be visible before the revelation.
2. The compiler deletion is a real lesson, but an intentionally unused result can look like the obvious mistake we rejected in round 5. The audit framing needs to be candid, not feigned astonishment.
3. The corrected example is underspecified in the narration. Merely printing a sum can still leave a closed-form or folded computation; generated code must decide whether the promised work remains.
4. Assembly is proof for experts but another language for beginners. Circle the relevant absence and use a tiny trace; do not expect viewers to read an entire disassembly.
5. E2 predicts recognizable compiler objections, yet this pitch could produce 'bad benchmark' replies without substantive tradeoff discussion. Its educational utility is stronger than its controversy.

## Decision and learning

Keep as a benchmark-literacy episode. Validate the repaired example before treating the script as complete.

P18: A fix must actually repair the demonstrated problem; a familiar recommendation is not proof that the repaired code does the intended work.

