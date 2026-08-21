# Local analytics dashboard

The dashboard is a read-only view over the private YouTube, X, Instagram, and
TikTok snapshots already produced by the repository's collectors.

Run it from the repository root:

```sh
make analytics-dashboard
```

Then open <http://127.0.0.1:8765>.

YouTube subscribers, X followers, Instagram followers, and TikTok followers
and video stats are read directly from timestamped API snapshots once
authorized (see "TikTok API setup" below). LinkedIn, and TikTok until it's
authorized, fall back to a private manual snapshot supplied at:

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
`youtube-series/analytics/private/manual-tiktok.json`, used only until the
real API is authorized:

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
