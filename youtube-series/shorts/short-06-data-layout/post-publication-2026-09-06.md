# Short 6: fixed-export post-publication check

Reviewed September 6, 2026, approximately 3:23-3:36 PM Eastern Time.
Scope: the new YouTube and TikTok uploads, plus the default dashboard refresh.
This is not a full audit of every historical release.

## Publications

- [YouTube Short](https://www.youtube.com/shorts/SPWFaXBs8tE): published
  September 6 at **3:15:06 PM ET**, verified through the owned-video API.
- [TikTok](https://www.tiktok.com/@mechaturka/video/7682503962943114526):
  public on `@mechaturka`, verified through the signed-out profile and video
  page. Exact publication time remains unverified; the creator reported this
  afternoon's release, and the page displayed `10m ago` during inspection.
- The original [Instagram Reel](https://www.instagram.com/reel/Dc8ohRhCQK1/)
  remains a separate earlier export. Its API timestamp is September 6,
  **9:23:27 AM ET**. No deletion or replacement was performed.

## YouTube checks and completed actions

| Check | Result |
| --- | --- |
| Intended account and public visibility | PASS: `@mechaturka`, channel `UCAhWaaYB2Qs7kXab0ypp7hA`, public and processed. |
| Uploaded file | PASS: Studio filename and API file size match the fixed local export: `cpp-data-layout-structure-of-arrays-performance.mp4`, 53,662,363 bytes, 2160x3840 at 30 fps. |
| Processing | PASS: Studio explicitly displays `4K complete`; API processing status is `succeeded`. Public-player 2160p menu and visual playback remain unverified. |
| Description | PASS: matches the prepared plain-text description, including benchmark scope and Episode 1 navigation. |
| Title | Preserved the creator's live `This C++ Struct Is a Performance Trap #cpp #coding  #programming`. The appended hashtags differ from the prepared title, but are relevant and do not include the banned `#shorts`. |
| Backend tags | CORRECTED: added the 16 researched tags from the package to the previously empty field. Read-back verified the complete set. Live title and description were preserved. |
| Playlist | PASS: Studio shows `Deep Learning, All the Way Down | Shorts`. |
| Related video | PASS: creator selected Short 4, `Big O Matters So Much Less Than You Think`. Preserved this relevant existing choice instead of replacing it with the package's planned Episode 1. |
| Audience and embedding | PASS: not made for kids; embedding enabled; Science & Technology category. API reports English original audio and metadata language. |
| Comments | PASS: On, Anyone, Basic moderation. Changed default sorting from Top to Newest and saved; Studio displayed Newest with Save disabled afterward. Moderation was not changed. |
| First comment | POSTED at **3:30:52 PM ET**, after a fresh duplicate check found no comments. Subsequent API read-back confirmed it is public. No duplicate was posted after an immediate read-back briefly returned no items. |
| Captions | English ASR track is serving. Downloaded to `captions/en.srt`; text matches the visible demonstration and includes scores, histories, the performance result, why-question, and next test. The generated rolling cues extend beyond the video end; this is not a manually authored timing pass. No chapters added to a fourteen-second Short. |
| Visible restrictions | Studio displayed no notices; API returned no age/content-rating or regional restriction field. This does not prove recommendation eligibility or a complete copyright audit. |

[First comment](https://www.youtube.com/watch?v=SPWFaXBs8tE&lc=UgzcpXEZx-K4LxHxZwF4AaABAg).
A one-time pin reminder was delivered with the link. Do not repeat pin checks.

## TikTok checks and remaining actions

- Public profile links to the correct video; public playback advances and
  reports a fourteen-second duration. This establishes availability, not
  an audio or visual-crop review.
- Caption and all five hashtags match the prepared TikTok package. No external
  URL appears in the caption. Original sound is attributed to `mechaturka`.
- The profile tile reported 48 views at inspection; the video showed zero
  comments and `Log in to comment`. Treat these as timestamped public UI
  observations, not processed analytics or a distribution judgment.
- Chrome is signed out of TikTok. The creator was asked to sign in to
  `@mechaturka` so the prepared first comment, creator-only restrictions, and
  interaction settings can be checked. **No TikTok comment was posted.**
- Phyllo's default refresh returned only three older TikTok content records.
  The newly public upload has not appeared in that feed. Do not turn provider
  indexing delay into a failed-publication claim or invent a dashboard row.
- Profile-grid crop, real player overlays, subjective sound quality, Duet and
  Stitch settings, and recommendation/copyright status remain unverified.

## Fixed-export media review

File: `aliases/04-final-cuts/shorts/ep06/cpp-data-layout-structure-of-arrays-performance.mp4`

SHA-256: `5a4fa9f0e2f26ea9933e4d95aef75c985d9077a49474a7e3468ce29bf2d3f4ab`

2160x3840, 30 fps, H.264 High, Rec.709, AAC stereo at 44.1 kHz.
Exact duration: **14.366667 seconds**. The container identifies as QuickTime
despite the `.mp4` filename; YouTube processed it successfully, so no replacement
is called for on that basis.

Evidence: [first decoded frame](assets/final-review-2026-09-06/first-frame.png)
and [half-second sequential frames](assets/final-review-2026-09-06/contact.jpg).
The contact sheet samples on a different cadence than the exact frame-zero
image; use the latter to judge the opening. Black unused tiles are sheet padding.

| Required upload-gate check | Result and evidence |
| --- | --- |
| All hook elements visible on frame zero | FAIL under the strict existing rule: the code, red markers, face, and `PERFORMANCE TRAP?` callout are present, but the spoken `THIS PATTERN` caption is absent from the exact first frame. The hook is nevertheless visibly identifiable. Record the missed gate; do not automatically delete a public post. |
| Recurring annotations | PASS: opening circle/arrow through roughly 1.5 s, lookup arrow around 2-3 s, score arrows around 3.5-4 s, history arrow around 7-8 s, result circle around 9.5-10 s. |
| Under 20 seconds | PASS: 14.366667 s, including the tail. |
| Recurring presenter movement | PASS in sequential-frame review: pointing around 0-1.5 s, hands together around 2-3 s, spreading/packing around 3.5-6.5 s, history/result gestures around 7-10 s, and head/hand movement during the ending. |

Local code and captions remain within the exported frame. The narrower code
composition appears in the corrected export, but local frames cannot establish
the actual TikTok or Shorts interface safe zone.

Audio decodes and is non-silent. Measured mean is -10.5 dBFS and sample peak is
0.0 dBFS. The peak warrants listening for clipping; it does not by itself prove
audible distortion. Full subjective listening and A/V synchronization remain
unverified. CapCut +5 dB and Enhance voice intensity 75% have not been confirmed
for this export and cannot be inferred from its audio measurements.

Overall: published, with partial post-publication verification. **Do not mark
the full media gate passed or backfill pre-upload approval.**

## Follow-up

1. Finish TikTok author-comment and creator-setting checks after sign-in.
2. Inspect both live crops and listen to complete playback. Chrome's extension
   returned `Debugger unattached`; native accessibility controls worked, but
   screenshot capture failed with ScreenCaptureKit error -3811. No visual or
   listening pass is claimed from an accessibility tree.
3. Capture matched-age 24-hour, 72-hour, and seven-day results, starting from
   each actual publication time. These are recorded follow-ups, not scheduled
   background jobs. Recheck TikTok's provider feed on the next default refresh.
4. The native X release is outside this two-platform request and remains
   unconfirmed. No tweet-level analytics or new X post was requested/performed.
