# Local analytics dashboard

The dashboard is a read-only view over the private YouTube, X, Instagram,
TikTok, and GitHub snapshots already produced by the repository's collectors.

Run it from the repository root:

```sh
make analytics-dashboard
```

Then open <http://127.0.0.1:8765>.

YouTube subscribers, X followers, Instagram followers, TikTok followers and
video stats, and GitHub repository stars are read from timestamped API
snapshots. LinkedIn, and TikTok until it is authorized, fall back to a private
manual snapshot supplied at:

Run `make analytics-sync` to refresh every default dashboard source. TikTok is
video analytics are included through Phyllo. Its public profile supplies the
freshest follower count when Phyllo's profile record lags. GitHub stars are
included through GitHub's public repository API. Tweet-level X data remains
excluded.

```text
youtube-series/analytics/private/manual-audience.json
```

Example:

```json
{
  "tiktok": {
    "handle": "@mechaturka",
    "followers": 0,
    "captured_at": "2026-08-17T09:00:00-04:00",
    "history": [
      {"captured_at": "2026-08-17T09:00:00-04:00", "followers": 0}
    ]
  },
  "linkedin": {
    "handle": "Kerem Kazan",
    "followers": 0,
    "captured_at": "2026-08-17T09:00:00-04:00",
    "history": [
      {"captured_at": "2026-08-17T09:00:00-04:00", "followers": 0}
    ]
  }
}
```

Unknown counts should remain absent or `null`; never enter an assumed zero.

TikTok also supports a hand-maintained per-video snapshot at
`youtube-series/analytics/private/manual-tiktok.json`. The dashboard uses it as
a complete fallback when no provider is available and as a gap-fill when a
connected provider has not indexed a newly published post yet. Provider records
win when the same video exists in both sources; missing manual metrics remain
`null` rather than being inferred:

```json
{
  "captured_at": null,
  "videos": [
    {
      "id": "7676185349994876190",
      "title": "This Check Can Never Catch an Overflow",
      "url": "https://www.tiktok.com/@mechaturka/video/7676185349994876190",
      "published_at": "2026-08-20T15:01:00-04:00",
      "views": null,
      "likes": null,
      "comments": null,
      "shares": null
    }
  ]
}
```

## TikTok API setup

TikTok's Display API is meaningfully different from the X and Instagram
integrations already in this repo: it's a confidential OAuth client (needs
a client secret, not just PKCE) and its redirect-URI rules are stricter, so
a plain `http://127.0.0.1` callback may or may not be accepted — this
depends on your app's configuration in TikTok's developer console and isn't
something that can be verified without actually registering the app.

1. Create an app at <https://developers.tiktok.com/>, add the **Login Kit**
   product, and add the `user.info.basic` and `video.list` scopes.
2. Register a redirect URI. Try `http://127.0.0.1:8766/callback` first — if
   the console accepts it, the flow below is fully automatic. If it
   doesn't, register any URI you control instead (even one that 404s is
   fine — TikTok still puts the authorization code in that URL's query
   string, which you copy from the browser's address bar).
3. Note the app's **Client Key** and **Client Secret**.
4. Run:

   ```sh
   make tiktok-auth
   ```

   This opens TikTok's authorization page and prompts for the Client Key
   and Client Secret the first time (stored under
   `~/.config/dlatwd/tiktok-analytics/`, outside the repo). If your
   redirect URI is the loopback default, authorization completes
   automatically. Otherwise, open the printed URL manually, approve access,
   and once TikTok redirects to your registered URI, copy the `code=`
   value from the address bar and run:

   ```sh
   UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics tiktok-auth --code PASTE_CODE_HERE
   ```

5. Verify with `make tiktok-test`, then pull real data with:

   ```sh
   make tiktok-analytics-sync
   ```

   This writes to `youtube-series/analytics/private/tiktok/`, which the
   dashboard prefers automatically over the manual snapshot once it exists.

Apps in development mode can typically read their own owner account's data
without full TikTok review, but this policy can change — `tiktok-test` is
the fastest way to confirm access actually works before relying on it.
# Expanded audience charts

Click **Expand chart** on any audience card for a large, timestamp-scaled view.
Select all snapshots, 30 days, 7 days, or 24 hours. Hover over the chart or use
the snapshot slider (including arrow keys) to inspect exact counts and times.
The expandable values table lists every observation in the selected range.
Close with the Close button, Escape, or a click outside the dialog.

Ranges end at the latest saved observation, not the current clock. Expanding
does not create finer source data; lines connect the existing snapshots.

Chart geometry tests: `node --test tools/analytics-dashboard/tests/test_charts.js`.

## Native platform evidence

The content detail dialog also exposes the full collected API reports. YouTube
includes its sampled retention curve plus basic, daily, traffic-source, device
and country tables (`make youtube-analytics-sync-full` supplies the latter two).
Instagram and X show available native-named metric fields; TikTok shows provider
watch-time, reach and other available fields, preserving unknowns and each
content record's source timestamp. These reports do not substitute for native
UI capture or claim API access to Studio-only impressions/CTR/skip metrics.

The dashboard opens with audience and latest-content summary cards, followed
by the content table. Click a content title's **View analysis** button to open
its detail dialog. Native captures appear there independently of API totals:
retention curves, timed creative events, engagement/conversion, original
screenshots and observed/hypothesis/next-test/limits notes. The capture selector
only lists observations for that post and platform. Estimates use dashed curve
segments. Close the dialog or press Escape to return to the summaries. Missing curves
and metrics remain explicitly unavailable. It is not an automatic phone scraper.

Capture screenshots through the platform UI and save originals privately. Write
a JSON record beside them using this shape (illustrative fields, not real data):

```json
{
  "id": "unique-platform-content-capture-id",
  "platform": "Instagram",
  "content_id": "native-post-id",
  "content_url": "https://www.instagram.com/reel/POST_ID/",
  "title": "Post title",
  "format": "short",
  "captured_at": "2026-09-07T14:00:00Z",
  "period": "Lifetime; All viewers",
  "source_surface": "Instagram iOS through iPhone Mirroring",
  "duration_seconds": 25,
  "screenshots": [
    {"id": "overview", "path": "overview.png", "label": "Overview"}
  ],
  "metrics": [
    {"key": "follows", "label": "Follows", "value": null,
     "unit": "count", "precision": "exact", "source": "overview"}
  ],
  "retention": [],
  "retention_definition": "Copy the native chart definition and filters",
  "events": [],
  "media_source": "Final master or verified transcript path",
  "analysis": {
    "observed": "Observed facts only",
    "hypotheses": "Possible explanations, not causal conclusions",
    "next_test": "A specific comparison and engagement guardrails",
    "limitations": "Missing screens, sample size and confounders"
  }
}
```

Each retention point has `seconds`, `percent`, `precision` and `source`.
Precision is `exact`, `rounded` or `estimated`. Percent uses 0–100 units, not
0–1 fractions; replay-based metrics may exceed 100%. Timed events have `seconds`
and `label` and require a final-media source. Use exact platform metric labels.
Canonical keys used for derived rates: `views`, `viewers`, `follows`,
`profile_visits`, `comments`, `shares`, `saves`. `viewers` must mean unique
viewers, not plays. Do not substitute account follower growth for post follows.

All measurements in a record must share a compatible analysis window and
audience filter. If screens use different windows, save separate records. Capture
screens in one short session, noting delays and rounding in limitations. Never
combine old screenshots with fresh totals to produce rates.

```sh
python3 tools/analytics-dashboard/native_insights.py /absolute/path/to/record.json
```

The importer validates provenance and time coordinates, copies screenshots into
`youtube-series/analytics/private/native-insights/<id>/`, and refuses to overwrite
an existing capture. Reload the dashboard after import. Only registered raster
screenshots are accessible from its private evidence route. Keep the server
bound to loopback; do not host or expose this private dashboard publicly.

The capture and interpretation checklist lives in
`docs/operations/native-performance-analysis.md`. Every future performance
analysis must use it, not just refresh API totals. Before the next script, read
the resulting report and open tests.

Checks:

```sh
python3 -m unittest discover -s tools/analytics-dashboard/tests
node --test tools/analytics-dashboard/tests/test_*.js
```
