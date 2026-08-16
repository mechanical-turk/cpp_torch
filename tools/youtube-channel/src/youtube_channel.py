from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any, Callable

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


SCOPES = (
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",
)

CONFIG_DIR = Path.home() / ".config" / "dlatwd" / "youtube-analytics"
CLIENT_SECRET_PATH = CONFIG_DIR / "client_secret.json"
TOKEN_PATH = CONFIG_DIR / "token.json"

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
PRIVATE_DATA_DIR = REPOSITORY_ROOT / "youtube-series" / "analytics" / "private"
SNAPSHOTS_DIR = PRIVATE_DATA_DIR / "snapshots"
LATEST_PATH = PRIVATE_DATA_DIR / "latest.json"
ANALYTICS_CONFIG_PATH = (
    REPOSITORY_ROOT / "youtube-series" / "analytics" / "config.json"
)


@dataclass(frozen=True)
class Services:
    youtube: Any
    analytics: Any


def ensure_private_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    path.chmod(0o700)


def save_credentials(credentials: Credentials) -> None:
    ensure_private_directory(CONFIG_DIR)
    TOKEN_PATH.write_text(credentials.to_json(), encoding="utf-8")
    TOKEN_PATH.chmod(0o600)


def authorize(*, force_consent: bool = False) -> Credentials:
    if not CLIENT_SECRET_PATH.exists():
        raise RuntimeError(
            f"OAuth client credential not found at {CLIENT_SECRET_PATH}"
        )

    credentials: Credentials | None = None
    if TOKEN_PATH.exists() and not force_consent:
        credentials = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        save_credentials(credentials)

    if credentials and credentials.valid:
        granted = set(credentials.scopes or ())
        missing = set(SCOPES) - granted
        if not missing:
            return credentials

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
    credentials = flow.run_local_server(
        host="localhost",
        port=0,
        access_type="offline",
        prompt="consent",
        open_browser=True,
    )
    save_credentials(credentials)
    return credentials


def build_services(credentials: Credentials) -> Services:
    return Services(
        youtube=build(
            "youtube", "v3", credentials=credentials, cache_discovery=False
        ),
        analytics=build(
            "youtubeAnalytics",
            "v2",
            credentials=credentials,
            cache_discovery=False,
        ),
    )


def execute(request: Any) -> dict[str, Any]:
    response = request.execute()
    if not isinstance(response, dict):
        raise RuntimeError("YouTube API returned a non-object response")
    return response


def list_all_pages(
    request_factory: Callable[[str | None], Any],
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    page_token: str | None = None
    while True:
        response = execute(request_factory(page_token))
        items.extend(response.get("items", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            return items


def channel_details(youtube: Any) -> dict[str, Any]:
    response = execute(
        youtube.channels().list(
            part="id,snippet,contentDetails,statistics,status",
            mine=True,
        )
    )
    items = response.get("items", [])
    if len(items) != 1:
        raise RuntimeError(
            f"Expected exactly one authorized YouTube channel, found {len(items)}"
        )
    return items[0]


def uploaded_video_ids(youtube: Any, uploads_playlist_id: str) -> list[str]:
    items = list_all_pages(
        lambda token: youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=token,
        )
    )
    return [item["contentDetails"]["videoId"] for item in items]


def video_details(youtube: Any, video_ids: list[str]) -> list[dict[str, Any]]:
    videos: list[dict[str, Any]] = []
    for start in range(0, len(video_ids), 50):
        batch = video_ids[start : start + 50]
        response = execute(
            youtube.videos().list(
                part="id,snippet,contentDetails,status,statistics",
                id=",".join(batch),
                maxResults=50,
            )
        )
        videos.extend(response.get("items", []))
    return videos


def analytics_query(
    analytics: Any,
    *,
    video_id: str,
    start_date: str,
    end_date: str,
    metrics: str,
    dimensions: str | None = None,
    sort: str | None = None,
) -> dict[str, Any]:
    parameters: dict[str, Any] = {
        "ids": "channel==MINE",
        "startDate": start_date,
        "endDate": end_date,
        "metrics": metrics,
        "filters": f"video=={video_id}",
    }
    if dimensions:
        parameters["dimensions"] = dimensions
    if sort:
        parameters["sort"] = sort
    return execute(analytics.reports().query(**parameters))


def safe_analytics_query(
    analytics: Any,
    *,
    report_name: str,
    **parameters: Any,
) -> dict[str, Any]:
    try:
        return {
            "status": "ok",
            "response": analytics_query(analytics, **parameters),
        }
    except HttpError as error:
        return {
            "status": "error",
            "report": report_name,
            "http_status": error.resp.status,
            "message": str(error),
        }


def published_date(video: dict[str, Any]) -> str:
    value = video["snippet"]["publishedAt"]
    return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()


def analytics_start_date(video: dict[str, Any]) -> str:
    """Include the full local publication day despite UTC date boundaries."""
    return (date.fromisoformat(published_date(video)) - timedelta(days=1)).isoformat()


def analytics_config() -> dict[str, Any]:
    if not ANALYTICS_CONFIG_PATH.exists():
        raise RuntimeError(f"Analytics configuration not found: {ANALYTICS_CONFIG_PATH}")
    config = json.loads(ANALYTICS_CONFIG_PATH.read_text(encoding="utf-8"))
    date.fromisoformat(config["series_started_on"])
    return config


def series_videos(videos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    config = analytics_config()
    started_on = date.fromisoformat(config["series_started_on"])
    included = set(config.get("included_video_ids", []))
    excluded = set(config.get("excluded_video_ids", []))
    return [
        video
        for video in videos
        if video["id"] not in excluded
        and (
            video["id"] in included
            or date.fromisoformat(published_date(video)) >= started_on
        )
    ]


def collect_video_analytics(
    analytics: Any, video: dict[str, Any], end_date: str, *, full: bool
) -> dict[str, Any]:
    video_id = video["id"]
    start_date = analytics_start_date(video)
    common = {
        "analytics": analytics,
        "video_id": video_id,
        "start_date": start_date,
        "end_date": end_date,
    }

    reports = {
        "video_id": video_id,
        "title": video["snippet"]["title"],
        "published_at": video["snippet"]["publishedAt"],
        "basic": safe_analytics_query(
            report_name="basic",
            metrics=(
                "engagedViews,views,comments,likes,shares,"
                "estimatedMinutesWatched,averageViewDuration,"
                "averageViewPercentage,subscribersGained,subscribersLost"
            ),
            **common,
        ),
        "daily": safe_analytics_query(
            report_name="daily",
            metrics=(
                "engagedViews,views,estimatedMinutesWatched,"
                "averageViewDuration,averageViewPercentage,"
                "subscribersGained,subscribersLost"
            ),
            dimensions="day",
            sort="day",
            **common,
        ),
        "traffic_sources": safe_analytics_query(
            report_name="traffic_sources",
            metrics="views,estimatedMinutesWatched",
            dimensions="insightTrafficSourceType",
            sort="-views",
            **common,
        ),
    }
    if full:
        reports["devices"] = safe_analytics_query(
            report_name="devices",
            metrics="views,estimatedMinutesWatched",
            dimensions="deviceType",
            sort="-views",
            **common,
        )
        reports["countries"] = safe_analytics_query(
            report_name="countries",
            metrics="views,estimatedMinutesWatched",
            dimensions="country",
            sort="-views",
            **common,
        )
    return reports


def write_snapshot(payload: dict[str, Any]) -> Path:
    timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H-%M-%SZ")
    ensure_private_directory(SNAPSHOTS_DIR)
    snapshot_path = SNAPSHOTS_DIR / f"{timestamp}.json"
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    snapshot_path.write_text(rendered, encoding="utf-8")
    snapshot_path.chmod(0o600)

    ensure_private_directory(PRIVATE_DATA_DIR)
    LATEST_PATH.write_text(rendered, encoding="utf-8")
    LATEST_PATH.chmod(0o600)
    return snapshot_path


def command_auth(args: argparse.Namespace) -> int:
    credentials = authorize(force_consent=args.force)
    print(f"Authorized scopes: {', '.join(credentials.scopes or ())}")
    print(f"Token stored securely at {TOKEN_PATH}")
    return 0


def command_sync(args: argparse.Namespace) -> int:
    credentials = authorize()
    services = build_services(credentials)
    channel = channel_details(services.youtube)
    uploads_playlist_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
    ids = uploaded_video_ids(services.youtube, uploads_playlist_id)
    all_videos = video_details(services.youtube, ids)
    videos = series_videos(all_videos)
    end_date = date.today().isoformat()

    print(f"Channel: {channel['snippet']['title']} ({channel['id']})", flush=True)
    print(
        f"Collecting {len(videos)} series videos through {end_date} "
        f"({len(all_videos) - len(videos)} historical uploads ignored)...",
        flush=True,
    )

    payload = {
        "schema_version": 1,
        "collected_at": datetime.now(UTC).isoformat(),
        "analytics_end_date": end_date,
        "channel": channel,
        "videos": videos,
        "ignored_historical_video_count": len(all_videos) - len(videos),
        "full_breakdowns": args.full,
        "analytics": [],
    }
    for index, video in enumerate(videos, start=1):
        print(
            f"[{index}/{len(videos)}] {video['snippet']['title']}",
            flush=True,
        )
        payload["analytics"].append(
            collect_video_analytics(
                services.analytics, video, end_date, full=args.full
            )
        )
    snapshot_path = write_snapshot(payload)
    print(f"Snapshot written to {snapshot_path}")
    print(f"Latest snapshot written to {LATEST_PATH}")
    return 0


def first_row(report: dict[str, Any]) -> dict[str, Any] | None:
    if report.get("status") != "ok":
        return None
    response = report["response"]
    rows = response.get("rows") or []
    if not rows:
        return None
    headers = [header["name"] for header in response.get("columnHeaders", [])]
    return dict(zip(headers, rows[0], strict=True))


def command_report(_: argparse.Namespace) -> int:
    if not LATEST_PATH.exists():
        raise RuntimeError(
            f"No analytics snapshot exists. Run `make youtube-analytics-sync` first."
        )
    payload = json.loads(LATEST_PATH.read_text(encoding="utf-8"))
    print(f"Collected: {payload['collected_at']}")
    print(f"Channel: {payload['channel']['snippet']['title']}")
    print()
    managed_ids = {video["id"] for video in series_videos(payload["videos"])}
    metadata_by_id = {
        video["id"]: video
        for video in payload["videos"]
        if video["id"] in managed_ids
    }
    for video_analytics in payload["analytics"]:
        if video_analytics["video_id"] not in managed_ids:
            continue
        row = first_row(video_analytics["basic"])
        metadata = metadata_by_id[video_analytics["video_id"]]
        public_statistics = metadata.get("statistics", {})
        status = metadata.get("status", {})
        print(video_analytics["title"])
        if row is None:
            print(
                "  Analytics unavailable or not yet processed; "
                f"public_views={public_statistics.get('viewCount', 'unavailable')} "
                f"likes={public_statistics.get('likeCount', 'unavailable')} "
                f"comments={public_statistics.get('commentCount', 'unavailable')} "
                f"privacy={status.get('privacyStatus', 'unknown')}"
            )
            continue
        print(
            "  "
            f"views={row.get('views', 0)} "
            f"watch_minutes={row.get('estimatedMinutesWatched', 0)} "
            f"average_seconds={row.get('averageViewDuration', 0)} "
            f"average_percentage={row.get('averageViewPercentage', 0)} "
            f"subscribers=+{row.get('subscribersGained', 0)}"
            f"/-{row.get('subscribersLost', 0)}"
        )
    return 0


def publishing_section(document: str, *headings: str) -> str:
    for heading in headings:
        pattern = re.compile(
            rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
            re.MULTILINE | re.DOTALL,
        )
        match = pattern.search(document)
        if not match:
            continue
        body = match.group(1).strip()
        fenced = re.fullmatch(r"```(?:text)?\s*\n(.*?)\n```", body, re.DOTALL)
        return fenced.group(1).strip() if fenced else body
    expected = " or ".join(f"`{heading}`" for heading in headings)
    raise RuntimeError(f"Missing {expected} section in publishing package")


def publishing_package(path: Path) -> dict[str, Any]:
    document = path.read_text(encoding="utf-8")
    tags = [
        tag.strip()
        for tag in publishing_section(document, "Suggested tags")
        .replace("\n", " ")
        .split(",")
        if tag.strip()
    ]
    return {
        "title": publishing_section(document, "Final title", "Recommended title"),
        "description": publishing_section(
            document, "YouTube description", "Description"
        ),
        "tags": tags,
        "pinned_comment": publishing_section(document, "Pinned comment"),
    }


def owned_video(youtube: Any, video_id: str) -> dict[str, Any]:
    response = execute(
        youtube.videos().list(part="id,snippet,status", id=video_id, maxResults=1)
    )
    items = response.get("items", [])
    if len(items) != 1:
        raise RuntimeError(f"Video `{video_id}` was not found")
    return items[0]


def render_diff(label: str, current: str, desired: str) -> None:
    print(f"\n{label}:")
    if current == desired:
        print("  unchanged")
        return
    print(
        "".join(
            difflib.unified_diff(
                current.splitlines(keepends=True),
                desired.splitlines(keepends=True),
                fromfile="current",
                tofile="desired",
            )
        ).rstrip()
    )


def desired_video_snippet(
    current: dict[str, Any], package: dict[str, Any]
) -> dict[str, Any]:
    snippet = {
        "title": package["title"],
        "description": package["description"],
        "tags": package["tags"],
        "categoryId": current["categoryId"],
    }
    for optional in ("defaultLanguage", "defaultAudioLanguage"):
        if optional in current:
            snippet[optional] = current[optional]
    return snippet


def channel_comment_exists(
    youtube: Any, *, channel_id: str, video_id: str, text: str
) -> bool:
    threads = list_all_pages(
        lambda token: youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            order="time",
            textFormat="plainText",
            pageToken=token,
        )
    )
    for thread in threads:
        snippet = thread["snippet"]["topLevelComment"]["snippet"]
        author_id = snippet.get("authorChannelId", {}).get("value")
        if author_id == channel_id and snippet.get("textOriginal") == text:
            return True
    return False


def post_comment(youtube: Any, *, video_id: str, text: str) -> dict[str, Any]:
    return execute(
        youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {"snippet": {"textOriginal": text}},
                }
            },
        )
    )


def command_package(args: argparse.Namespace) -> int:
    package_path = Path(args.package).resolve()
    package = publishing_package(package_path)
    services = build_services(authorize())
    channel = channel_details(services.youtube)
    video = owned_video(services.youtube, args.video_id)
    current = video["snippet"]
    desired = desired_video_snippet(current, package)

    render_diff("Title", current.get("title", ""), desired["title"])
    render_diff("Description", current.get("description", ""), desired["description"])
    render_diff(
        "Tags",
        "\n".join(current.get("tags", [])),
        "\n".join(desired.get("tags", [])),
    )

    comment_exists = channel_comment_exists(
        services.youtube,
        channel_id=channel["id"],
        video_id=args.video_id,
        text=package["pinned_comment"],
    )
    print("\nPinned-comment text:")
    print("  already posted" if comment_exists else package["pinned_comment"])

    if not args.apply:
        print("\nDry run only. Re-run with `--apply` to update metadata and post the comment.")
        return 0

    execute(
        services.youtube.videos().update(
            part="snippet",
            body={"id": args.video_id, "snippet": desired},
        )
    )
    print("Metadata updated.")
    if not comment_exists:
        result = post_comment(
            services.youtube,
            video_id=args.video_id,
            text=package["pinned_comment"],
        )
        comment_id = result["snippet"]["topLevelComment"]["id"]
        print(f"Comment posted: {comment_id}")
    print("Pinning is not exposed by the YouTube API; pin this comment in Studio.")
    return 0


def owned_playlists(youtube: Any) -> list[dict[str, Any]]:
    return list_all_pages(
        lambda token: youtube.playlists().list(
            part="id,snippet,status,contentDetails",
            mine=True,
            maxResults=50,
            pageToken=token,
        )
    )


def find_playlist(youtube: Any, title: str) -> dict[str, Any] | None:
    matches = [
        playlist
        for playlist in owned_playlists(youtube)
        if playlist["snippet"]["title"] == title
    ]
    if len(matches) > 1:
        raise RuntimeError(f"Multiple playlists are named `{title}`")
    return matches[0] if matches else None


def command_playlist_ensure(args: argparse.Namespace) -> int:
    services = build_services(authorize())
    existing = find_playlist(services.youtube, args.title)
    description = args.description or ""
    if existing:
        print(f"Playlist already exists: {existing['id']}")
        render_diff(
            "Description", existing["snippet"].get("description", ""), description
        )
        return 0
    print(f"Would create public playlist: {args.title}")
    if not args.apply:
        print("Dry run only. Re-run with `--apply` to create it.")
        return 0
    result = execute(
        services.youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {"title": args.title, "description": description},
                "status": {"privacyStatus": "public"},
            },
        )
    )
    print(f"Playlist created: {result['id']}")
    return 0


def command_playlist_add(args: argparse.Namespace) -> int:
    services = build_services(authorize())
    playlist = find_playlist(services.youtube, args.title)
    if not playlist:
        raise RuntimeError(f"Playlist `{args.title}` does not exist")
    items = list_all_pages(
        lambda token: services.youtube.playlistItems().list(
            part="id,snippet,contentDetails",
            playlistId=playlist["id"],
            maxResults=50,
            pageToken=token,
        )
    )
    if any(item["contentDetails"]["videoId"] == args.video_id for item in items):
        print("Video is already in the playlist.")
        return 0
    print(f"Would add video {args.video_id} to `{args.title}`.")
    if not args.apply:
        print("Dry run only. Re-run with `--apply` to add it.")
        return 0
    execute(
        services.youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist["id"],
                    "resourceId": {"kind": "youtube#video", "videoId": args.video_id},
                }
            },
        )
    )
    print("Video added to playlist.")
    return 0


def command_thumbnail(args: argparse.Namespace) -> int:
    path = Path(args.file).resolve()
    if not path.is_file():
        raise RuntimeError(f"Thumbnail file does not exist: {path}")
    print(f"Would upload {path} for video {args.video_id}.")
    if not args.apply:
        print("Dry run only. Re-run with `--apply` to upload it.")
        return 0
    services = build_services(authorize())
    result = execute(
        services.youtube.thumbnails().set(
            videoId=args.video_id,
            media_body=MediaFileUpload(str(path), resumable=False),
        )
    )
    print(f"Thumbnail uploaded ({len(result.get('items', []))} sizes returned).")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        prog="youtube-channel",
        description="Private local YouTube analytics and channel management",
    )
    commands = root.add_subparsers(dest="command", required=True)

    auth = commands.add_parser("auth", help="Authorize or refresh OAuth access")
    auth.add_argument(
        "--force", action="store_true", help="Force a new interactive consent flow"
    )
    auth.set_defaults(handler=command_auth)

    sync = commands.add_parser("sync", help="Collect channel-wide analytics")
    sync.add_argument(
        "--full",
        action="store_true",
        help="Also collect slower device and country breakdowns",
    )
    sync.set_defaults(handler=command_sync)

    report = commands.add_parser("report", help="Summarize the latest snapshot")
    report.set_defaults(handler=command_report)

    package = commands.add_parser(
        "package",
        help="Diff or apply video metadata and pinned-comment text from publishing.md",
    )
    package.add_argument("--video-id", required=True)
    package.add_argument("--package", required=True)
    package.add_argument("--apply", action="store_true")
    package.set_defaults(handler=command_package)

    playlist_ensure = commands.add_parser(
        "playlist-ensure", help="Create a public playlist if it does not exist"
    )
    playlist_ensure.add_argument("--title", required=True)
    playlist_ensure.add_argument("--description")
    playlist_ensure.add_argument("--apply", action="store_true")
    playlist_ensure.set_defaults(handler=command_playlist_ensure)

    playlist_add = commands.add_parser(
        "playlist-add", help="Add a video to an existing playlist"
    )
    playlist_add.add_argument("--title", required=True)
    playlist_add.add_argument("--video-id", required=True)
    playlist_add.add_argument("--apply", action="store_true")
    playlist_add.set_defaults(handler=command_playlist_add)

    thumbnail = commands.add_parser(
        "thumbnail", help="Upload a custom video thumbnail"
    )
    thumbnail.add_argument("--video-id", required=True)
    thumbnail.add_argument("--file", required=True)
    thumbnail.add_argument("--apply", action="store_true")
    thumbnail.set_defaults(handler=command_thumbnail)
    return root


def main() -> None:
    args = parser().parse_args()
    try:
        raise SystemExit(args.handler(args))
    except (HttpError, OSError, RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
