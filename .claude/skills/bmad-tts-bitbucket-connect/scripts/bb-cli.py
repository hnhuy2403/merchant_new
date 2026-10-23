#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Lightweight Bitbucket REST API helper for the tts module.

Stdlib-only (urllib + json + base64) — runs anywhere Python 3.10+ exists,
zero external dependencies, no `uv` needed.

Supports BOTH Bitbucket flavors:

  cloud   — Bitbucket Cloud (api.bitbucket.org/2.0)
            Auth: Basic — `username:app-password` OR `x-token-auth:token`
            Reviewer ID: UUID in braces, e.g. {a1b2c3d4-...}
            Repo path: /repositories/{workspace}/{repo}/...

  server  — Bitbucket Server / Data Center (self-hosted, e.g. bitbucket.example.com)
            Auth: Bearer <http-access-token>
            Reviewer ID: username (e.g. "techlead")
            Repo path: /projects/{project_key}/repos/{repo}/...

Flavor is auto-detected from --api-base-url (or BB_API_BASE_URL env):
  contains "api.bitbucket.org" → cloud
  anything else                → server
Override explicitly with --api-flavor / BB_API_FLAVOR.

Subcommands:
  validate      Test auth + workspace/project access.
  user-lookup   Find a user (by nickname for Cloud, by query for Server).
  pr-list       List PRs for a repo. Filterable by source/dest branch + state.
                Outputs internal-vocab states (open / merged / closed_unmerged).
  pr-create     Create a new PR. Body comes from --body-file (markdown).
  pr-edit       Edit existing PR (body, title, reviewers).
  pr-comments   List review comments on a PR. Outputs normalized list with
                inline context (file, line) and resolution state.

Auth (provide via flags OR env vars):
  --auth-method app-password|access-token|bearer  (or $BB_AUTH_METHOD)
                Cloud uses 'app-password' or 'access-token'.
                Server uses 'bearer' (HTTP Access Token).
  --username <nick>                                (or $BB_USERNAME)         cloud/app-password
  --app-password <secret>                          (or $BB_APP_PASSWORD)     cloud/app-password
  --token <secret>                                 (or $BB_TOKEN)            cloud/access-token + server/bearer
  --workspace <slug or projectKey>                 (or $BB_WORKSPACE)        Cloud workspace, Server project key
  --repository <slug>                              (or $BB_REPOSITORY)
  --api-base-url <url>                             (or $BB_API_BASE_URL)
                Defaults to https://api.bitbucket.org/2.0 (Cloud).
                For Server: https://bitbucket.example.com (no /rest/api/...).
  --api-flavor cloud|server                        (or $BB_API_FLAVOR)
                Optional override; auto-detected from URL by default.

Output: JSON to stdout. Non-zero exit on auth failure or HTTP error;
the error JSON goes to stderr with the upstream Bitbucket payload preserved
so callers can surface it to the user.
"""

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

CLOUD_BASE = "https://api.bitbucket.org/2.0"


# ─── Flavor + URL helpers ───────────────────────────────────────────────────

def _resolve_api_base(args) -> str:
    return args.api_base_url or os.environ.get("BB_API_BASE_URL", "") or CLOUD_BASE


def _detect_flavor(api_base: str) -> str:
    """Return 'cloud' if the URL targets Bitbucket Cloud, else 'server'."""
    return "cloud" if "api.bitbucket.org" in api_base else "server"


def _resolve_flavor(args) -> str:
    explicit = (args.api_flavor or os.environ.get("BB_API_FLAVOR", "")).lower()
    if explicit in ("cloud", "server"):
        return explicit
    return _detect_flavor(_resolve_api_base(args))


def _server_rest_base(api_base: str) -> str:
    """Strip trailing slashes; the REST API lives at {host}/rest/api/1.0."""
    host = api_base.rstrip("/")
    if host.endswith("/rest/api/1.0"):
        return host
    return f"{host}/rest/api/1.0"


# ─── Auth ───────────────────────────────────────────────────────────────────

def _build_auth(args, flavor: str) -> str:
    method = (args.auth_method or os.environ.get("BB_AUTH_METHOD", "")).lower()
    token = args.token or os.environ.get("BB_TOKEN", "")

    if flavor == "server":
        # Bitbucket Server / DC always uses Bearer for HTTP Access Tokens.
        # If method is unset or 'bearer', proceed; if explicitly app-password, refuse.
        if method and method not in ("bearer", "access-token"):
            _die(f"Server flavor requires --auth-method=bearer (got: {method!r})")
        if not token:
            _die("Server flavor requires --token (or BB_TOKEN)")
        return f"Bearer {token}"

    # Cloud
    if method == "app-password":
        user = args.username or os.environ.get("BB_USERNAME", "")
        secret = args.app_password or os.environ.get("BB_APP_PASSWORD", "")
        if not user or not secret:
            _die("Cloud app-password requires --username and --app-password (or BB_USERNAME / BB_APP_PASSWORD)")
        creds = f"{user}:{secret}"
    elif method == "access-token":
        if not token:
            _die("Cloud access-token requires --token (or BB_TOKEN)")
        creds = f"x-token-auth:{token}"
    else:
        _die(f"Cloud --auth-method must be 'app-password' or 'access-token' (got: {method!r})")
    return "Basic " + base64.b64encode(creds.encode()).decode()


# ─── HTTP ───────────────────────────────────────────────────────────────────

def _http(method: str, url: str, args, flavor: str, body: dict | None = None) -> tuple[int, dict]:
    headers = {
        "Authorization": _build_auth(args, flavor),
        "Accept": "application/json",
        "User-Agent": "bmad-tts-bb-cli/1.1",
    }
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            return resp.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read() or b"{}")
        except json.JSONDecodeError:
            payload = {"error": "non-json response"}
        return e.code, payload
    except urllib.error.URLError as e:
        _die(f"Network error contacting Bitbucket: {e.reason}")


def _die(msg: str, code: int = 2) -> None:
    print(json.dumps({"status": "error", "message": msg}), file=sys.stderr)
    sys.exit(code)


def _emit_error(http_status: int, body: dict) -> None:
    print(json.dumps({"status": "error", "http_status": http_status, "body": body}), file=sys.stderr)


# ─── Pure helpers (PR shape normalization) ─────────────────────────────────

def _normalize_state(bb_state: str) -> str:
    """Cloud: OPEN/MERGED/DECLINED/SUPERSEDED · Server: OPEN/MERGED/DECLINED."""
    return {
        "OPEN": "open",
        "MERGED": "merged",
        "DECLINED": "closed_unmerged",
        "SUPERSEDED": "closed_unmerged",
    }.get(bb_state, "unknown")


def _summarize_participants_cloud(participants: list) -> dict:
    approvals = changes_requested = pending = 0
    for p in participants:
        if p.get("role") != "REVIEWER":
            continue
        if p.get("approved"):
            approvals += 1
        elif p.get("state") == "changes_requested":
            changes_requested += 1
        else:
            pending += 1
    return {"approvals": approvals, "changes_requested": changes_requested, "pending_reviewers": pending}


def _summarize_participants_server(reviewers: list) -> dict:
    """Server PR has top-level `reviewers[]`, each with `approved` (bool) + `status` enum
    (UNAPPROVED / APPROVED / NEEDS_WORK)."""
    approvals = changes_requested = pending = 0
    for r in reviewers:
        status = r.get("status", "")
        if r.get("approved") or status == "APPROVED":
            approvals += 1
        elif status == "NEEDS_WORK":
            changes_requested += 1
        else:
            pending += 1
    return {"approvals": approvals, "changes_requested": changes_requested, "pending_reviewers": pending}


def _slim_pr_cloud(pr: dict) -> dict:
    return {
        "id": pr.get("id"),
        "title": pr.get("title"),
        "state": _normalize_state(pr.get("state", "")),
        "raw_state": pr.get("state"),
        "merged_at": pr.get("updated_on") if pr.get("state") == "MERGED" else None,
        "url": pr.get("links", {}).get("html", {}).get("href"),
        "source_branch": pr.get("source", {}).get("branch", {}).get("name"),
        "destination_branch": pr.get("destination", {}).get("branch", {}).get("name"),
        "review_summary": _summarize_participants_cloud(pr.get("participants") or []),
    }


def _slim_pr_server(pr: dict) -> dict:
    """Server PR shape: fromRef/toRef.displayId, links.self[0].href, top-level reviewers[]."""
    self_links = pr.get("links", {}).get("self", [])
    url = self_links[0].get("href") if self_links else None
    raw_state = pr.get("state", "")
    return {
        "id": pr.get("id"),
        "title": pr.get("title"),
        "state": _normalize_state(raw_state),
        "raw_state": raw_state,
        # Server uses milliseconds-since-epoch in `closedDate` for merged/declined; expose as-is.
        "merged_at": pr.get("closedDate") if raw_state == "MERGED" else None,
        "url": url,
        "source_branch": pr.get("fromRef", {}).get("displayId"),
        "destination_branch": pr.get("toRef", {}).get("displayId"),
        "review_summary": _summarize_participants_server(pr.get("reviewers") or []),
    }


# Back-compat alias for tests + earlier callers.
def _slim_pr(pr: dict) -> dict:
    """Default to Cloud shape (back-compat). Prefer _slim_pr_cloud or _slim_pr_server."""
    return _slim_pr_cloud(pr)


def _summarize_participants(participants: list) -> dict:
    """Back-compat alias for tests + earlier callers (Cloud shape)."""
    return _summarize_participants_cloud(participants)


# ─── PR-create payload builders ─────────────────────────────────────────────

def _pr_create_payload_cloud(args, description: str, reviewer_ids: list) -> dict:
    payload = {
        "title": args.title,
        "description": description,
        "source": {"branch": {"name": args.source}},
        "destination": {"branch": {"name": args.dest}},
    }
    if reviewer_ids:
        payload["reviewers"] = [{"uuid": uid} for uid in reviewer_ids]
    if args.close_source_branch:
        payload["close_source_branch"] = True
    return payload


def _pr_create_payload_server(args, description: str, reviewer_names: list) -> dict:
    """Server requires fromRef/toRef with full repo+project context."""
    ws = args.workspace or os.environ.get("BB_WORKSPACE", "")
    repo = args.repository or os.environ.get("BB_REPOSITORY", "")
    repo_ref = {"slug": repo, "project": {"key": ws}}
    payload = {
        "title": args.title,
        "description": description,
        "fromRef": {"id": f"refs/heads/{args.source}", "repository": repo_ref},
        "toRef": {"id": f"refs/heads/{args.dest}", "repository": repo_ref},
        "state": "OPEN",
        "open": True,
        "closed": False,
    }
    if reviewer_names:
        payload["reviewers"] = [{"user": {"name": name}} for name in reviewer_names]
    return payload


# ─── Subcommands ────────────────────────────────────────────────────────────

def _resolve_ws_repo(args) -> tuple[str, str]:
    ws = args.workspace or os.environ.get("BB_WORKSPACE", "")
    repo = args.repository or os.environ.get("BB_REPOSITORY", "")
    if not ws or not repo:
        _die("--workspace and --repository required")
    return ws, repo


def cmd_validate(args) -> int:
    flavor = _resolve_flavor(args)
    api_base = _resolve_api_base(args)

    if flavor == "cloud":
        method = (args.auth_method or os.environ.get("BB_AUTH_METHOD", "")).lower()
        if method not in ("app-password", "access-token"):
            _die(f"Cloud --auth-method must be 'app-password' or 'access-token' (got: {method!r})")
        if method == "app-password":
            url = f"{api_base}/user"
        else:
            ws = args.workspace or os.environ.get("BB_WORKSPACE", "")
            if not ws:
                _die("--workspace required for Cloud access-token validation")
            url = f"{api_base}/workspaces/{ws}"
    else:  # server
        url = f"{_server_rest_base(api_base)}/users?limit=1"

    status, body = _http("GET", url, args, flavor)
    if 200 <= status < 300:
        if flavor == "cloud":
            identity = body.get("nickname") or body.get("display_name") or body.get("slug") or "(unknown)"
        else:
            users = body.get("values") or []
            identity = users[0].get("name") if users else "(probe-only)"
        print(json.dumps({"status": "ok", "flavor": flavor, "http_status": status, "identity": identity}))
        return 0
    _emit_error(status, body)
    return 1


def cmd_user_lookup(args) -> int:
    flavor = _resolve_flavor(args)
    api_base = _resolve_api_base(args)

    if flavor == "cloud":
        ws = args.workspace or os.environ.get("BB_WORKSPACE", "")
        if not ws:
            _die("--workspace required")
        q = urllib.parse.quote(f'user.nickname="{args.query}"')
        url = f"{api_base}/workspaces/{ws}/members?q={q}&pagelen=10"
        status, body = _http("GET", url, args, flavor)
        if status >= 300:
            _emit_error(status, body)
            return 1
        matches = []
        for m in body.get("values", []):
            u = m.get("user", {})
            matches.append({"id": u.get("uuid"), "nickname": u.get("nickname"), "display_name": u.get("display_name")})
    else:  # server
        # /users?filter= matches displayName/name/emailAddress
        params = urllib.parse.urlencode({"filter": args.query, "limit": 10})
        url = f"{_server_rest_base(api_base)}/users?{params}"
        status, body = _http("GET", url, args, flavor)
        if status >= 300:
            _emit_error(status, body)
            return 1
        matches = []
        for u in body.get("values", []):
            matches.append({"id": u.get("name"), "nickname": u.get("name"), "display_name": u.get("displayName")})

    print(json.dumps({"status": "ok", "flavor": flavor, "matches": matches}))
    return 0


def _pr_list_cloud(args, api_base: str, ws: str, repo: str) -> int:
    filters = []
    if args.source:
        filters.append(f'source.branch.name="{args.source}"')
    if args.dest:
        filters.append(f'destination.branch.name="{args.dest}"')
    params = {"pagelen": str(args.limit)}
    if filters:
        params["q"] = " AND ".join(filters)
    if args.state and args.state.lower() != "all":
        params["state"] = args.state.upper()
    url = f"{api_base}/repositories/{ws}/{repo}/pullrequests?{urllib.parse.urlencode(params)}"
    status, body = _http("GET", url, args, "cloud")
    if status >= 300:
        _emit_error(status, body)
        return 1
    prs = [_slim_pr_cloud(p) for p in body.get("values", [])]
    print(json.dumps({"status": "ok", "flavor": "cloud", "count": len(prs), "prs": prs}))
    return 0


def _pr_list_server(args, api_base: str, project_key: str, repo: str) -> int:
    """Server filters by `at` (= toRef branch). Source filtering is client-side."""
    params = {"limit": str(args.limit), "order": "NEWEST"}
    if args.state and args.state.lower() != "all":
        params["state"] = args.state.upper()
    else:
        params["state"] = "ALL"
    if args.dest:
        params["at"] = f"refs/heads/{args.dest}"
    url = f"{_server_rest_base(api_base)}/projects/{project_key}/repos/{repo}/pull-requests?{urllib.parse.urlencode(params)}"
    status, body = _http("GET", url, args, "server")
    if status >= 300:
        _emit_error(status, body)
        return 1
    prs = []
    for p in body.get("values", []):
        if args.source and p.get("fromRef", {}).get("displayId") != args.source:
            continue
        prs.append(_slim_pr_server(p))
    print(json.dumps({"status": "ok", "flavor": "server", "count": len(prs), "prs": prs}))
    return 0


def cmd_pr_list(args) -> int:
    flavor = _resolve_flavor(args)
    api_base = _resolve_api_base(args)
    ws, repo = _resolve_ws_repo(args)
    return _pr_list_cloud(args, api_base, ws, repo) if flavor == "cloud" else _pr_list_server(args, api_base, ws, repo)


def cmd_pr_create(args) -> int:
    flavor = _resolve_flavor(args)
    api_base = _resolve_api_base(args)
    ws, repo = _resolve_ws_repo(args)

    description = ""
    if args.body_file:
        with open(args.body_file, encoding="utf-8") as f:
            description = f.read()

    if flavor == "cloud":
        payload = _pr_create_payload_cloud(args, description, args.reviewer)
        url = f"{api_base}/repositories/{ws}/{repo}/pullrequests"
    else:
        payload = _pr_create_payload_server(args, description, args.reviewer)
        url = f"{_server_rest_base(api_base)}/projects/{ws}/repos/{repo}/pull-requests"

    status, body = _http("POST", url, args, flavor, body=payload)
    if status >= 300:
        _emit_error(status, body)
        return 1

    if flavor == "cloud":
        url_out = body.get("links", {}).get("html", {}).get("href")
    else:
        self_links = body.get("links", {}).get("self") or []
        url_out = self_links[0].get("href") if self_links else None

    print(json.dumps({"status": "ok", "flavor": flavor, "id": body.get("id"), "url": url_out}))
    return 0


def cmd_pr_edit(args) -> int:
    flavor = _resolve_flavor(args)
    api_base = _resolve_api_base(args)
    ws, repo = _resolve_ws_repo(args)

    description = None
    if args.body_file:
        with open(args.body_file, encoding="utf-8") as f:
            description = f.read()

    if flavor == "cloud":
        payload = {}
        if args.title:
            payload["title"] = args.title
        if description is not None:
            payload["description"] = description
        if args.reviewer:
            payload["reviewers"] = [{"uuid": uid} for uid in args.reviewer]
        if not payload:
            _die("pr-edit: nothing to update — pass --title, --body-file, or --reviewer")
        url = f"{api_base}/repositories/{ws}/{repo}/pullrequests/{args.pr_id}"
        status, body = _http("PUT", url, args, "cloud", body=payload)
    else:  # server
        # Server PUT requires the current `version` for optimistic locking — fetch first.
        get_url = f"{_server_rest_base(api_base)}/projects/{ws}/repos/{repo}/pull-requests/{args.pr_id}"
        gs, gb = _http("GET", get_url, args, "server")
        if gs >= 300:
            _emit_error(gs, gb)
            return 1
        payload = {"version": gb.get("version", 0)}
        if args.title:
            payload["title"] = args.title
        if description is not None:
            payload["description"] = description
        if args.reviewer:
            payload["reviewers"] = [{"user": {"name": name}} for name in args.reviewer]
        if len(payload) == 1:
            _die("pr-edit: nothing to update — pass --title, --body-file, or --reviewer")
        status, body = _http("PUT", get_url, args, "server", body=payload)

    if status >= 300:
        _emit_error(status, body)
        return 1

    if flavor == "cloud":
        url_out = body.get("links", {}).get("html", {}).get("href")
    else:
        self_links = body.get("links", {}).get("self") or []
        url_out = self_links[0].get("href") if self_links else None
    print(json.dumps({"status": "ok", "flavor": flavor, "id": body.get("id"), "url": url_out}))
    return 0


# ─── PR comments ────────────────────────────────────────────────────────────

def _slim_comment_cloud(c: dict) -> dict:
    inline = c.get("inline")
    return {
        "id": c.get("id"),
        "author": (c.get("author") or {}).get("nickname") or (c.get("author") or {}).get("display_name"),
        "body": (c.get("content") or {}).get("raw", ""),
        "created_at": c.get("created_on"),
        "updated_at": c.get("updated_on"),
        "inline": {
            "path": inline.get("path"),
            "line": inline.get("to") or inline.get("from"),
        } if inline else None,
        "deleted": c.get("deleted", False),
        "resolved": False,  # Cloud has no native resolve flag on comments
    }


def _slim_comment_server(c: dict) -> dict:
    inline = None
    anchor = c.get("anchor")
    if anchor and anchor.get("path"):
        inline = {
            "path": anchor.get("path"),
            "line": anchor.get("line"),
        }
    return {
        "id": c.get("id"),
        "author": (c.get("author") or {}).get("name") or (c.get("author") or {}).get("displayName"),
        "body": (c.get("text") or ""),
        "created_at": c.get("createdDate"),
        "updated_at": c.get("updatedDate"),
        "inline": inline,
        "deleted": c.get("severity") == "DELETED",
        "resolved": c.get("state") == "RESOLVED",
    }


def cmd_pr_comments(args) -> int:
    flavor = _resolve_flavor(args)
    api_base = _resolve_api_base(args)
    ws, repo = _resolve_ws_repo(args)
    pr_id = args.pr_id
    limit = args.limit

    if flavor == "cloud":
        url = f"{api_base}/repositories/{ws}/{repo}/pullrequests/{pr_id}/comments?pagelen={limit}"
        status, body = _http("GET", url, args, "cloud")
        if status >= 300:
            _emit_error(status, body)
            return 1
        raw = body.get("values", [])
        comments = [_slim_comment_cloud(c) for c in raw if not c.get("deleted")]
    else:
        url = f"{_server_rest_base(api_base)}/projects/{ws}/repos/{repo}/pull-requests/{pr_id}/comments?limit={limit}"
        status, body = _http("GET", url, args, "server")
        if status >= 300:
            _emit_error(status, body)
            return 1
        raw = body.get("values", [])
        comments = [_slim_comment_server(c) for c in raw if c.get("severity") != "DELETED"]

    if args.unresolved_only:
        comments = [c for c in comments if not c["resolved"]]

    print(json.dumps({
        "status": "ok",
        "flavor": flavor,
        "pr_id": pr_id,
        "count": len(comments),
        "comments": comments,
    }))
    return 0


# ─── Git remote auto-detect ────────────────────────────────────────────────

# Bitbucket Server clone URLs put the project key under `/scm/<key>/...`.
# Browse URLs use `/projects/<KEY>/repos/<slug>` (uppercase).
_BBS_SCM_RE = re.compile(r"^/scm/([^/]+)/(.+?)(?:\.git)?/?$", re.IGNORECASE)
_PLAIN_PATH_RE = re.compile(r"^/?([^/]+)/(.+?)(?:\.git)?/?$")
_SSH_SCP_RE = re.compile(r"^([^@]+)@([^:]+):(.+)$")


def _looks_like_bitbucket(host: str) -> bool:
    """Conservative heuristic: host == bitbucket.org (Cloud) OR contains
    'bitbucket' (typical for self-hosted: bitbucket.example.com, bb.corp).
    Use --force to bypass this check for self-hosted with non-obvious names
    (e.g., git.example.com hosting BBS)."""
    if not host:
        return False
    h = host.lower()
    return h == "bitbucket.org" or "bitbucket" in h


def _parse_git_remote(url: str, accept_any_host: bool = False) -> dict | None:
    """Parse a git remote URL into Bitbucket components.

    Supports:
      - Cloud HTTPS: https://bitbucket.org/<workspace>/<repo>[.git]
      - Cloud SSH:   git@bitbucket.org:<workspace>/<repo>[.git]
      - Server HTTP: http(s)://<host>/scm/<projectKey>/<repo>[.git]
      - Server SSH:  ssh://git@<host>[:port]/<projectKey>/<repo>[.git]
                     OR scp-style: git@<host>:<projectKey>/<repo>[.git]

    Returns dict with: host, scheme, flavor, workspace, repository, api_base_url
    or None if the URL doesn't look like Bitbucket / can't be parsed.

    By default rejects hosts that don't look like Bitbucket (github.com, etc.).
    Set `accept_any_host=True` to bypass this check (e.g., self-hosted BBS on
    a non-bitbucket-named host like git.example.com).
    """
    if not url:
        return None
    url = url.strip()

    host = None
    path = None
    scheme = None

    # SSH scp-style: user@host:path (no scheme)
    m = _SSH_SCP_RE.match(url)
    if m and "://" not in url:
        host = m.group(2)
        path = "/" + m.group(3)
        scheme = "ssh"
    else:
        try:
            parsed = urllib.parse.urlsplit(url)
        except ValueError:
            return None
        if not parsed.scheme or not parsed.netloc:
            return None
        scheme = parsed.scheme
        netloc = parsed.netloc
        if "@" in netloc:
            netloc = netloc.split("@", 1)[1]
        if ":" in netloc:
            netloc = netloc.split(":", 1)[0]
        host = netloc
        path = parsed.path

    if not host or not path:
        return None

    if not accept_any_host and not _looks_like_bitbucket(host):
        return None

    # Cloud detection is exact (only bitbucket.org), even when accept_any_host.
    flavor = "cloud" if host.lower() == "bitbucket.org" else "server"

    workspace = repository = None
    if flavor == "server":
        scm_match = _BBS_SCM_RE.match(path)
        if scm_match:
            workspace = scm_match.group(1).upper()
            repository = scm_match.group(2)
        else:
            plain = _PLAIN_PATH_RE.match(path)
            if plain:
                workspace = plain.group(1).upper()
                repository = plain.group(2)
    else:  # cloud
        plain = _PLAIN_PATH_RE.match(path)
        if plain:
            workspace = plain.group(1)
            repository = plain.group(2)

    if not workspace or not repository:
        return None

    if repository.endswith(".git"):
        repository = repository[:-4]

    if flavor == "cloud":
        api_base_url = CLOUD_BASE
    else:
        # Server: API lives at the same host. Default to https unless the
        # remote URL explicitly used http (we don't downgrade silently).
        api_scheme = "http" if scheme == "http" else "https"
        api_base_url = f"{api_scheme}://{host}"

    return {
        "host": host,
        "scheme": scheme,
        "flavor": flavor,
        "workspace": workspace,
        "repository": repository,
        "api_base_url": api_base_url,
    }


def cmd_detect_from_git(args) -> int:
    """Read `git remote get-url <name>` (default 'origin') and parse the URL."""
    if not shutil.which("git"):
        print(json.dumps({"status": "error", "found": False, "message": "git not found on PATH"}))
        return 1

    if args.url:
        remote_url = args.url
        source = f"--url override"
    else:
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", args.remote],
                capture_output=True, text=True, timeout=5, cwd=args.cwd or os.getcwd(),
            )
        except (subprocess.SubprocessError, OSError) as e:
            print(json.dumps({"status": "error", "found": False, "message": f"git invocation failed: {e}"}))
            return 1
        if result.returncode != 0:
            print(json.dumps({
                "status": "ok", "found": False,
                "message": f"No git remote '{args.remote}' (or not a git repo)",
                "stderr": result.stderr.strip(),
            }))
            return 0
        remote_url = result.stdout.strip()
        source = f"git remote ({args.remote})"

    parsed = _parse_git_remote(remote_url, accept_any_host=args.force)
    if not parsed:
        print(json.dumps({
            "status": "ok", "found": False,
            "message": f"Remote URL doesn't look like Bitbucket: {remote_url}. "
                       f"Pass --force to accept self-hosted BBS on a non-bitbucket-named host.",
            "remote_url": remote_url, "source": source,
        }))
        return 0

    print(json.dumps({
        "status": "ok", "found": True,
        "remote_url": remote_url, "source": source,
        **parsed,
    }))
    return 0


# ─── Argparse wiring ────────────────────────────────────────────────────────

def _add_common_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--auth-method", choices=["app-password", "access-token", "bearer"])
    p.add_argument("--username")
    p.add_argument("--app-password")
    p.add_argument("--token")
    p.add_argument("--workspace", help="Cloud workspace slug, or Server project key")
    p.add_argument("--repository")
    p.add_argument("--api-base-url", help=f"Default: {CLOUD_BASE} (Cloud). For Server: https://your-bb-host")
    p.add_argument("--api-flavor", choices=["cloud", "server"], help="Override auto-detection")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_v = sub.add_parser("validate", help="test auth + workspace/project access")
    _add_common_args(p_v)
    p_v.set_defaults(func=cmd_validate)

    p_u = sub.add_parser("user-lookup", help="look up a user")
    _add_common_args(p_u)
    p_u.add_argument("--query", required=True, help="nickname (Cloud) or filter string (Server)")
    p_u.set_defaults(func=cmd_user_lookup)

    p_l = sub.add_parser("pr-list", help="list PRs for a repo")
    _add_common_args(p_l)
    p_l.add_argument("--source", help="filter by source branch name")
    p_l.add_argument("--dest", help="filter by destination branch name")
    p_l.add_argument("--state", default="all", help="OPEN, MERGED, DECLINED, (Cloud also SUPERSEDED), or all")
    p_l.add_argument("--limit", type=int, default=20)
    p_l.set_defaults(func=cmd_pr_list)

    p_c = sub.add_parser("pr-create", help="create a PR")
    _add_common_args(p_c)
    p_c.add_argument("--title", required=True)
    p_c.add_argument("--source", required=True)
    p_c.add_argument("--dest", required=True)
    p_c.add_argument("--body-file", help="path to PR description (markdown)")
    p_c.add_argument("--reviewer", action="append", default=[],
                     help="reviewer ID (UUID for Cloud, username for Server). Repeatable.")
    p_c.add_argument("--close-source-branch", action="store_true", help="Cloud only")
    p_c.set_defaults(func=cmd_pr_create)

    p_e = sub.add_parser("pr-edit", help="edit existing PR")
    _add_common_args(p_e)
    p_e.add_argument("--pr-id", required=True)
    p_e.add_argument("--title")
    p_e.add_argument("--body-file")
    p_e.add_argument("--reviewer", action="append", default=[])
    p_e.set_defaults(func=cmd_pr_edit)

    p_cm = sub.add_parser("pr-comments", help="list review comments on a PR")
    _add_common_args(p_cm)
    p_cm.add_argument("--pr-id", required=True, help="PR numeric ID")
    p_cm.add_argument("--limit", type=int, default=100, help="max comments to fetch (default: 100)")
    p_cm.add_argument("--unresolved-only", action="store_true",
                      help="filter to unresolved comments only (Server: state != RESOLVED)")
    p_cm.set_defaults(func=cmd_pr_comments)

    # Auto-detect Bitbucket connection params from git remote.
    # No auth required — runs `git remote get-url` locally.
    p_g = sub.add_parser("detect-from-git",
                         help="parse `git remote get-url` to derive flavor/host/workspace/repository")
    p_g.add_argument("--remote", default="origin", help="remote name (default: origin)")
    p_g.add_argument("--url", help="parse this URL instead of running git (for testing)")
    p_g.add_argument("--cwd", help="git working directory (default: current)")
    p_g.add_argument("--force", action="store_true",
                     help="accept hosts not matching 'bitbucket' (for self-hosted BBS on custom domains)")
    p_g.set_defaults(func=cmd_detect_from_git)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
