# Social Analytics and Profile Branding

Status: active branch, opened 2026-08-16.

## Objective

Create one durable analytics pipeline for YouTube, X, and LinkedIn, then apply a
cohesive personal brand across all three profiles without making them look like
corporate copies of one another.

## Analytics access

### YouTube

Complete. The local collector can retrieve series-only channel and video data.

### X

Use X API v2 with authenticated user context so the collector can retrieve both
public engagement and private metrics for owned posts. X currently charges per
API use through prepaid credits. Private and organic post metrics are available
only for posts created within the previous 30 days, so snapshots must run
regularly rather than being reconstructed months later.

Authorization is complete for `@mechaturka` using read-only OAuth 2.0 PKCE.
The local collector stores renewable tokens outside the repository and supports
series-era owned-post snapshots. The first bounded sync completed on August 16
and retrieved seven posts. It included public impressions and engagement plus
owned-post engagements, link clicks, and profile clicks.

The permanent X collection boundary is **2026-08-13 at 9:10 AM Eastern Time**
(`2026-08-13T13:10:00Z`). Never move it backward or retrieve the account's full
history without explicit creator approval. This protects both privacy and API
credits.

Next gate: inspect the Developer Console's actual charge for the bounded sync,
then choose a cost-conscious snapshot frequency. Do not enable automatic
collection before that review.

### LinkedIn

Personal-post analytics require LinkedIn's vetted Community Management API and
the `r_member_postAnalytics` permission. The development-tier application
requires a verified organization, business email, website/domain, and associated
LinkedIn Page. Approval may take time and is not guaranteed.

Next gate: determine whether the creator already has the required organization,
domain email, website, and LinkedIn Page. If so, create a new LinkedIn developer
application and apply for Community Management Development Tier access. If not,
do not create placeholder business infrastructure merely to unlock analytics;
use periodic manual exports until the series has enough scale to justify it.

## Brand system

Define the system once before editing any profile:

- public identity: Kerem Kazan / `@mechaturka`;
- project: *Deep Learning, All the Way Down*;
- positioning: deep learning from first principles through modern C++, systems,
  performance, and eventually GPU programming;
- voice: technically rigorous, curious, direct, and personal;
- visual language: restrained navy technical grid, white type, blue tensor
  structures, and limited orange accents;
- primary destination: the complete YouTube playlist;
- source destination: the GitHub repository.

## Profile responsibilities

### X

Concise personal bio, one primary series link, recognizable banner, and a pinned
navigation post. Preserve room for technical and personal posts; the account
must not read like an automated episode feed.

### LinkedIn

Professional headline and About section that connect existing experience to the
public learning project. Use the Featured section for the playlist, repository,
and strongest episode. Keep the banner visually related to X and YouTube while
using LinkedIn's wider professional context.

### YouTube

Channel description, banner, profile identity, homepage sections, main course
playlist, Shorts playlist, and featured video. The Data API can update channel
description and keywords and can upload/set a banner after final approval.

## Sequence

1. Capture the current state of all three profiles.
2. Approve one positioning statement, bio vocabulary, link hierarchy, and
   visual system.
3. Produce platform-specific copy and banner crops from that system.
4. Preview every profile before applying changes.
5. Apply approved changes, using APIs where supported and Studio/UI only where
   no API exists.
6. Record the completed profile refresh in the distribution timeline.
