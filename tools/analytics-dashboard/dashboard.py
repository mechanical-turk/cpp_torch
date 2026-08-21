#!/usr/bin/env python3
"""Read-only local dashboard for the series' private analytics snapshots."""

from __future__ import annotations

import argparse
import json
import mimetypes
from dataclasses import dataclass
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[2]
PRIVATE_ROOT = REPO_ROOT / "youtube-series" / "analytics" / "private"
STATIC_ROOT = Path(__file__).resolve().parent / "static"


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def iso_from_epoch(value: Any) -> str | None:
    if not isinstance(value, (int, float)):
        return None
    return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()


def result_row(report: dict[str, Any] | None) -> dict[str, Any] | None:
    if not report:
        return None
    response = report.get("response", {})
    rows = response.get("rows", [])
    headers = response.get("columnHeaders", [])
    if not rows:
        return None
    names = [header.get("name") for header in headers]
    return dict(zip(names, rows[0], strict=False))


def load_youtube() -> dict[str, Any]:
    data = load_json(PRIVATE_ROOT / "latest.json") or {}
    channel = data.get("channel", {})
    statistics = channel.get("statistics", {})
    analytics_by_id = {
        item.get("video_id"): item for item in data.get("analytics", [])
    }

    content = []
    for video in data.get("videos", []):
        video_id = video.get("id")
        snippet = video.get("snippet", {})
        public = video.get("statistics", {})
        analytics = analytics_by_id.get(video_id, {})
        content.append(
            {
                "id": video_id,
                "title": snippet.get("title", "Untitled"),
                "published_at": snippet.get("publishedAt"),
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "public_views": int(public.get("viewCount", 0)),
                "likes": int(public.get("likeCount", 0)),
                "comments": int(public.get("commentCount", 0)),
                "analytics": result_row(analytics.get("basic")),
            }
        )

    return {
        "platform": "YouTube",
        "handle": channel.get("snippet", {}).get("customUrl", "@mechaturka"),
        "followers": int(statistics.get("subscriberCount", 0)),
        "total_views": int(statistics.get("viewCount", 0)),
        "captured_at": data.get("collected_at"),
        "content": content,
    }


def load_x() -> dict[str, Any]:
    data = load_json(PRIVATE_ROOT / "x" / "latest.json") or {}
    account = data.get("account", {})
    metrics = account.get("public_metrics", {})
    media_by_key = {item.get("media_key"): item for item in data.get("media", [])}
    posts = []
    for post in data.get("posts", []):
        media_keys = post.get("attachments", {}).get("media_keys", [])
        media = media_by_key.get(media_keys[0]) if media_keys else None
        posts.append(
            {
                "id": post.get("id"),
                "title": post.get("text", "").replace("\n", " "),
                "published_at": post.get("created_at"),
                "url": f"https://x.com/{account.get('username', 'mechaturka')}/status/{post.get('id')}",
                "metrics": post.get("non_public_metrics", {}),
                "public_metrics": post.get("public_metrics", {}),
                "media": media,
            }
        )
    return {
        "platform": "X",
        "handle": f"@{account.get('username', 'mechaturka')}",
        "followers": metrics.get("followers_count"),
        "captured_at": iso_from_epoch(data.get("captured_at")),
        "content": posts,
    }


def load_instagram() -> dict[str, Any]:
    data = load_json(PRIVATE_ROOT / "instagram" / "latest.json") or {}
    account = data.get("account", {})
    media = []
    for item in data.get("media", []):
        media.append(
            {
                "id": item.get("id"),
                "title": item.get("caption", "").replace("\n", " "),
                "published_at": item.get("timestamp"),
                "url": item.get("permalink"),
                "metrics": item.get("insights", {}),
                "likes": item.get("like_count", 0),
                "comments": item.get("comments_count", 0),
            }
        )
    return {
        "platform": "Instagram",
        "handle": f"@{account.get('username', 'mechaturka')}",
        "followers": account.get("followers_count"),
        "captured_at": iso_from_epoch(data.get("captured_at")),
        "content": media,
    }


def load_tiktok() -> dict[str, Any]:
    api_data = load_json(PRIVATE_ROOT / "tiktok" / "latest.json")
    if api_data is not None:
        account = api_data.get("account", {})
        content = []
        for item in api_data.get("videos", []):
            content.append(
                {
                    "id": item.get("id"),
                    "title": (item.get("video_description") or "Untitled").replace(
                        "\n", " "
                    ),
                    "published_at": iso_from_epoch(item.get("create_time")),
                    "url": item.get("share_url"),
                    "metrics": {
                        "views": item.get("view_count"),
                        "likes": item.get("like_count"),
                        "comments": item.get("comment_count"),
                        "shares": item.get("share_count"),
                    },
                }
            )
        return {
            "platform": "TikTok",
            "handle": account.get("display_name", "@mechaturka"),
            "followers": account.get("follower_count"),
            "captured_at": iso_from_epoch(api_data.get("captured_at")),
            "content": content,
            "source": "api",
        }

    # Fall back to a hand-maintained snapshot until `make tiktok-auth` and
    # `make tiktok-analytics-sync` have been run at least once.
    audience = load_json(PRIVATE_ROOT / "manual-audience.json") or {}
    account = audience.get("tiktok", {})
    data = load_json(PRIVATE_ROOT / "manual-tiktok.json") or {}

    content = []
    for item in data.get("videos", []):
        content.append(
            {
                "id": item.get("id"),
                "title": item.get("title", "Untitled"),
                "published_at": item.get("published_at"),
                "url": item.get("url"),
                "metrics": {
                    "views": item.get("views"),
                    "likes": item.get("likes"),
                    "comments": item.get("comments"),
                    "shares": item.get("shares"),
                },
            }
        )

    return {
        "platform": "TikTok",
        "handle": account.get("handle", "@mechaturka"),
        "followers": account.get("followers"),
        "captured_at": data.get("captured_at") or account.get("captured_at"),
        "content": content,
        "source": "manual",
    }


def load_manual_platforms() -> list[dict[str, Any]]:
    data = load_json(PRIVATE_ROOT / "manual-audience.json") or {}
    result = []
    for name in ("LinkedIn",):
        entry = data.get(name.lower(), {})
        result.append(
            {
                "platform": name,
                "handle": entry.get("handle", "@mechaturka"),
                "followers": entry.get("followers"),
                "captured_at": entry.get("captured_at"),
                "content": [],
                "source": "manual",
            }
        )
    return result


def load_audience_history() -> dict[str, list[dict[str, Any]]]:
    history: dict[str, list[dict[str, Any]]] = {
        "YouTube": [],
        "X": [],
        "Instagram": [],
        "TikTok": [],
        "LinkedIn": [],
    }

    for path in sorted((PRIVATE_ROOT / "snapshots").glob("*.json")):
        data = load_json(path) or {}
        count = data.get("channel", {}).get("statistics", {}).get("subscriberCount")
        if count is not None:
            history["YouTube"].append(
                {"captured_at": data.get("collected_at"), "followers": int(count)}
            )

    for platform, folder, extractor in (
        ("X", PRIVATE_ROOT / "x" / "snapshots", lambda d: d.get("account", {}).get("public_metrics", {}).get("followers_count")),
        ("Instagram", PRIVATE_ROOT / "instagram" / "snapshots", lambda d: d.get("account", {}).get("followers_count")),
        ("TikTok", PRIVATE_ROOT / "tiktok" / "snapshots", lambda d: d.get("account", {}).get("follower_count")),
    ):
        for path in sorted(folder.glob("*.json")):
            data = load_json(path) or {}
            count = extractor(data)
            if count is not None:
                history[platform].append(
                    {
                        "captured_at": iso_from_epoch(data.get("captured_at")),
                        "followers": count,
                    }
                )

    manual = load_json(PRIVATE_ROOT / "manual-audience.json") or {}
    if not history["TikTok"]:
        for point in manual.get("tiktok", {}).get("history", []):
            history["TikTok"].append(point)
    for point in manual.get("linkedin", {}).get("history", []):
        history["LinkedIn"].append(point)

    return history


def dashboard_payload() -> dict[str, Any]:
    platforms = [load_youtube(), load_x(), load_instagram(), load_tiktok(), *load_manual_platforms()]
    return {
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "platforms": platforms,
        "audience_history": load_audience_history(),
    }


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/dashboard":
            body = json.dumps(dashboard_payload()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        relative = "index.html" if path == "/" else path.lstrip("/")
        target = (STATIC_ROOT / relative).resolve()
        if STATIC_ROOT.resolve() not in target.parents and target != STATIC_ROOT.resolve():
            self.send_error(404)
            return
        try:
            body = target.read_bytes()
        except FileNotFoundError:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(target.name)[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"Analytics dashboard: http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
