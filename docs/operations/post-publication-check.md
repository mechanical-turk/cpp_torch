# Post-Publication Check

Run this automatically whenever the learner reports, or the repository shows,
that new content was published. Do not wait for `engine-check`.

Use the live public post as the authority. Verify, as applicable:

- the public URL opens on the intended account;
- the correct media plays fully with working audio;
- title, caption, hashtags, cover, first frame, crop, and captions render as
  intended;
- comments and intended interaction settings are enabled;
- no accidental privacy, age, copyright, audio, or recommendation restriction
  is visible;
- playlist, related content, explicitly planned first comment, navigation reply, and other planned
  metadata are present; and
- the exact publication time, URL, defects, and corrections are recorded in
  `docs/distribution-timeline.md`.

New long-form videos do not require an end-of-episode answer comment. Its
absence is not a post-publication defect. Do not create one automatically.

For Instagram Reels, inspect both the live Reel and its profile-grid tile. The
live crop overrides every local safe-area assumption. Fix a reversible defect.
If publication made it irreversible, record the observation in the relevant
append-only log and change the next release package rather than rewriting the
historical record.

For new Shorts covered by `short-upload-gate.md`, verify that live playback
preserves the approved first frame, recurring annotations, duration, and
presenter movement. Report a missing pre-upload review or new rendering defect
explicitly; do not backfill a pass from the script or cover image.
