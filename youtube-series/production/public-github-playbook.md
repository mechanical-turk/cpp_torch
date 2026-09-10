# Public GitHub Playbook

The public source repository is a primary distribution channel. Read this
before an engine check, long-form release, or public README change.

Repository:
`/Users/keremkazan/Documents/Projects/deep-learning-all-the-way-down`

Workspace alias: `aliases/02-screen-long-form`

## Release requirements

- Every public episode has a checkpoint commit on `main` matching the code
  reached in the recording.
- Git history is the authoritative code timeline. Do not replace it with the
  cleaner state imagined by a script.
- For a routine episode README update, change only the episode table and add
  the new episode summary. Include its actual source checkpoint hash and video
  link, then retain a row for the next episode marked `*(Work in progress)*`.
- Match the new summary to the existing summaries in length, paragraph count,
  and link format. Do not expand it into a separate feature or status guide.
- Preserve existing titles, headings, subheadings, wording, ordering, and
  unrelated sections. Do not use an episode update as a general README rewrite.
  Broader changes require a separate user request.
- Do not claim future work, a production framework, a PyTorch replacement, or
  completed GPU support.
- Compile and run every public entry point after release-facing code or README
  changes.
- Confirm `HEAD` is pushed to `origin/main`, generated binaries are ignored, and
  the tree contains no accidental binaries or secrets.
- When the user requests a repository-layout or build change, update only the
  README sections directly affected by that change.
- Apply `platform-copy-playbook.md` to README and repository social copy. Use
  accurate C++, machine learning, deep learning, and systems terms naturally.

Record the checkpoint commit and meaningful README synchronization in
`docs/distribution-timeline.md`. A stale README or source checkpoint is a
release defect and should be corrected during engine check.
