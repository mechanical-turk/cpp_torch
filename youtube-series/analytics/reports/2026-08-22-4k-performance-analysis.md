# 4K Publishing and Channel Performance

## Conclusion

Use 4K as a quality standard, not as a growth hack.

YouTube says 4K improves the viewing experience on larger screens and that 4K
uploads consistently achieve higher watch time on TVs. That makes 4K relevant
to this series because small C++ identifiers, tensor shapes, and mathematical
notation benefit from additional detail.

YouTube's public recommendation documentation does not identify upload
resolution as a direct ranking signal. It emphasizes what viewers choose,
watch time, likes and dislikes, feedback, and satisfaction. Therefore any
distribution benefit from 4K should be understood as indirect: clearer content
may improve watch behavior for viewers and devices that benefit from it.

## Expected effects

### Most plausible benefits

- Sharper code, terminal text, formulas, and diagrams.
- Better viewing on desktop monitors and TVs.
- More room for cropping or reframing while retaining a sharp final image.
- A more durable source master for future reuse.

### What is not established

- There is no documented automatic recommendation boost merely for uploading
  at 4K.
- A 4K upload cannot fix an unclear hook, slow pacing, poor lighting, weak
  audio, or illegible composition.
- Shorts viewers on small mobile screens may receive little practical benefit,
  and destination platforms may downscale the upload.

### Costs

- Larger files, longer exports, and longer uploads.
- Longer high-resolution processing before release. YouTube says 4K is four
  times the pixel count of 1080p and can take roughly four times as long for the
  highest quality to become available.
- More storage and greater editing load.

## Operating decision

The setup cost has already been absorbed, and technical legibility is central
to the series, so the 4K standard is justified even without a direct algorithm
benefit. Publication must wait for `2160p` processing so launch viewers are not
served only the early low-resolution transcode.

## Current channel evidence

The latest complete YouTube device breakdown available on August 22 covers the
processed samples for Episodes 1 through 4. Aggregated across those episodes:

- desktop: 194 of 319 views, about 61%;
- mobile: 111 views, about 35%;
- TV: 7 views, about 2%; and
- tablet: 7 views, about 2%.

TV accounted for only about 2% of views but approximately 7% of estimated watch
time. Its estimated average view duration was roughly 3.4 minutes, versus about
1.1 minutes across the complete device sample. The watch-time metrics are
rounded and the TV sample contains only seven views, so this is not evidence
that 4K will grow the channel. It does show that the current audience is
desktop-heavy and that a small group of TV viewers watched for comparatively
long periods. Those are the two viewing contexts most likely to benefit from
sharper code and diagrams.

## How to evaluate the change

Episode 6 provides the final `1440p` operational baseline. Episodes after it
will be 4K, but this is not a controlled A/B test because their topics,
packaging, lengths, and audiences will differ.

Track:

- watch time and average percentage viewed by device type;
- TV watch time and TV average view duration;
- first-minute retention in code-heavy sections;
- viewer comments about legibility or image quality;
- processing delay and whether 4K threatens the release cadence; and
- performance of downscaled vertical uploads separately on each platform.

Reassess after at least three 4K long-form episodes and three 4K Shorts. Treat
changes as directional evidence, not proof that resolution caused them.

## Primary sources

- YouTube 4K guidance:
  https://support.google.com/youtube/answer/16597617
- YouTube upload encoding and bitrate guidance:
  https://support.google.com/youtube/answer/1722171
- YouTube high-resolution processing guidance:
  https://support.google.com/youtube/answer/71674
- YouTube recommendation signals:
  https://support.google.com/youtube/answer/16089387
