# YouTube Studio Short-funnel checkpoint: August 23, 2026

## Studio-only observations

For the last 28 days, YouTube Studio reports:

- 2,914 channel views, 19.7 hours of watch time, and +17 subscribers.
- Shorts: 2.4K views, 1.1K engaged views, 26 likes, and +1 subscriber.
- Shorts traffic is primarily discovery traffic: 87.9% comes from the Shorts
  feed.
- Across Shorts, 45.8% of viewers stayed to watch and 54.2% swiped away.

The strongest recent Shorts are the concrete-failure experiments:

| Short | Views | Average viewed | Other signal |
|---|---:|---:|---|
| Overflow check | 1.4K | 80.0% | 15 likes |
| Unsigned loop | 954 | 71.1% | 19 seconds average view duration |
| Tensor shape | 99 | 58.0% | materially smaller initial test |

The detailed per-Short Studio reports add the following funnel numbers:

| Short | Engaged views | Stayed | Swiped | Avg duration | Subscribers |
|---|---:|---:|---:|---:|---:|
| Tensor shape | 51 | 55.0% | 45.0% | 0:16 | 0 |
| Unsigned loop | 474 | 53.5% | 46.5% | 0:19 | 1 |
| Overflow check | 553 | 40.6% | 59.4% | 0:19 | 0 |

The first two Shorts converted roughly half of feed exposures into engaged
views. The overflow Short had the strongest average percentage viewed among
those who stayed, but the weakest initial stay rate and no subscriber
conversion.

## Long-form Studio context

Studio's current 28-day content table reports:

| Video | Views | Average duration | Average viewed |
|---|---:|---:|---:|
| Episode 1 | 231 | 1:35 | 4.3% |
| Episode 2 | 94 | 1:06 | 3.9% |
| Episode 3 | 68 | 0:45 | 2.2% |
| Episode 4 | 43 | 1:11 | 8.9% |
| Episode 5 | 40 | 1:36 | 5.9% |

Episode 1's detailed retention report says 27% of viewers remain around the
0:30 mark. Episode 2 reports 1:06 average view duration and 3.9% average
percentage viewed. The later episodes have too little volume for a reliable
retention-shape comparison, but Episode 4 currently has the best average
percentage viewed of the recent long-form uploads.

## Durable lessons

1. Discovery and consumption are separate measurements. A Short can receive a
   strong average percentage viewed among engaged viewers while still losing
   more than half of its initial feed impressions to swipes.
2. The current bottleneck is not only how long engaged viewers watch. The first
   frame and first spoken sentence must persuade a cold viewer not to swipe.
3. A high average percentage viewed is therefore not enough to predict continued
   distribution. We must also watch stayed-to-watch rate, engaged views,
   interactions per view, rewatches when available, and subscriber conversion.
4. The failure-led format remains the best current hypothesis, but it needs
   repeated tests. Repeat the structure for the next two or three Shorts while
   changing one meaningful variable at a time, especially the opening frame or
   first sentence.
5. Do not interpret a two-hour slowdown as permanent rejection. Shorts are
   commonly tested in an initial audience batch, and a later retest is possible.
   Record the slowdown as an initial-distribution result rather than claiming
   that the video is permanently out of circulation.

## Interpretation of the overflow Short

The per-video Studio report is more precise than the channel summary. For the
overflow Short, Studio reports:

- 1,416 views;
- 553 engaged views;
- 0:19 average view duration on a 0:24 Short;
- 3.3 hours of watch time;
- 40.6% stayed to watch and 59.4% swiped away;
- 90.5% Shorts-feed traffic;
- 2.0% YouTube-search traffic, led by `overflow` and `c++`;
- 15 likes and no subscriber change; and
- 98.8% of watch time from viewers who were not subscribed.

The channel-level 45.8% stayed-to-watch figure is an aggregate across Shorts
and should not be substituted for the overflow Short's 40.6%. The reported
80.0% average percentage viewed is conditional evidence about viewers who
stayed long enough to become engaged. It does not mean that 80% of everyone
shown the Short watched it. The likely failure point is the initial decision
to watch, not the middle or ending for viewers who stayed.

The available data cannot identify the exact cause of the distribution slowdown.
Possible contributors include the opening frame, topic-audience match,
interaction rate, rewatch behavior, satisfaction signals, and competition in
the feed at that moment. The evidence supports improving and testing the hook,
not a single causal explanation.

## Studio extraction plan

The Data API already supplies basic views, likes, comments, and subscriber
counts. Studio adds the following high-value fields that should be collected by
the local browser-based analytics workflow:

- per-video engaged views and average view duration;
- per-video stayed-to-watch and swiped-away percentages;
- traffic-source breakdown, including Shorts feed and search terms;
- watch time from subscribed versus non-subscribed viewers;
- device type;
- end-screen click rate and remix activity; and
- audience-retention curves once a video has enough data.

The collector should save these by video ID and timestamp, keeping channel-level
aggregates separate from per-video values. It should also record when Studio
says that a report has insufficient data rather than converting that state to
zero.

## Next experiment

For Shorts 4 through 6:

- keep the runtime near 20 to 30 seconds;
- show the concrete failure immediately;
- make the first frame understandable without audio;
- preserve the failure-led structure;
- change one opening variable per Short; and
- compare stayed-to-watch rate before average percentage viewed.

Reassess after three more Shorts and at the 24-hour and 72-hour checkpoints.
