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
X_AUDIENCE_LATEST_PATH = X_PRIVATE_DIR / "audience-latest.json"
X_AUDIENCE_SNAPSHOTS_DIR = X_PRIVATE_DIR / "audience-snapshots"
REDIRECT_URI = "http://127.0.0.1:8765/callback"
SCOPES = "tweet.read tweet.write users.read offline.access"
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
TIKTOK_CONFIG_DIR = Path.home() / ".config" / "dlatwd" / "tiktok-analytics"
TIKTOK_CLIENT_PATH = TIKTOK_CONFIG_DIR / "client.json"
TIKTOK_TOKEN_PATH = TIKTOK_CONFIG_DIR / "token.json"
TIKTOK_PENDING_AUTH_PATH = TIKTOK_CONFIG_DIR / "pending-auth.json"
TIKTOK_PRIVATE_DIR = (
    REPOSITORY_ROOT / "youtube-series" / "analytics" / "private" / "tiktok"
)
TIKTOK_LATEST_PATH = TIKTOK_PRIVATE_DIR / "latest.json"
TIKTOK_SNAPSHOTS_DIR = TIKTOK_PRIVATE_DIR / "snapshots"
# TikTok's app console may reject a loopback redirect URI outright (unlike X,
# which allows it for public clients). Try this first; if TikTok's console
# won't accept it, register a redirect URI you do control instead and use
# `tiktok-auth --code` with the value TikTok appends to that URL.
TIKTOK_REDIRECT_URI = "http://127.0.0.1:8766/callback"
TIKTOK_SCOPES = "user.info.basic,video.list"
TIKTOK_VIDEO_FIELDS = (
    "id,create_time,share_url,video_description,duration,cover_image_url,"
    "view_count,like_count,comment_count,share_count"
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


def command_x_audience_sync(_args: argparse.Namespace) -> int:
    """Collect only owned-account profile and follower metrics from X."""
    account = x_get(
        "/2/users/me",
        {"user.fields": "id,name,username,description,url,public_metrics"},
    )["data"]
    captured_at = int(time.time())
    snapshot = {"captured_at": captured_at, "account": account}
    X_AUDIENCE_SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%dT%H-%M-%SZ", time.gmtime(captured_at))
    write_private_json(X_AUDIENCE_SNAPSHOTS_DIR / f"{timestamp}.json", snapshot)
    write_private_json(X_AUDIENCE_LATEST_PATH, snapshot)
    followers = account.get("public_metrics", {}).get("followers_count")
    print(f"Collected X follower count for @{account['username']}: {followers}")
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


def x_post(path: str, body: dict[str, Any]) -> dict[str, Any]:
    request = Request(
        f"https://api.x.com{path}",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"X write failed ({error.code}): {detail}") from error


def account_replies(parent_post_id: str) -> list[dict[str, Any]]:
    me = x_get("/2/users/me", {"user.fields": "id,username"})["data"]
    result = x_get(
        f"/2/users/{me['id']}/tweets",
        {
            "start_time": X_COLLECTION_START,
            "max_results": "100",
            "tweet.fields": "id,text,created_at,conversation_id,referenced_tweets",
        },
    )
    return [
        post
        for post in result.get("data", [])
        if post.get("id") != parent_post_id
        and post.get("conversation_id") == parent_post_id
    ]


def command_x_reply(args: argparse.Namespace) -> int:
    parent_post_id = args.in_reply_to.strip()
    if not parent_post_id.isdecimal():
        raise RuntimeError("The parent X post ID must contain only digits")

    text = Path(args.text_file).read_text(encoding="utf-8").strip()
    if not text:
        raise RuntimeError("The reply text file is empty")

    print(f"Reply target: https://x.com/i/status/{parent_post_id}")
    print()
    print(text)
    print()

    if not args.apply:
        print("Dry run only. Re-run with --apply to publish this reply.")
        return 0

    existing = account_replies(parent_post_id)
    if existing:
        print("Refusing to create another account-authored reply.")
        for post in existing:
            print(f"  https://x.com/i/status/{post['id']}")
            print(f"  {post.get('text', '').strip()}")
        return 2

    result = x_post(
        "/2/tweets",
        {
            "text": text,
            "reply": {"in_reply_to_tweet_id": parent_post_id},
        },
    )["data"]
    me = x_get("/2/users/me", {"user.fields": "username"})["data"]
    print(f"Published: https://x.com/{me['username']}/status/{result['id']}")
    return 0


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
    write_private_json(
        X_AUDIENCE_LATEST_PATH,
        {"captured_at": captured_at, "account": me},
    )
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


def tiktok_client() -> tuple[str, str]:
    if TIKTOK_CLIENT_PATH.exists():
        stored = json.loads(TIKTOK_CLIENT_PATH.read_text(encoding="utf-8"))
        return stored["client_key"], stored["client_secret"]
    client_key = input("TikTok Client Key: ").strip()
    if not client_key:
        raise RuntimeError("Client Key cannot be empty")
    client_secret = getpass.getpass("TikTok Client Secret: ").strip()
    if not client_secret:
        raise RuntimeError("Client Secret cannot be empty")
    write_private_json(
        TIKTOK_CLIENT_PATH,
        {"client_key": client_key, "client_secret": client_secret},
    )
    return client_key, client_secret


class TikTokCallbackHandler(BaseHTTPRequestHandler):
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
            message = "TikTok authorization complete. You may close this tab."
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))
        threading.Thread(target=self.server.shutdown, daemon=True).start()

    def log_message(self, _format: str, *_args: object) -> None:
        return


def tiktok_exchange_code(
    client_key: str, client_secret: str, code: str, verifier: str
) -> dict[str, Any]:
    body = urlencode(
        {
            "client_key": client_key,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": TIKTOK_REDIRECT_URI,
            "code_verifier": verifier,
        }
    ).encode("utf-8")
    request = Request(
        "https://open.tiktokapis.com/v2/oauth/token/",
        data=body,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            result = json.load(response)
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"TikTok token exchange failed ({error.code}): {detail}"
        ) from error
    if "access_token" not in result:
        raise RuntimeError(f"TikTok token exchange did not return a token: {result}")
    result["acquired_at"] = int(time.time())
    return result


def command_tiktok_auth(args: argparse.Namespace) -> int:
    client_key, client_secret = tiktok_client()

    if args.code:
        if not TIKTOK_PENDING_AUTH_PATH.exists():
            raise RuntimeError(
                "No pending TikTok authorization found; run `tiktok-auth` "
                "(without --code) first to generate one"
            )
        pending = json.loads(TIKTOK_PENDING_AUTH_PATH.read_text(encoding="utf-8"))
        token = tiktok_exchange_code(
            client_key, client_secret, args.code, pending["verifier"]
        )
        write_private_json(TIKTOK_TOKEN_PATH, token)
        TIKTOK_PENDING_AUTH_PATH.unlink(missing_ok=True)
        print(f"Authorization stored securely at {TIKTOK_TOKEN_PATH}")
        return 0

    verifier, challenge = pkce_pair()
    state = secrets.token_urlsafe(32)
    write_private_json(TIKTOK_PENDING_AUTH_PATH, {"verifier": verifier, "state": state})
    parameters = urlencode(
        {
            "client_key": client_key,
            "response_type": "code",
            "scope": TIKTOK_SCOPES,
            "redirect_uri": TIKTOK_REDIRECT_URI,
            "state": state,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        }
    )
    url = f"https://www.tiktok.com/v2/auth/authorize/?{parameters}"
    print("Opening TikTok authorization in your browser...")
    print(url)
    print()
    print(
        "If the browser redirects successfully to "
        f"{TIKTOK_REDIRECT_URI}, this command will finish automatically."
    )
    print(
        "If TikTok rejects that redirect URI at authorization time, "
        "register a redirect URI you control in the TikTok developer "
        "console instead, open the URL above manually, and once TikTok "
        "redirects there, rerun this command with "
        "`tiktok-auth --code <the code= value from that URL>`."
    )

    TikTokCallbackHandler.expected_state = state
    TikTokCallbackHandler.result = {}
    webbrowser.open(url)
    server = HTTPServer(("127.0.0.1", 8766), TikTokCallbackHandler)
    server.timeout = 300
    server.handle_request()
    code = TikTokCallbackHandler.result.get("code")
    if not code:
        error = TikTokCallbackHandler.result.get("error")
        if error:
            raise RuntimeError(error)
        print(
            "No callback received within 5 minutes. The pending "
            f"authorization is saved at {TIKTOK_PENDING_AUTH_PATH} — "
            "once you have a code, rerun with `tiktok-auth --code ...`."
        )
        return 1
    token = tiktok_exchange_code(client_key, client_secret, code, verifier)
    write_private_json(TIKTOK_TOKEN_PATH, token)
    TIKTOK_PENDING_AUTH_PATH.unlink(missing_ok=True)
    print(f"Authorization stored securely at {TIKTOK_TOKEN_PATH}")
    return 0


def tiktok_refresh_access_token(token: dict[str, Any]) -> dict[str, Any]:
    client_key, client_secret = tiktok_client()
    refresh_token = token.get("refresh_token")
    if not refresh_token:
        raise RuntimeError("TikTok token cannot refresh; run `make tiktok-auth` again")
    body = urlencode(
        {
            "client_key": client_key,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
    ).encode("utf-8")
    request = Request(
        "https://open.tiktokapis.com/v2/oauth/token/",
        data=body,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            result = json.load(response)
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"TikTok token refresh failed ({error.code}): {detail}"
        ) from error
    result["acquired_at"] = int(time.time())
    if "refresh_token" not in result:
        result["refresh_token"] = refresh_token
    write_private_json(TIKTOK_TOKEN_PATH, result)
    return result


def tiktok_access_token() -> str:
    if not TIKTOK_TOKEN_PATH.exists():
        raise RuntimeError("TikTok is not authorized; run `make tiktok-auth` first")
    token = json.loads(TIKTOK_TOKEN_PATH.read_text(encoding="utf-8"))
    acquired_at = token.get("acquired_at")
    expires_in = token.get("expires_in", 86400)
    if acquired_at is None:
        token["acquired_at"] = int(time.time())
        write_private_json(TIKTOK_TOKEN_PATH, token)
    elif time.time() >= acquired_at + expires_in - 300:
        token = tiktok_refresh_access_token(token)
    return token["access_token"]


def tiktok_get(path: str, parameters: dict[str, str]) -> dict[str, Any]:
    url = f"https://open.tiktokapis.com{path}?{urlencode(parameters)}"
    request = Request(
        url, headers={"Authorization": f"Bearer {tiktok_access_token()}"}
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"TikTok request failed ({error.code}): {detail}") from error


def tiktok_post(
    path: str, query: dict[str, str], body: dict[str, Any]
) -> dict[str, Any]:
    url = f"https://open.tiktokapis.com{path}?{urlencode(query)}"
    request = Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {tiktok_access_token()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"TikTok request failed ({error.code}): {detail}") from error


def command_tiktok_test(_args: argparse.Namespace) -> int:
    result = tiktok_get(
        "/v2/user/info/",
        {"fields": "open_id,display_name,follower_count,video_count,likes_count"},
    )
    data = result.get("data", {}).get("user", {})
    if not data:
        raise RuntimeError(f"Unexpected TikTok response: {result}")
    print(f"Authorized TikTok account: {data.get('display_name')}")
    print(json.dumps(data, indent=2))
    return 0


def command_tiktok_sync(_args: argparse.Namespace) -> int:
    user = tiktok_get(
        "/v2/user/info/",
        {"fields": "open_id,display_name,follower_count,video_count,likes_count"},
    ).get("data", {}).get("user", {})

    videos: list[dict[str, Any]] = []
    cursor = 0
    while True:
        page = tiktok_post(
            "/v2/video/list/",
            {"fields": TIKTOK_VIDEO_FIELDS},
            {"max_count": 20, "cursor": cursor} if cursor else {"max_count": 20},
        )
        data = page.get("data", {})
        videos.extend(data.get("videos", []))
        if not data.get("has_more"):
            break
        cursor = data.get("cursor", 0)
        if not cursor:
            break

    captured_at = int(time.time())
    snapshot = {"captured_at": captured_at, "account": user, "videos": videos}
    TIKTOK_SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%dT%H-%M-%SZ", time.gmtime(captured_at))
    write_private_json(TIKTOK_SNAPSHOTS_DIR / f"{timestamp}.json", snapshot)
    write_private_json(TIKTOK_LATEST_PATH, snapshot)
    print(f"Collected {len(videos)} TikTok videos for {user.get('display_name')}.")
    for video in videos:
        print(
            f"  {video.get('share_url')} views={video.get('view_count')} "
            f"likes={video.get('like_count')} comments={video.get('comment_count')} "
            f"shares={video.get('share_count')}"
        )
    print(f"Latest snapshot: {TIKTOK_LATEST_PATH}")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Local social analytics collector")
    commands = root.add_subparsers(required=True)
    x_auth = commands.add_parser("x-auth", help="Authorize owned-account X analytics")
    x_auth.set_defaults(handler=command_x_auth)
    x_test = commands.add_parser("x-test", help="Verify the authorized X account")
    x_test.set_defaults(handler=command_x_test)
    x_audience_sync = commands.add_parser(
        "x-audience-sync", help="Collect only X profile and follower metrics"
    )
    x_audience_sync.set_defaults(handler=command_x_audience_sync)
    x_sync = commands.add_parser(
        "x-sync", help="Explicitly collect series-era X posts and their metrics"
    )
    x_sync.set_defaults(handler=command_x_sync)
    x_reply = commands.add_parser(
        "x-reply", help="Preview or publish a reply from a UTF-8 text file"
    )
    x_reply.add_argument(
        "--in-reply-to", required=True, help="Numeric ID of the parent X post"
    )
    x_reply.add_argument(
        "--text-file", required=True, help="Path to a UTF-8 file containing the reply"
    )
    x_reply.add_argument(
        "--apply",
        action="store_true",
        help="Publish after checking for an existing account-authored reply",
    )
    x_reply.set_defaults(handler=command_x_reply)
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
    tiktok_auth = commands.add_parser(
        "tiktok-auth", help="Authorize owned-account TikTok analytics"
    )
    tiktok_auth.add_argument(
        "--code",
        default=None,
        help=(
            "Complete a pending authorization using a code manually copied "
            "from a redirect TikTok sent to a URL other than the loopback "
            "default (see `tiktok-auth` output for when this is needed)."
        ),
    )
    tiktok_auth.set_defaults(handler=command_tiktok_auth)
    tiktok_test = commands.add_parser(
        "tiktok-test", help="Verify the authorized TikTok account"
    )
    tiktok_test.set_defaults(handler=command_tiktok_test)
    tiktok_sync = commands.add_parser(
        "tiktok-sync", help="Collect owned TikTok videos and their stats"
    )
    tiktok_sync.set_defaults(handler=command_tiktok_sync)
    return root


def main() -> None:
    args = parser().parse_args()
    raise SystemExit(args.handler(args))


if __name__ == "__main__":
    main()
