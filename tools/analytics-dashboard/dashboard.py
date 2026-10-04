#!/usr/bin/env python3
"""Read-only local dashboard for the series' private analytics snapshots."""

from __future__ import annotations

import argparse
import json
import mimetypes
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from native_insights import load_records, evidence_file, image_type


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


def timestamp_value(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return float("-inf")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return float("-inf")
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.timestamp()


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
                "reports": {key: value for key, value in analytics.items() if isinstance(value, dict)},
                "duration": video.get("contentDetails", {}).get("duration"),
                "source_captured_at": data.get("collected_at"),
                "analytics_end_date": data.get("analytics_end_date"),
            }
        )

    return {
        "platform": "YouTube",
        "handle": channel.get("snippet", {}).get("customUrl", "@mechaturka"),
        "followers": int(statistics.get("subscriberCount", 0)),
        "metric_label": "Subscribers",
        "total_views": int(statistics.get("viewCount", 0)),
        "captured_at": data.get("collected_at"),
        "content": content,
    }


def load_x() -> dict[str, Any]:
    post_data = load_json(PRIVATE_ROOT / "x" / "latest.json") or {}
    audience_data = (
        load_json(PRIVATE_ROOT / "x" / "audience-latest.json") or post_data
    )
    account = audience_data.get("account", {})
    metrics = account.get("public_metrics", {})
    media_by_key = {
        item.get("media_key"): item for item in post_data.get("media", [])
    }
    posts = []
    for post in post_data.get("posts", []):
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
                "source_captured_at": iso_from_epoch(post_data.get("captured_at")),
            }
        )
    return {
        "platform": "X",
        "handle": f"@{account.get('username', 'mechaturka')}",
        "followers": metrics.get("followers_count"),
        "metric_label": "Followers",
        "captured_at": iso_from_epoch(audience_data.get("captured_at")),
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
        "metric_label": "Followers",
        "captured_at": iso_from_epoch(data.get("captured_at")),
        "content": media,
    }


def load_manual_tiktok_content() -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
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
                "captured_at": item.get("captured_at") or data.get("captured_at"),
                "metrics": {
                    "views": item.get("views"),
                    "likes": item.get("likes"),
                    "comments": item.get("comments"),
                    "shares": item.get("shares"),
                },
                "source": "manual",
            }
        )
    return account, data, content


def merge_tiktok_content(
    primary: list[dict[str, Any]], supplemental: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], bool]:
    merged = list(primary)
    ids = {str(item.get("id")) for item in merged if item.get("id")}
    urls = {str(item.get("url")) for item in merged if item.get("url")}
    added = False
    for item in supplemental:
        item_id = str(item.get("id")) if item.get("id") else None
        item_url = str(item.get("url")) if item.get("url") else None
        if (item_id and item_id in ids) or (item_url and item_url in urls):
            continue
        merged.append(item)
        added = True
        if item_id:
            ids.add(item_id)
        if item_url:
            urls.add(item_url)
    return merged, added


def load_tiktok() -> dict[str, Any]:
    manual_account, manual_data, manual_content = load_manual_tiktok_content()
    public_data = load_json(PRIVATE_ROOT / "tiktok-public" / "latest.json") or {}
    public_account = public_data.get("account", {})
    phyllo_profiles = load_json(PRIVATE_ROOT / "phyllo" / "latest-profiles.json")
    phyllo_content = load_json(PRIVATE_ROOT / "phyllo" / "latest-content.json")
    phyllo_summary = load_json(PRIVATE_ROOT / "phyllo" / "latest-summary.json") or {}
    if isinstance(phyllo_profiles, list) and isinstance(phyllo_content, list):
        profile = next(
            (
                item
                for item in phyllo_profiles
                if str(item.get("platform", "")).lower() == "tiktok"
            ),
            None,
        )
        if profile is not None:
            audience_candidates = [
                {
                    "followers": profile.get("followers"),
                    "captured_at": profile.get("updated_at")
                    or phyllo_summary.get("collected_at"),
                    "source": "phyllo",
                },
                {
                    "followers": public_account.get("follower_count"),
                    "captured_at": iso_from_epoch(public_data.get("captured_at")),
                    "source": "public-profile",
                },
                {
                    "followers": manual_account.get("followers"),
                    "captured_at": manual_account.get("captured_at"),
                    "source": "manual",
                },
            ]
            audience = max(
                (item for item in audience_candidates if item["followers"] is not None),
                key=lambda item: timestamp_value(item["captured_at"]),
                default={
                    "followers": None,
                    "captured_at": profile.get("updated_at")
                    or phyllo_summary.get("collected_at"),
                    "source": "phyllo",
                },
            )
            content = []
            for item in phyllo_content:
                if str(item.get("platform", "")).lower() != "tiktok":
                    continue
                content.append(
                    {
                        "id": item.get("external_id") or item.get("content_id"),
                        "title": (
                            item.get("title")
                            or item.get("description")
                            or "Untitled"
                        ).replace("\n", " "),
                        "published_at": item.get("published_at"),
                        "url": item.get("url"),
                        "metrics": {
                            "views": item.get("views"),
                            "likes": item.get("likes"),
                            "comments": item.get("comments"),
                            "shares": item.get("shares"),
                            **{key: item.get(key) for key in (
                                "average_watch_seconds", "duration_seconds", "organic_impressions",
                                "organic_reach", "paid_impressions", "paid_reach", "replays",
                                "reposts", "saves", "watch_time_hours"
                            )},
                        },
                        "source": "phyllo",
                        "source_captured_at": item.get("updated_at"),
                    }
                )
            content, used_manual = merge_tiktok_content(content, manual_content)
            return {
                "platform": "TikTok",
                "handle": f"@{profile.get('username', 'mechaturka')}",
                "followers": audience["followers"],
                "metric_label": "Followers",
                "captured_at": audience["captured_at"],
                "content": content,
                "source": (
                    ("phyllo+manual" if used_manual else "phyllo")
                    if audience["source"] == "phyllo"
                    else f"phyllo-content+{audience['source']}-audience"
                    + ("+manual-content" if used_manual else "")
                ),
                "provider_updated_at": profile.get("updated_at"),
            }

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
                    "source": "api",
                }
            )
        content, used_manual = merge_tiktok_content(content, manual_content)
        return {
            "platform": "TikTok",
            "handle": account.get("display_name", "@mechaturka"),
            "followers": account.get("follower_count"),
            "metric_label": "Followers",
            "captured_at": iso_from_epoch(api_data.get("captured_at")),
            "content": content,
            "source": "api+manual" if used_manual else "api",
        }

    return {
        "platform": "TikTok",
        "handle": manual_account.get("handle", "@mechaturka"),
        "followers": manual_account.get("followers"),
        "metric_label": "Followers",
        "captured_at": manual_data.get("captured_at") or manual_account.get("captured_at"),
        "content": manual_content,
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
                "metric_label": "Followers",
                "captured_at": entry.get("captured_at"),
                "content": [],
                "source": "manual",
            }
        )
    return result


def load_github() -> dict[str, Any]:
    data = load_json(PRIVATE_ROOT / "github" / "latest.json") or {}
    repository = data.get("repository", {})
    return {
        "platform": "GitHub",
        "handle": repository.get(
            "full_name", "mechanical-turk/deep-learning-all-the-way-down"
        ),
        "followers": repository.get("stargazers_count"),
        "metric_label": "Stars",
        "captured_at": iso_from_epoch(data.get("captured_at")),
        "content": [],
        "source": "github-api",
    }


def load_audience_history() -> dict[str, list[dict[str, Any]]]:
    history: dict[str, list[dict[str, Any]]] = {
        "YouTube": [],
        "X": [],
        "Instagram": [],
        "TikTok": [],
        "LinkedIn": [],
        "GitHub": [],
    }

    for path in sorted((PRIVATE_ROOT / "snapshots").glob("*.json")):
        data = load_json(path) or {}
        count = data.get("channel", {}).get("statistics", {}).get("subscriberCount")
        if count is not None:
            history["YouTube"].append(
                {"captured_at": data.get("collected_at"), "followers": int(count)}
            )

    # Preserve the older follower history embedded in explicit post snapshots,
    # then append the new lightweight audience-only snapshots.
    seen_x_points: set[tuple[str | None, Any]] = set()
    for folder in (
        PRIVATE_ROOT / "x" / "snapshots",
        PRIVATE_ROOT / "x" / "audience-snapshots",
    ):
        for path in sorted(folder.glob("*.json")):
            data = load_json(path) or {}
            count = (
                data.get("account", {})
                .get("public_metrics", {})
                .get("followers_count")
            )
            point = (iso_from_epoch(data.get("captured_at")), count)
            if count is not None and point not in seen_x_points:
                history["X"].append(
                    {"captured_at": point[0], "followers": point[1]}
                )
                seen_x_points.add(point)

    for platform, folder, extractor in (
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

    for path in sorted((PRIVATE_ROOT / "tiktok-public" / "snapshots").glob("*.json")):
        data = load_json(path) or {}
        count = data.get("account", {}).get("follower_count")
        if count is not None:
            history["TikTok"].append(
                {
                    "captured_at": iso_from_epoch(data.get("captured_at")),
                    "followers": count,
                }
            )

    for path in sorted((PRIVATE_ROOT / "phyllo" / "runs").glob("*/profiles.json")):
        profiles = load_json(path)
        if not isinstance(profiles, list):
            continue
        profile = next(
            (
                item
                for item in profiles
                if str(item.get("platform", "")).lower() == "tiktok"
            ),
            None,
        )
        if profile is None or profile.get("followers") is None:
            continue
        summary = load_json(path.parent / "summary.json") or {}
        history["TikTok"].append(
            {
                "captured_at": summary.get("collected_at"),
                "followers": profile.get("followers"),
            }
        )

    manual = load_json(PRIVATE_ROOT / "manual-audience.json") or {}
    if not history["TikTok"]:
        for point in manual.get("tiktok", {}).get("history", []):
            history["TikTok"].append(point)
    for point in manual.get("linkedin", {}).get("history", []):
        history["LinkedIn"].append(point)

    for path in sorted((PRIVATE_ROOT / "github" / "snapshots").glob("*.json")):
        data = load_json(path) or {}
        count = data.get("repository", {}).get("stargazers_count")
        if count is not None:
            history["GitHub"].append(
                {
                    "captured_at": iso_from_epoch(data.get("captured_at")),
                    "followers": count,
                }
            )

    return history


def dashboard_payload() -> dict[str, Any]:
    platforms = [
        load_youtube(),
        load_x(),
        load_instagram(),
        load_tiktok(),
        *load_manual_platforms(),
        load_github(),
    ]
    return {
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "platforms": platforms,
        "audience_history": load_audience_history(),
        "native_insights": load_records(PRIVATE_ROOT / "native-insights"),
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

        if path.startswith("/native-evidence/"):
            target = evidence_file(path.removeprefix("/native-evidence/"), PRIVATE_ROOT / "native-insights")
            if target is None:
                self.send_error(404)
                return
            try:
                content_type, _ = image_type(target)
            except (OSError, ValueError):
                self.send_error(404)
                return
            body = target.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
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
        self.send_header("Cache-Control", "no-store")
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
