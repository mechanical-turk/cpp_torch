# 07: This copy changes the original

Proposed MP4: `cpp-vector-bool-auto-proxy-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P06: choose an observable value change with no hidden timing boundary. Reduce the scene from machine behavior to one small C++ object.

### Script gate

Claim: auto stores vector<bool>'s element proxy here, so assigning it changes the represented bit. Belief: auto value declarations always detach a value. Expected objection: 'That is a proxy, not a bool copy; avoid vector<bool>.' Omit: proxy taxonomy and ranges internals. Keep visible: vector<bool>, auto, and the bool replacement.

### First frame and edit

Frame one: flags[0] is false, with 'auto bit = flags[0];' and 'bit = true;' beneath it. Callout: 'Copied or connected?' Circle bit and emphasize 'original' in the opening caption. 0-5s: separate hands for supposed copy and original. 5-11s: draw a red connection from bit to flags[0], bringing hands together. 11-15s: reveal true, replace auto with bool and rerun to show the original stays false. 15-19s: point to the packed-bit strip for the tradeoff question.

### Narration

> This copy changes the original. Take a bit from vector bool with auto, then change it. The original bit changes too. Auto kept a little handle to that bit. Use bool, and you get a separate value. Is packing the bits worth this behavior? I'll benchmark that tradeoff next.

### Technical gate

Check T7, vector<bool>::reference and assignment. Keep the vector alive and unchanged in capacity; no dangling proxy or undefined behavior is needed. Compile both forms and record false/true outputs. The first line's word 'copy' refers to copying the proxy object, not copying a standalone bool; the demonstration must promptly clarify that distinction.

Candidate search language: C++ vector bool, auto proxy reference, packed bits. Platform demand and hashtags unresearched.

## Analyst's critique

1. The word 'copy' deliberately invites an objection about the copied proxy. The explanation is correct, but this remains close to round 1's terminology-based controversy.
2. The first-frame callout asks a meaningful question, yet viewers unfamiliar with vector<bool> may interpret it as ordinary reference syntax. Keep the container type legible without a long template declaration.
3. The second bool run is needed to provide practical value, but it adds a reset and replay. The edit must make the reset explicit or the before/after state becomes ambiguous.
4. Packed-bit performance is a genuine tradeoff, but this Short proves only reference behavior. It cannot imply packed storage is slower or unsafe in all uses.
5. E3's coordinated annotation could help the hidden connection read clearly; we have no retention evidence for proxy explanations.

## Decision and learning

Keep as a language-behavior candidate. Do not prioritize solely because 'avoid vector<bool>' is likely to attract comments.

P07: Prefer disagreement about consequences and choices over arguments created mainly by an ambiguous noun.

