# Episode 13 script review

## Source and scope

Start from recorded code `c9918e8`. Current main `516f66e` has identical C++
source; its intervening changes are documentation/editor configuration.
Review destination: refactor branch `b4d85fe`.
Do not switch, overwrite, or merge the creator's recording checkout.

The existing Episode 12 written ending mentions saving/loading weights.
The creator has since selected a cleanup episode instead. Treat serialization
as deferred, not delivered here; final recorded outro has not been inspected.

Research: [keyword-research.md](keyword-research.md).
Recording script: [script.md](script.md).
Scope direction: [production-notes.md](production-notes.md).

## Checklist plan before drafting

| Check | Planned treatment |
| --- | --- |
| L01 | Complete result construction, reusable library, independent unit tests. |
| L02 | Open on actual result-creation code, not a series greeting or folder tour. |
| L03 | Introduce Parent in the opening coding beat, before 30 seconds as a rehearsal target. |
| L04 | Pair the two broadcast mappings with their inputs immediately; show that concrete structural payoff before one minute. |
| L05 | Separate parent representation, node construction, file relocation, build, and testing milestones. |
| L06 | Show the awkward call site before defining the constructor that fixes it. |
| L07 | Explain leaf defaults, ownership, broadcast edge mapping, and library/test separation where used. |
| L08 | Replay literal edits from the recorded checkpoint; no unrequested changes to numerical rules. |
| L09 | Preserve baseline tests; verify broadcast gradients and actual examples separately from long training waits on camera. |
| L10 | One active edit at a time; collapse exact mechanical move panels until needed. |
| L11 | Short connected narration, existing bodies moved rather than retyped; flag runtime after word count. |
| L12 | Finish with a working library and named tests; leave further architecture work for later. |
| L13 | Itemized recap, next-step display, standard sign-off, clean five-second tail. |
| L14 | Only recording content in script.md; rationale and checks stay here. |
| L15 | Complete keyword research before prose; use CMake and GoogleTest at their coding need. |
| L16 | Apply long-form opening evidence, not Shorts controversy or pacing. Report unmeasured rehearsal risk. |

## Evidence used

[Episodes 1-6 long-form retention](../analytics/reports/2026-08-29-long-form-retention-comparison-episodes-01-06.md)
shows steep opening losses and navigation toward concrete implementation.
Response: begin with one real code problem and an immediate edit; no history
recap or advance tour of the entire refactor. This is an editorial hypothesis,
not evidence that a constructor refactor will improve retention.

The recent creator feedback supplies the stronger local constraint: explain
why an edit is needed before typing it, and connect the next step to the
previous one. File moves follow logical migrations, not the reverse.

## Final audit

| Check | Status | Points | Evidence or remaining risk |
| --- | --- | --- | --- |
| L01 | PASS | 10 | A names graph assembly; B completes initialization; C-E produce the library and separate tests. Serialization remains deferred. |
| L02 | PASS | 10 | Opening shows the current result builder; no greeting, recap, or directory tour. |
| L03 | PASS | 8 | 48-word opening leads directly to Parent; roughly 20 seconds at 145 wpm before the first edit. This is an estimate, not measured retention. |
| L04 | PARTIAL | 4 | Parent and its first populated broadcast entries are the early structural payoff. The first-minute timing depends on editing speed and needs rehearsal. |
| L05 | PASS | 8 | Parent mapping, complete node construction, library separation, named tests, and build presets each resolve the preceding limitation. |
| L06 | PASS | 8 | Result builder precedes constructor design; sum is the first complete-result example; CMake arrives after the multi-file need. |
| L07 | PASS | 8 | Explains per-input mappings, leaf defaults, member initialization order, private ownership boundary, and independent tests. |
| L08 | PASS | 10 | All 58 literal edits replay against c9918e8; all final implementation/build/test files match b4d85fe. Current main has identical baseline C++ source. |
| L09 | PASS | 6 | Logical migration reproduces full baseline stdout; final tests pass in three build modes; all examples run, with MNIST output matching baseline. |
| L10 | PASS | 5 | Active code locations and individual highlights specified; large exact moves folded. Rendered editor fit remains a recording check. |
| L11 | PARTIAL | 2.5 | 1,182 spoken words plus mechanical edits. Budget approximately 12-16 minutes; rehearse file moves and reduce scope if it exceeds 15. |
| L12 | PASS | 4 | Tests and XOR demonstrate the split library; MNIST confirms preserved behavior. Further composition/dispatch/serialization remain future work. |
| L13 | PASS | 4 | Itemized recap and next steps, exact sign-off, five-second clean tail; no Q&A. |
| L14 | PASS | 2 | Filename, code, recording cues and > narration only in script; this review stays separate. |
| L15 | PASS | 2 | Research predates drafting. C++ deep learning, Tensor, library, CMake, GoogleTest and tests occur at their code need. |
| L16 | PASS | 2 | Long-form source evidence cited; scope, timing estimates, and unverified rehearsal/visual execution are explicit. |

## Critique and repairs

1. The initial opening spent too many words describing the coming cleanup.
   Shortened it and introduced Parent immediately after the concrete broadcast
   mapping need. The first structural payoff is not presented as a successful
   run; the multi-edit migration is explicitly unfinished until A ends.
2. Removed a standalone illustrative sum test that was not part of the actual
   migration. The visible example now comes from TensorTest.Sum, and the
   narration explains the fixture instead of assuming TEST_F is familiar.
3. Kept every original method and moved test visible in exact-code panels,
   without forcing thousands of mechanically repeated lines into the spoken
   track. C1 demonstrates the signature split before supplying complete
   destinations. The presenter must perform these moves, not pretend they
   happened off camera. No math implementation is supplied secretly.
4. Node constructor, leaf Tensor construction, and operation result creation
   are separate stages. Empty/non-null node reasoning stays at the private
   constructor. No long list of graph fields appears in the public API.

Remaining weakness: the full cleanup is near the runtime ceiling. Roughly
eight minutes of speech at 145 wpm leaves four to seven minutes for edits and
holds that do not overlap narration. The longest risk is C1-C4, not the math.
Use editor cut/paste for existing bodies; do not retype or reread them. If a
dry run exceeds 15 minutes, split after B and defer C-E to a separate episode
with creator approval. Do not silently cut causal explanations to fit.

Score: 93.5/100. Decision: rework timing in rehearsal; technical verification passes.

## Verification and provenance

Run `python3 youtube-series/chapter-13/verify-script.py` from Content HQ.
The verifier checks literal panels against the migration manifest, applies
every edit in a temporary directory, compiles three intermediate milestones,
and compares the logical migration's output with the recorded baseline.
It then builds the final split project in Debug, Release and sanitizer modes,
runs all 41 tests, runs every Release example, and compares final files against
the reviewed branch. It verifies that the live recording source is unchanged.

The existing local GoogleTest source cache avoids redundant network downloads
during this verification only; the recording CMake file uses the pinned
FetchContent URL. MNIST files are read from the existing recording checkout's
data directory. Neither the dataset nor local caches are committed.

Literal Before panels preserve whitespace from the recorded source so edits
can replay exactly. Trailing spaces within those copied code panels are
intentional; they are not a formatting change to the implementation.

See [verification-run.json](verification-run.json) for outputs, hashes, and
the temporary replay location. No measured speaking rehearsal, thumbnail,
final-media review, new analytics, public post, push or merge is claimed.
