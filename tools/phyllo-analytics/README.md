# Phyllo analytics experiment

This collector downloads profile and content analytics for the connected
YouTube, TikTok, and X accounts without integrating Phyllo into the main
dashboard.

## Configuration

The command reads credentials from environment variables first. For the current
local setup it can also safely parse `export NAME="value"` assignments from the
repository-root `phyllo.sh` file without executing that file.

Required values:

```text
PHYLLO_CLIENT_ID
PHYLLO_CLIENT_SECRET
PHYLLO_BASE_URL
PHYLLO_USER_ID
```

`phyllo.sh` is ignored by Git because it contains private credentials.

## Pull data

From the repository root:

```sh
make phyllo-sync
```

The default collection boundary is `2026-08-12`, when the series began. Change
it for an exploratory run with:

```sh
uv run --project tools/phyllo-analytics \
  phyllo-analytics sync --since 2026-08-20
```

The dashboard's routine refresh uses Phyllo only for TikTok:

```sh
make phyllo-tiktok-sync
```

Select one or more platforms explicitly with repeated `--platform` options.
With no option, the standalone experiment still collects all three platforms.

Private output is written under:

```text
youtube-series/analytics/private/phyllo/
```

Each run preserves raw API responses in a timestamped directory. The top-level
`latest-*` files provide flattened JSON and CSV views:

- `latest-profiles.json`
- `latest-profiles.csv`
- `latest-content.json`
- `latest-content.csv`
- `latest-summary.json`

## Safety

- Requests are sequential and rate-limited.
- HTTP 429 responses are retried with exponential backoff.
- Secrets are never written to reports.
- The collector is read-only.
- Raw and normalized analytics remain in the gitignored private directory.
