# 08: This lookup keeps growing the map

Proposed MP4: `cpp-unordered-map-lookup-inserts-entries-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P07: make the disputed consequence an actual state change, not the definition of copy. The code is valid; the surprise is an API's insertion behavior.

### Script gate

Claim: operator[] inserts an entry when each queried key is absent. Belief: looking up a value cannot change a container. Expected objection: 'Use find or at; this API is designed to insert.' Omit: bucket internals and hash complexity. Keep visible: distinct missing names, the map's size, and operator[].

### First frame and edit

Frame one: 'score = scores[name];' beside an initially empty map and a stack of incoming names. Callout: 'A lookup that writes?' Circle the brackets; emphasize 'growing' in captions. 0-5s: point to each new name. 5-11s: arrows move new zero-valued entries into the map while a size counter grows. 11-15s: highlight the insertion and replace the lookup with find, showing no new entry. 15-19s: gesture toward an existing entry for the next test. No real accounts or personal data.

### Narration

> This lookup keeps growing the map. Ask for a name that isn't there, and these brackets insert it with a zero score. Ask for another missing name, and another entry appears. Find lets us check without inserting. Which lookup would you use in a hot loop? I'll benchmark them next.

### Technical gate

T8. Verify unordered_map<string,int> size before and after operator[] for distinct missing keys. Show that repeated lookup of the same inserted key does not keep growing it. Compare find with operator[] only under equivalent specified hit/miss semantics in any future benchmark; at throws on a miss and needs a different contract.

Candidate search language: C++ unordered_map operator brackets, map lookup insertion, find versus at. Platform demand and hashtags unresearched.

## Analyst's critique

1. The state change is clear, but experienced viewers may see only a basic API lesson. An expected correction is not automatically a compelling controversy.
2. The growing counter can imply a leak. These entries remain owned by the map, so language about lost memory would be inaccurate.
3. Displaying several names, values, size, code, captions and annotations would crowd the opening. One pending name and one counter are enough.
4. The proposed lookup benchmark has a semantic trap: insertion and non-insertion do different jobs. The outro needs an explicit shared workload before implementation.
5. E1/E3 support the compact state-change treatment; E2 does not establish demand for container API lessons. The value is practical surprise rather than a proven follow-conversion mechanism.

## Decision and learning

Keep as a simple correctness Short; weaker than a genuine performance tradeoff for the immediate follow-up.

P08: Keep the next experiment inside a shared task contract; comparing APIs that do different jobs can create a false contest.

