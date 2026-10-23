#!/usr/bin/env python3
"""
sonar-cli.py — lightweight SonarQube REST API helper for the vds-tts-fix-sonar skill.

Credentials are taken from env vars (NEVER CLI args, to avoid leaking through
process lists):
  SONAR_HOST_URL      — e.g. http://sonar-10.digital.vn (no trailing slash)
  SONAR_TOKEN         — Sonar user token (prefix squ_ for SonarQube 9.x+)
  SONAR_PROJECT_KEY   — componentKeys for issue lookup (sub-commands that need it)

Sub-commands:
  validate           — call /api/authentication/validate to confirm token works
  issues             — list issues for project + branch with severity/rule filters
  rule               — fetch rule definition (title + html description)

All output is JSON to stdout. Exit codes:
  0 on success
  1 on argument/configuration error
  2 on HTTP error from Sonar (auth, 5xx, etc.)
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.parse
import urllib.request


def _resolve_creds(args) -> tuple[str, str]:
    host = os.environ.get("SONAR_HOST_URL", "").rstrip("/")
    token = os.environ.get("SONAR_TOKEN", "")
    if not host:
        _die_arg("SONAR_HOST_URL env var is required.")
    if not token:
        _die_arg("SONAR_TOKEN env var is required. Read from _bmad/config.user.yaml → tts.sonar.token.")
    return host, token


def _die_arg(msg: str) -> None:
    print(json.dumps({"status": "error", "kind": "config", "message": msg}), file=sys.stdout)
    sys.exit(1)


def _http_get(host: str, path: str, token: str, params: dict | None = None) -> tuple[int, dict | None, str]:
    url = host + path
    if params:
        # Drop None / empty values; keep zero/false
        clean = {k: v for k, v in params.items() if v is not None and v != ""}
        if clean:
            url += "?" + urllib.parse.urlencode(clean, doseq=True)
    # Sonar uses HTTP Basic with token as username (empty password)
    creds = f"{token}:".encode()
    auth = "Basic " + base64.b64encode(creds).decode()
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", auth)
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, _safe_json(body), body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return e.code, _safe_json(body), body
    except urllib.error.URLError as e:
        return 0, None, str(e)


def _safe_json(body: str) -> dict | None:
    if not body:
        return None
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return None


def _emit_http_error(status: int, body_obj: dict | None, body_raw: str) -> None:
    payload = {"status": "error", "kind": "http", "http_status": status}
    if body_obj is not None:
        payload["body"] = body_obj
    elif body_raw:
        payload["body_raw"] = body_raw[:500]
    print(json.dumps(payload))
    sys.exit(2)


# ── Sub-commands ──────────────────────────────────────────────────────────────


def cmd_validate(args) -> int:
    host, token = _resolve_creds(args)
    status, body, raw = _http_get(host, "/api/authentication/validate", token)
    if status >= 300:
        _emit_http_error(status, body, raw)
    valid = bool((body or {}).get("valid"))
    print(json.dumps({"status": "ok", "valid": valid}))
    return 0 if valid else 2


def cmd_issues(args) -> int:
    host, token = _resolve_creds(args)
    project = args.project_key or os.environ.get("SONAR_PROJECT_KEY", "")
    if not project:
        _die_arg("--project-key OR env SONAR_PROJECT_KEY is required.")

    params: dict = {
        "componentKeys": project,
        "branch": args.branch,
        "statuses": args.statuses,
        "severities": args.severities,
        "ps": min(args.max, 500),
        "p": 1,
        "resolved": "false",
        "facets": "severities,types,rules,files",
    }
    if args.rule:
        params["rules"] = args.rule
    if args.types:
        params["types"] = args.types

    # Paginate up to args.max
    all_issues: list[dict] = []
    facets: list[dict] = []
    total = 0
    page = 1
    while True:
        params["p"] = page
        status, body, raw = _http_get(host, "/api/issues/search", token, params)
        if status >= 300 or body is None:
            _emit_http_error(status, body, raw)
        if page == 1:
            total = body.get("total", 0)
            facets = body.get("facets", [])
        issues = body.get("issues", [])
        all_issues.extend(issues)
        if len(all_issues) >= args.max or not issues:
            break
        if page * params["ps"] >= total:
            break
        page += 1

    # Optionally filter by file substring (Sonar API doesn't support substring on component)
    if args.file:
        needle = args.file.lower()
        all_issues = [i for i in all_issues if needle in (i.get("component") or "").lower()]

    # Slim down each issue
    slim = [
        {
            "key": i.get("key"),
            "rule": i.get("rule"),
            "severity": i.get("severity"),
            "type": i.get("type"),
            "component": i.get("component"),
            "line": i.get("line"),
            "message": i.get("message"),
            "effort": i.get("effort"),
            "debt": i.get("debt"),
            "tags": i.get("tags", []),
            "status": i.get("status"),
        }
        for i in all_issues
    ]
    print(json.dumps({
        "status": "ok",
        "project_key": project,
        "branch": args.branch,
        "total_reported": total,
        "returned": len(slim),
        "facets": facets,
        "issues": slim,
    }))
    return 0


def cmd_rule(args) -> int:
    host, token = _resolve_creds(args)
    params = {"key": args.key, "actives": "true"}
    status, body, raw = _http_get(host, "/api/rules/show", token, params)
    if status >= 300 or body is None:
        _emit_http_error(status, body, raw)
    rule = body.get("rule", {})
    slim = {
        "key": rule.get("key"),
        "name": rule.get("name"),
        "severity": rule.get("severity"),
        "type": rule.get("type"),
        "lang": rule.get("lang"),
        "html_desc": rule.get("htmlDesc") or rule.get("htmlNote"),
        "md_desc": rule.get("mdDesc"),
        "tags": rule.get("tags", []),
        "remediation_function": rule.get("remFnType"),
        "remediation_effort": rule.get("remFnBaseEffort"),
    }
    print(json.dumps({"status": "ok", "rule": slim}))
    return 0


# ── Argparse ──────────────────────────────────────────────────────────────────


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sp_validate = sub.add_parser("validate", help="confirm token + host reachable")
    sp_validate.set_defaults(func=cmd_validate)

    sp_issues = sub.add_parser("issues", help="list issues for a project + branch")
    sp_issues.add_argument("--project-key", default=None, help="Sonar componentKeys (else use $SONAR_PROJECT_KEY)")
    sp_issues.add_argument("--branch", default="staging", help="branch name (default: staging)")
    sp_issues.add_argument("--severities", default="BLOCKER,CRITICAL,MAJOR",
                           help="comma-separated severities (default: BLOCKER,CRITICAL,MAJOR)")
    sp_issues.add_argument("--statuses", default="OPEN,REOPENED,CONFIRMED",
                           help="comma-separated statuses (default: OPEN,REOPENED,CONFIRMED)")
    sp_issues.add_argument("--types", default=None,
                           help="optional types filter, e.g. BUG,VULNERABILITY,CODE_SMELL,SECURITY_HOTSPOT")
    sp_issues.add_argument("--rule", default=None, help="filter to one rule key (e.g. java:S1192)")
    sp_issues.add_argument("--file", default=None, help="substring filter on file path")
    sp_issues.add_argument("--max", type=int, default=200, help="max issues to fetch (default 200)")
    sp_issues.set_defaults(func=cmd_issues)

    sp_rule = sub.add_parser("rule", help="fetch a Sonar rule definition")
    sp_rule.add_argument("--key", required=True, help="rule key, e.g. java:S2189")
    sp_rule.set_defaults(func=cmd_rule)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
