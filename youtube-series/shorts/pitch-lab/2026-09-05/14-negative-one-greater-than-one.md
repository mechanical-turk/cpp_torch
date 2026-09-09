# 14: Negative one is greater than one here

Proposed MP4: `cpp-signed-unsigned-comparison-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P13: move away from shared-reference behavior to a numerical comparison. P12 demands a visual explanation rather than a catalogue of conversion rules.

### Script gate

Claim: -1 > 1u evaluates true under the usual arithmetic conversions. Belief: comparisons preserve the ordinary mathematical order of these literal values. Expected objection: 'The u changes the type; warnings catch it.' Omit: every integer rank and type combination. Keep visible: the unsigned suffix and the conversion arrow before the payoff.

### First frame and edit

Frame one: '-1 > 1u' with a ? result and a red circle around u. Callout: 'Which number wins?' Emphasize 'negative one' and 'greater'. 0-5s: point below zero on a tiny number line. 5-11s: arrow moves -1 to the maximum unsigned value after conversion; sweep hand to the other end. 11-15s: reveal true with the converted operands still present. 15-19s: point to a size() comparison for the next test. The numerical maximum uses the actual unsigned width.

### Narration

> Negative one is greater than one here. That little u makes this comparison unsigned. Negative one converts to the largest unsigned int before the comparison happens. Now the result is true. Could a container's size trigger the same problem? I'll test that comparison next.

### Technical gate

T13. Compile -1 > 1u with warnings enabled and record the result; display the actual unsigned-int maximum rather than hard-code a universal width. For the follow-up, test the actual size_t rank and signed operand type. Do not generalize this result to all mixed signed/unsigned comparisons or call it signed overflow.

Candidate search language: C++ signed unsigned comparison, integer conversion, size_t comparison. Platform demand and hashtags unresearched.

## Analyst's critique

1. The numerical contradiction is immediate, but it is a familiar C++ puzzle. More surprise for beginners may mean less relevance to the systems audience we want to retain.
2. The hook spends eight words stating the result. The first-frame expression helps, but the obscure u suffix still imposes a recognition cost.
3. The explanation resolves the question before the true result is revealed. Holding that result until second 11 is theatrical delay rather than useful suspense.
4. The size() continuation is practical, but many viewers can answer it immediately after hearing the rule. It is not a strong unresolved engineering question.
5. E1 tells us to reduce opening friction, not to replace performance content with broadly accessible trivia. This pitch might gain views without strengthening the intended audience identity.

## Decision and learning

Do not select next. Keep as an occasional practical bug lesson only if attached to a real size comparison rather than a standalone arithmetic riddle.

P14: Do not delay a result the explanation has already made obvious; preserve uncertainty that is still worth resolving.

