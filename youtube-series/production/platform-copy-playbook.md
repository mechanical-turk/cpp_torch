# Platform Copy and SEO Playbook

Read this file before writing or approving any title, description, caption,
comment, social post, profile text, alt text, or publishing package.

Copy is not final until every applicable step below passes.

For a `publishing.md`, also follow the
[publishing-package checklist](publishing-playbook.md). Its required order is
checklist plan, publishing content, checklist audit, critique, and final score.
This file remains the authority for copy and platform-specific SEO research.

## 1. Establish the content truth

- Inspect the final video, captions, code, benchmark output, or live artifact.
- Identify the exact subject, language, operation, result, and audience.
- Do not rely on an earlier script when the recording changed.
- Do not claim that one machine's benchmark applies universally.

## 2. Research how people describe the subject

Research each selected platform separately. Do not copy a keyword or hashtag
set from one platform to another.

Use the best evidence currently available:

1. The owned account's search terms, traffic sources, and successful posts.
2. Live platform search and autocomplete.
3. Current comparable posts and videos.
4. Google Trends or broader search evidence when it helps distinguish wording.

Record:

- research date;
- platform;
- sources checked;
- candidate phrases;
- observed evidence or unavailable evidence;
- the primary phrase selected;
- supporting terms selected;
- hashtags retained or rejected, with reasons.

No platform copy is final when this record is missing.

## 3. Choose the search language

- Put the strongest accurate subject phrase near the beginning.
- Prefer terms real viewers use over internal project vocabulary.
- Include the language and central concept when they matter, such as `C++ loop`,
  `C++ performance`, `automatic differentiation`, or `matrix multiplication`.
- Introduce the concrete idea before specialist vocabulary.
- Optimize for qualified discovery and correct audience matching, not keyword
  density.
- Never add a term the content does not fulfill.

## 4. Write the copy

- Lead with the problem, result, contradiction, question, or useful idea.
- Use simple, direct English and active voice.
- Use professional capitalization and restrained punctuation.
- Keep natural sentence lengths and a cadence a technically serious person
  would use aloud.
- Remove corporate language, manufactured hype, filler, fake intimacy, and
  slogan-like fragments.
- Avoid canned structures such as `it is not X, it is Y` and abrupt
  `X. This is Y.` transitions.
- Do not force lowercase to manufacture informality.
- Do not manufacture informality with stage directions such as `say`, `imagine`,
  or `picture this`. State the situation directly.
- Never use an em dash.
- Use ordinary characters when possible, such as `41x` instead of `41×`.

## 5. Audit hashtags and metadata tags separately

- Hashtags are visible navigation and discovery links.
- YouTube metadata tags are backend descriptors.
- Neither replaces a strong title or natural caption.
- Retain only researched terms with evidence of real platform use.
- Reject invented or weak compounds such as `#cppperformance` unless current
  evidence supports them.
- Never use `#shorts`.
- YouTube descriptions normally use no hashtags.
- A small relevant set is better than a decorative block.

## 6. Apply platform rules

### YouTube

- Long-form titles contain `Deep Learning, All the Way Down` and `#N`.
- Titles begin with the searchable episode subject, not `Episode N is out`.
- Descriptions use plain text, not Markdown styling.
- Descriptions naturally describe the actual C++ and deep-learning concepts.
- Shorts titles state the concrete question or result in ordinary search
  language.

### Instagram

- Put the concrete subject in the opening line.
- Use no external URL in the Reel caption or first comment.
- Research Instagram hashtags independently.
- Add accurate alt text.
- Keep the caption useful without requiring the viewer to leave Instagram.

### TikTok

- Put the concrete subject in the opening line.
- Use no external URL in the caption.
- Research TikTok search terms and hashtags independently.
- Keep the caption compact enough that the topic remains visible in the feed.

### X

- Do not open an episode announcement with release administration.
- Name `Deep Learning, All the Way Down` when identifying an episode.
- Keep personal posts self-contained and normally link-free.
- Give an episode announcement exactly one previewable external URL: the
  YouTube watch URL. Put the playlist and GitHub repository in the navigation
  reply after publication.
- Do not include the recurring line that the complete implementation remains
  one C++23 file using only the standard library, or a rephrased equivalent.

### LinkedIn

- Lead with the technical idea or reason the work matters.
- Name `Deep Learning, All the Way Down` when identifying an episode.
- Give the main announcement exactly one previewable external URL: the YouTube
  watch URL. Put GitHub or secondary navigation in the first author comment
  when useful.
- Do not include the recurring line that the complete implementation remains
  one C++23 file using only the standard library, or a rephrased equivalent.

### Reddit

- Write for the specific community and check its current rules.
- Lead with the project milestone and useful technical evidence.
- Do not post a generic episode announcement.
- Put GitHub before YouTube when both links appear.
- End with one specific question the community can answer.

## 7. Final release gate

Before approving copy, answer yes to every applicable item:

- Is the platform-specific keyword research record complete?
- Does the first line contain the strongest accurate subject phrase naturally?
- Are the title, caption, description, and tags factually consistent with the
  final media?
- Were hashtags researched separately for this platform?
- Does every retained keyword or hashtag have a reason to exist?
- Is the language direct, natural, professional, and free of banned cadence?
- Is the copy free of em dashes and `#shorts`?
- Are links ordered correctly for the desired preview?
- Is the upload filename descriptive and keyword-rich?

If any answer is no, the copy is not ready to publish.

For a Short, Reel, or TikTok, copy approval alone does not clear upload
readiness. Complete `docs/operations/short-upload-gate.md` on the final export
and include its results in the publishing package.

## Publishing package research template

Every selected platform gets its own record:

```text
Platform:
Research date:
Sources checked:
Owned-account evidence:
Candidate search phrases:
Primary phrase:
Supporting terms:
Hashtags retained:
Hashtags rejected:
Reasoning and evidence:
Unavailable evidence:
```
