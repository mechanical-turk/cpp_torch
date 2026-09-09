from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import re
import shutil
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SERIES_START = "2026-08-12"
SUPPORTED_PLATFORMS = {"youtube", "tiktok", "x"}
DEFAULT_OUTPUT = Path("youtube-series/analytics/private/phyllo")
EXPORT_PATTERN = re.compile(
    r'^\s*export\s+([A-Za-z_][A-Za-z0-9_]*)=(?:"([^"]*)"|\'([^\']*)\'|([^\s#]+))\s*$'
)


class PhylloError(RuntimeError):
    pass


@dataclass(frozen=True)
class Config:
    client_id: str
    client_secret: str
    base_url: str
    user_id: str


def parse_export_file(path: Path) -> dict[str, str]:
    """Read simple shell export assignments without executing shell code."""
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = EXPORT_PATTERN.match(line)
        if not match:
            continue
        name = match.group(1)
        value = next(part for part in match.groups()[1:] if part is not None)
        values[name] = value
    return values


def load_config(path: Path) -> Config:
    file_values = parse_export_file(path)

    def required(name: str) -> str:
        value = os.environ.get(name) or file_values.get(name)
        if not value:
            raise PhylloError(
                f"missing {name}; export it or define it in {path}"
            )
        return value

    return Config(
        client_id=required("PHYLLO_CLIENT_ID"),
        client_secret=required("PHYLLO_CLIENT_SECRET"),
        base_url=required("PHYLLO_BASE_URL").rstrip("/"),
        user_id=required("PHYLLO_USER_ID"),
    )


class PhylloClient:
    def __init__(
        self,
        config: Config,
        *,
        delay_seconds: float = 2.0,
        retries: int = 4,
        timeout_seconds: float = 30.0,
    ) -> None:
        self.config = config
        self.delay_seconds = delay_seconds
        self.retries = retries
        self.timeout_seconds = timeout_seconds
        self._last_request_at: float | None = None

    def _pace(self) -> None:
        if self._last_request_at is None:
            return
        remaining = self.delay_seconds - (time.monotonic() - self._last_request_at)
        if remaining > 0:
            time.sleep(remaining)

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        query = urlencode(
            {key: value for key, value in (params or {}).items() if value is not None}
        )
        url = f"{self.config.base_url}{endpoint}"
        if query:
            url = f"{url}?{query}"

        credentials = (
            f"{self.config.client_id}:{self.config.client_secret}".encode("utf-8")
        )
        authorization = base64.b64encode(credentials).decode("ascii")

        for attempt in range(self.retries + 1):
            self._pace()
            request = Request(
                url,
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Basic {authorization}",
                    "User-Agent": "dlatwd-phyllo-analytics/0.1",
                },
            )
            try:
                self._last_request_at = time.monotonic()
                with urlopen(request, timeout=self.timeout_seconds) as response:
                    return json.load(response)
            except HTTPError as error:
                body = error.read().decode("utf-8", errors="replace")
                if error.code == 429 and attempt < self.retries:
                    time.sleep(self.delay_seconds * (2 ** attempt))
                    continue
                raise PhylloError(
                    f"GET {endpoint} failed with HTTP {error.code}: {body}"
                ) from error
            except URLError as error:
                if attempt < self.retries:
                    time.sleep(self.delay_seconds * (2 ** attempt))
                    continue
                raise PhylloError(f"GET {endpoint} failed: {error.reason}") from error

        raise AssertionError("request retry loop ended unexpectedly")

    def paginated(
        self,
        endpoint: str,
        params: dict[str, Any],
        *,
        page_size: int,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        items: list[dict[str, Any]] = []
        pages: list[dict[str, Any]] = []
        offset = 0

        while True:
            page_params = {**params, "limit": page_size, "offset": offset}
            payload = self.get(endpoint, page_params)
            if not isinstance(payload, dict):
                raise PhylloError(f"unexpected response from {endpoint}")
            page_items = payload.get("data", [])
            if not isinstance(page_items, list):
                raise PhylloError(f"unexpected data field from {endpoint}")

            pages.append(payload)
            items.extend(item for item in page_items if isinstance(item, dict))
            if len(page_items) < page_size:
                return items, pages
            offset += page_size


def platform_name(record: dict[str, Any]) -> str:
    work_platform = record.get("work_platform") or {}
    return str(work_platform.get("name") or record.get("platform") or "unknown")


def nested_number(record: dict[str, Any], group: str, key: str) -> Any:
    nested = record.get(group)
    if isinstance(nested, dict) and key in nested:
        return nested.get(key)
    return record.get(key)


def normalize_profile(profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "platform": platform_name(profile),
        "account_id": (profile.get("account") or {}).get("id"),
        "profile_id": profile.get("id"),
        "external_id": profile.get("external_id"),
        "username": profile.get("platform_username") or profile.get("username"),
        "display_name": profile.get("platform_profile_name")
        or profile.get("full_name"),
        "url": profile.get("url"),
        "verified": profile.get("is_verified"),
        "followers": nested_number(profile, "reputation", "follower_count"),
        "following": nested_number(profile, "reputation", "following_count"),
        "subscribers": nested_number(profile, "reputation", "subscriber_count"),
        "paid_subscribers": nested_number(
            profile, "reputation", "paid_subscriber_count"
        ),
        "content_count": nested_number(profile, "reputation", "content_count"),
        "total_likes": nested_number(profile, "reputation", "like_count"),
        "watch_time_hours": nested_number(
            profile, "reputation", "watch_time_in_hours"
        ),
        "updated_at": profile.get("updated_at"),
    }


def normalize_content(content: dict[str, Any]) -> dict[str, Any]:
    engagement = content.get("engagement")
    if not isinstance(engagement, dict):
        engagement = {}

    def metric(name: str) -> Any:
        return engagement.get(name, content.get(name))

    return {
        "platform": platform_name(content),
        "account_id": (content.get("account") or {}).get("id"),
        "content_id": content.get("id"),
        "external_id": content.get("external_id"),
        "username": content.get("platform_username"),
        "title": content.get("title"),
        "description": content.get("description"),
        "type": content.get("type"),
        "format": content.get("format"),
        "published_at": content.get("published_at"),
        "url": content.get("url"),
        "duration_seconds": content.get("duration"),
        "views": metric("view_count"),
        "likes": metric("like_count"),
        "comments": metric("comment_count"),
        "shares": metric("share_count"),
        "reposts": metric("repost_count"),
        "saves": metric("save_count"),
        "replays": metric("replay_count"),
        "organic_impressions": metric("impression_organic_count"),
        "paid_impressions": metric("impression_paid_count"),
        "organic_reach": metric("reach_organic_count"),
        "paid_reach": metric("reach_paid_count"),
        "watch_time_hours": metric("watch_time_in_hours"),
        "average_watch_seconds": metric("avg_watch_time_in_sec"),
        "updated_at": content.get("updated_at"),
    }


def dump_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def dump_csv(path: Path, records: list[dict[str, Any]]) -> None:
    if not records:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def latest_copy(source: Path, destination: Path) -> None:
    shutil.copyfile(source, destination)


def collect(
    client: PhylloClient,
    *,
    output_root: Path,
    since: str,
    page_size: int,
    platforms: set[str],
) -> dict[str, Any]:
    collected_at = datetime.now(UTC)
    run_id = collected_at.strftime("%Y%m%dT%H%M%SZ")
    run_dir = output_root / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    accounts_payload = client.get("/v1/accounts", {"user_id": client.config.user_id})
    dump_json(run_dir / "accounts.json", accounts_payload)
    accounts = accounts_payload.get("data", [])
    selected_accounts = [
        account
        for account in accounts
        if isinstance(account, dict)
        and platform_name(account).lower() in platforms
        and str(account.get("status", "")).upper() == "CONNECTED"
    ]

    all_profiles: list[dict[str, Any]] = []
    all_contents: list[dict[str, Any]] = []
    platform_summaries: list[dict[str, Any]] = []

    for account in selected_accounts:
        account_id = str(account["id"])
        platform = platform_name(account)
        slug = platform.lower().replace(" ", "-")

        profiles, profile_pages = client.paginated(
            "/v1/profiles",
            {"account_id": account_id},
            page_size=page_size,
        )
        contents, content_pages = client.paginated(
            "/v1/social/contents",
            {"account_id": account_id, "from_date": since},
            page_size=page_size,
        )

        dump_json(run_dir / f"{slug}-profiles-raw.json", profile_pages)
        dump_json(run_dir / f"{slug}-contents-raw.json", content_pages)
        all_profiles.extend(normalize_profile(profile) for profile in profiles)
        all_contents.extend(normalize_content(content) for content in contents)
        platform_summaries.append(
            {
                "platform": platform,
                "account_id": account_id,
                "profiles": len(profiles),
                "content_items": len(contents),
            }
        )

    all_contents.sort(
        key=lambda item: str(item.get("published_at") or ""), reverse=True
    )
    all_profiles.sort(key=lambda item: str(item.get("platform") or ""))

    profiles_json = run_dir / "profiles.json"
    profiles_csv = run_dir / "profiles.csv"
    content_json = run_dir / "content.json"
    content_csv = run_dir / "content.csv"
    summary_json = run_dir / "summary.json"

    summary = {
        "collected_at": collected_at.isoformat(),
        "base_url": client.config.base_url,
        "since": since,
        "requested_platforms": sorted(platforms),
        "platforms": platform_summaries,
        "profile_records": len(all_profiles),
        "content_records": len(all_contents),
        "run_directory": str(run_dir),
    }

    dump_json(profiles_json, all_profiles)
    dump_csv(profiles_csv, all_profiles)
    dump_json(content_json, all_contents)
    dump_csv(content_csv, all_contents)
    dump_json(summary_json, summary)

    output_root.mkdir(parents=True, exist_ok=True)
    for source, name in (
        (profiles_json, "latest-profiles.json"),
        (profiles_csv, "latest-profiles.csv"),
        (content_json, "latest-content.json"),
        (content_csv, "latest-content.csv"),
        (summary_json, "latest-summary.json"),
    ):
        latest_copy(source, output_root / name)

    return summary


def command_sync(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    client = PhylloClient(
        config,
        delay_seconds=args.delay,
        retries=args.retries,
        timeout_seconds=args.timeout,
    )
    summary = collect(
        client,
        output_root=args.output,
        since=args.since,
        page_size=args.page_size,
        platforms=set(args.platform or SUPPORTED_PLATFORMS),
    )

    print(f"Phyllo sync completed: {summary['content_records']} content records")
    for platform in summary["platforms"]:
        print(
            f"  {platform['platform']}: "
            f"{platform['profiles']} profile, "
            f"{platform['content_items']} content items"
        )
    print(f"Latest files: {args.output.resolve()}")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(required=True)
    sync = commands.add_parser("sync", help="pull profile and content analytics")
    sync.add_argument("--config", type=Path, default=Path("phyllo.sh"))
    sync.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    sync.add_argument("--since", default=SERIES_START)
    sync.add_argument(
        "--platform",
        action="append",
        choices=sorted(SUPPORTED_PLATFORMS),
        help="collect only this platform; repeat to select multiple",
    )
    sync.add_argument("--page-size", type=int, default=50)
    sync.add_argument("--delay", type=float, default=2.0)
    sync.add_argument("--retries", type=int, default=4)
    sync.add_argument("--timeout", type=float, default=30.0)
    sync.set_defaults(handler=command_sync)
    return root


def main() -> None:
    args = parser().parse_args()
    try:
        args.handler(args)
    except PhylloError as error:
        print(f"phyllo-analytics: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
