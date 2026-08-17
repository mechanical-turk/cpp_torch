from __future__ import annotations

import argparse
import base64
import getpass
import hashlib
import json
import secrets
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen


CONFIG_DIR = Path.home() / ".config" / "dlatwd" / "x-analytics"
CLIENT_PATH = CONFIG_DIR / "client.json"
TOKEN_PATH = CONFIG_DIR / "token.json"
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
X_PRIVATE_DIR = REPOSITORY_ROOT / "youtube-series" / "analytics" / "private" / "x"
X_LATEST_PATH = X_PRIVATE_DIR / "latest.json"
X_SNAPSHOTS_DIR = X_PRIVATE_DIR / "snapshots"
REDIRECT_URI = "http://127.0.0.1:8765/callback"
SCOPES = "tweet.read users.read offline.access"
X_COLLECTION_START = "2026-08-13T13:10:00Z"
INSTAGRAM_CONFIG_DIR = Path.home() / ".config" / "dlatwd" / "instagram-analytics"
INSTAGRAM_TOKEN_PATH = INSTAGRAM_CONFIG_DIR / "token.json"
INSTAGRAM_PRIVATE_DIR = (
    REPOSITORY_ROOT / "youtube-series" / "analytics" / "private" / "instagram"
)
INSTAGRAM_LATEST_PATH = INSTAGRAM_PRIVATE_DIR / "latest.json"
INSTAGRAM_SNAPSHOTS_DIR = INSTAGRAM_PRIVATE_DIR / "snapshots"
INSTAGRAM_REEL_INSIGHT_METRICS = (
    "views,reach,total_interactions,likes,comments,saved,shares,"
    "ig_reels_avg_watch_time,ig_reels_video_view_total_time"
)


def base64url(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def pkce_pair() -> tuple[str, str]:
    verifier = base64url(secrets.token_bytes(64))
    challenge = base64url(hashlib.sha256(verifier.encode("ascii")).digest())
    return verifier, challenge


def write_private_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    path.chmod(0o600)


def client_id() -> str:
    if CLIENT_PATH.exists():
        return json.loads(CLIENT_PATH.read_text(encoding="utf-8"))["client_id"]
    value = input("X OAuth 2.0 Client ID: ").strip()
    if not value:
        raise RuntimeError("Client ID cannot be empty")
    write_private_json(CLIENT_PATH, {"client_id": value})
    return value


class CallbackHandler(BaseHTTPRequestHandler):
    result: dict[str, str] = {}
    expected_state = ""

    def do_GET(self) -> None:  # noqa: N802
        query = parse_qs(urlparse(self.path).query)
        if query.get("state", [""])[0] != self.expected_state:
            self.send_response(400)
            message = "Authorization failed: state mismatch."
            type(self).result = {"error": message}
        elif "error" in query:
            self.send_response(400)
            description = query.get("error_description", [""])[0]
            message = f"Authorization denied: {query['error'][0]}"
            if description:
                message += f" ({description})"
            type(self).result = {"error": message}
        else:
            type(self).result = {"code": query.get("code", [""])[0]}
            self.send_response(200)
            message = "X authorization complete. You may close this tab."
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))
        threading.Thread(target=self.server.shutdown, daemon=True).start()

    def log_message(self, _format: str, *_args: object) -> None:
        return


def exchange_code(client: str, code: str, verifier: str) -> dict[str, Any]:
    body = urlencode(
        {
            "code": code,
            "grant_type": "authorization_code",
            "client_id": client,
            "redirect_uri": REDIRECT_URI,
            "code_verifier": verifier,
        }
    ).encode("utf-8")
    request = Request(
        "https://api.x.com/2/oauth2/token",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            result = json.load(response)
            result["acquired_at"] = int(time.time())
            return result
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"X token exchange failed ({error.code}): {detail}") from error


def command_x_auth(_args: argparse.Namespace) -> int:
    client = client_id()
    verifier, challenge = pkce_pair()
    state = secrets.token_urlsafe(32)
    CallbackHandler.expected_state = state
    CallbackHandler.result = {}
    parameters = urlencode(
        {
            "response_type": "code",
            "client_id": client,
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPES,
            "state": state,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        }
    )
    url = f"https://x.com/i/oauth2/authorize?{parameters}"
    server = HTTPServer(("127.0.0.1", 8765), CallbackHandler)
    print("Opening X authorization in your browser...")
    print(url)
    webbrowser.open(url)
    server.serve_forever()
    code = CallbackHandler.result.get("code")
    if not code:
        raise RuntimeError(
            CallbackHandler.result.get(
                "error", "X did not return an authorization code"
            )
        )
    token = exchange_code(client, code, verifier)
    write_private_json(TOKEN_PATH, token)
    print(f"Authorization stored securely at {TOKEN_PATH}")
    return 0


def command_x_test(_args: argparse.Namespace) -> int:
    token = access_token()
    request = Request(
        "https://api.x.com/2/users/me?user.fields=id,name,username,public_metrics",
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        with urlopen(request, timeout=30) as response:
            result = json.load(response)["data"]
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"X identity check failed ({error.code}): {detail}") from error
    print(f"Authorized X account: @{result['username']} ({result['name']})")
    print(json.dumps(result.get("public_metrics", {}), indent=2))
    return 0


def refresh_access_token(token: dict[str, Any]) -> dict[str, Any]:
    refresh_token = token.get("refresh_token")
    if not refresh_token:
        raise RuntimeError("X token cannot refresh; run `make x-auth` again")
    body = urlencode(
        {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "client_id": client_id(),
        }
    ).encode("utf-8")
    request = Request(
        "https://api.x.com/2/oauth2/token",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            result = json.load(response)
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"X token refresh failed ({error.code}): {detail}") from error
    result["acquired_at"] = int(time.time())
    if "refresh_token" not in result:
        result["refresh_token"] = refresh_token
    write_private_json(TOKEN_PATH, result)
    return result


def access_token() -> str:
    if not TOKEN_PATH.exists():
        raise RuntimeError("X is not authorized; run `make x-auth` first")
    token = json.loads(TOKEN_PATH.read_text(encoding="utf-8"))
    acquired_at = token.get("acquired_at")
    expires_in = token.get("expires_in", 7200)
    if acquired_at is None:
        token["acquired_at"] = int(time.time())
        write_private_json(TOKEN_PATH, token)
    elif time.time() >= acquired_at + expires_in - 300:
        token = refresh_access_token(token)
    return token["access_token"]


def x_get(path: str, parameters: dict[str, str]) -> dict[str, Any]:
    url = f"https://api.x.com{path}?{urlencode(parameters)}"
    request = Request(url, headers={"Authorization": f"Bearer {access_token()}"})
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        if error.code == 402 and "credits depleted" in detail:
            raise RuntimeError(
                "X authentication succeeded, but the app has no API credits. "
                "Add prepaid credits in the X Developer Console, then rerun "
                "`make x-analytics-sync`."
            ) from error
        raise RuntimeError(f"X request failed ({error.code}): {detail}") from error


def command_x_sync(_args: argparse.Namespace) -> int:
    me = x_get(
        "/2/users/me",
        {"user.fields": "id,name,username,description,url,public_metrics"},
    )["data"]
    posts: list[dict[str, Any]] = []
    includes: list[dict[str, Any]] = []
    pagination_token: str | None = None
    while True:
        parameters = {
            # Series analytics begin at 9:10 AM ET on August 13, 2026.
            # Never expand this boundary backward without explicit approval:
            # X charges per resource read.
            "start_time": X_COLLECTION_START,
            "max_results": "100",
            "tweet.fields": (
                "id,text,created_at,conversation_id,referenced_tweets,attachments,"
                "public_metrics,non_public_metrics,organic_metrics"
            ),
            "expansions": "attachments.media_keys",
            "media.fields": (
                "media_key,type,duration_ms,height,width,"
                "public_metrics,non_public_metrics,organic_metrics"
            ),
        }
        if pagination_token:
            parameters["pagination_token"] = pagination_token
        page = x_get(f"/2/users/{me['id']}/tweets", parameters)
        posts.extend(page.get("data", []))
        includes.extend(page.get("includes", {}).get("media", []))
        pagination_token = page.get("meta", {}).get("next_token")
        if not pagination_token:
            break
    captured_at = int(time.time())
    snapshot = {
        "captured_at": captured_at,
        "account": me,
        "posts": posts,
        "media": includes,
    }
    X_SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%dT%H-%M-%SZ", time.gmtime(captured_at))
    snapshot_path = X_SNAPSHOTS_DIR / f"{timestamp}.json"
    write_private_json(snapshot_path, snapshot)
    write_private_json(X_LATEST_PATH, snapshot)
    print(f"Collected {len(posts)} X posts since the series launch.")
    print(f"Latest snapshot: {X_LATEST_PATH}")
    return 0


def instagram_access_token() -> str:
    if not INSTAGRAM_TOKEN_PATH.exists():
        raise RuntimeError(
            "Instagram is not authorized; run `make instagram-import-token` first"
        )
    return json.loads(INSTAGRAM_TOKEN_PATH.read_text(encoding="utf-8"))["access_token"]


def instagram_get(path: str, parameters: dict[str, str]) -> dict[str, Any]:
    query = dict(parameters)
    query["access_token"] = instagram_access_token()
    url = f"https://graph.instagram.com{path}?{urlencode(query)}"
    request = Request(url)
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Instagram request failed ({error.code}): {detail}"
        ) from error


def command_instagram_import_token(_args: argparse.Namespace) -> int:
    token = getpass.getpass("Instagram access token: ").strip()
    if not token:
        raise RuntimeError("Instagram access token cannot be empty")
    write_private_json(
        INSTAGRAM_TOKEN_PATH,
        {"access_token": token, "acquired_at": int(time.time())},
    )
    print(f"Instagram authorization stored securely at {INSTAGRAM_TOKEN_PATH}")
    return 0


def command_instagram_test(_args: argparse.Namespace) -> int:
    account = instagram_get(
        "/me",
        {
            "fields": (
                "user_id,username,name,account_type,media_count,followers_count,"
                "follows_count"
            )
        },
    )
    print(f"Authorized Instagram account: @{account['username']}")
    print(json.dumps(account, indent=2))
    return 0


def command_instagram_sync(_args: argparse.Namespace) -> int:
    account = instagram_get(
        "/me",
        {
            "fields": (
                "user_id,username,name,account_type,media_count,followers_count,"
                "follows_count"
            )
        },
    )
    media = instagram_get(
        "/me/media",
        {
            "fields": (
                "id,caption,media_type,media_product_type,permalink,timestamp,"
                "like_count,comments_count,thumbnail_url"
            )
        },
    ).get("data", [])
    for item in media:
        if item.get("media_product_type") != "REELS":
            continue
        result = instagram_get(
            f"/{item['id']}/insights",
            {"metric": INSTAGRAM_REEL_INSIGHT_METRICS},
        )
        item["insights"] = {
            metric["name"]: metric.get("values", [{}])[0].get("value")
            for metric in result.get("data", [])
        }
    captured_at = int(time.time())
    snapshot = {
        "captured_at": captured_at,
        "account": account,
        "media": media,
    }
    INSTAGRAM_SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%dT%H-%M-%SZ", time.gmtime(captured_at))
    snapshot_path = INSTAGRAM_SNAPSHOTS_DIR / f"{timestamp}.json"
    write_private_json(snapshot_path, snapshot)
    write_private_json(INSTAGRAM_LATEST_PATH, snapshot)
    print(f"Collected {len(media)} Instagram media items for @{account['username']}.")
    for item in media:
        if "insights" not in item:
            continue
        insights = item["insights"]
        average_ms = insights.get("ig_reels_avg_watch_time")
        average = f"{average_ms / 1000:.2f}s" if average_ms is not None else "n/a"
        print(
            f"  {item['permalink']} views={insights.get('views')} "
            f"reach={insights.get('reach')} avg_watch={average} "
            f"interactions={insights.get('total_interactions')}"
        )
    print(f"Latest snapshot: {INSTAGRAM_LATEST_PATH}")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Local social analytics collector")
    commands = root.add_subparsers(required=True)
    x_auth = commands.add_parser("x-auth", help="Authorize owned-account X analytics")
    x_auth.set_defaults(handler=command_x_auth)
    x_test = commands.add_parser("x-test", help="Verify the authorized X account")
    x_test.set_defaults(handler=command_x_test)
    x_sync = commands.add_parser("x-sync", help="Collect series-era owned X posts")
    x_sync.set_defaults(handler=command_x_sync)
    instagram_import = commands.add_parser(
        "instagram-import-token", help="Securely import an Instagram access token"
    )
    instagram_import.set_defaults(handler=command_instagram_import_token)
    instagram_test = commands.add_parser(
        "instagram-test", help="Verify the authorized Instagram account"
    )
    instagram_test.set_defaults(handler=command_instagram_test)
    instagram_sync = commands.add_parser(
        "instagram-sync", help="Collect owned Instagram media and Reel insights"
    )
    instagram_sync.set_defaults(handler=command_instagram_sync)
    return root


def main() -> None:
    args = parser().parse_args()
    raise SystemExit(args.handler(args))


if __name__ == "__main__":
    main()
