# Local analytics dashboard

The dashboard is a read-only view over the private YouTube, X, and Instagram
snapshots already produced by the repository's collectors.

Run it from the repository root:

```sh
make analytics-dashboard
```

Then open <http://127.0.0.1:8765>.

YouTube subscribers, X followers, and Instagram followers are read directly
from timestamped API snapshots. TikTok and LinkedIn remain visibly unavailable
until a private manual snapshot is supplied at:

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
