# 20: The compiler split this loop for me

Proposed MP4: `cpp-compiler-auto-vectorization-sum-reduction-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P19: make generated code the actual subject and evidence. This is a different experiment from Short 5's manual accumulator comparison: one unchanged source loop, inspected under the normal optimizing compiler.

### Script gate

Claim: this verified compiler build transforms a one-accumulator integer sum into multiple partial sums before combining them. Belief: the source's single sum necessarily describes one executed chain, or the compiler cannot perform the manual transformation. Expected objection: 'It does not always vectorize; floating point and aliasing change the answer.' Omit: all optimization blockers and intrinsic syntax. Keep visible: unsigned integer input, actual flags and annotated generated code.

### First frame and edit

Frame one: one source sum feeding several empty execution lanes, callout 'I wrote one sum'. Circle the source variable; emphasize 'compiler' and 'split'. 0-5s: hold up one finger. 5-11s: show the actual compiler output with only the accumulator lines highlighted; spread fingers as lanes fill. 11-15s: arrows merge the partial sums into the verified result. 15-19s: point back to the source element type for the next test. Assembly is evidence behind the lane drawing, not a screenful to read.

### Narration

> The compiler split this loop for me. I wrote one sum. In this optimized build, the generated code keeps several partial sums, then combines them. I didn't add those variables. The compiler did. Will it do the same with floating-point numbers? I'll change the type and check next.

### Technical gate

T6. Compile the actual integer reduction with the normal optimized toolchain and inspect vectorization remarks plus assembly. Distinguish independent accumulator registers from lanes inside one SIMD register; illustrate only what the output shows. Verify equal results across empty, odd and large input sizes. Do not promise an unmeasured speedup. If the compiler does not perform this transformation, this script fails its premise.

Candidate search language: C++ auto vectorization, compiler optimization, sum reduction. Platform demand and hashtags unresearched.

## Analyst's critique

1. This directly answers a documented Short 5 objection, but existing commenters already believe the result. Relevance to a thread does not guarantee surprise for cold viewers.
2. The first frame can look too similar to the accumulator Short. Make compiler-generated work, rather than manually adding variables, visibly central.
3. The script risks implying several scalar variables where the compiler uses SIMD lanes. That would undermine the exact expertise this audience is likely to test.
4. The floating-point follow-up is technically adjacent and worth discussing, but the current short must finish its generated-code proof before changing the type.
5. E2 makes this an evidence-informed topic candidate, not an audience-tested hook. E1 still requires a phone-size check: an assembly-heavy opening could lose viewers before the benefit becomes clear.

## Decision and learning

High-priority verification candidate because it addresses an actual audience question. Compare its opening against round 10 before choosing; do not treat comment volume as a demand forecast.

P20: Use real audience objections to choose experiments, but test whether the opening also matters to someone outside that existing thread.

