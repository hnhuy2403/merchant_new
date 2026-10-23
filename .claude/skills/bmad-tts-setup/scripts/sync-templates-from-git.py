#!/usr/bin/env python3
"""
sync-templates-from-git.py — refresh this skill's assets/templates/ tree from
the authoritative git repo (source of truth).

Background: `npx bmad-method install` has been observed to skip the
`assets/templates/` directory, leaving it empty at the skill destination.
This script pulls the directory directly from the git repo so that the
subsequent `copy-templates.py` step has fresh content to copy into the project.

Auth: Bitbucket Server bearer token. Resolved from (highest priority first):
  --token CLI arg, $BITBUCKET_TOKEN env var, or `tts.bitbucket.token` in
  the user's `_bmad/config.user.yaml`.

Outputs a JSON summary to stdout. Exits non-zero on hard errors.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

DEFAULT_REPO_URL = "http://bitbucket.digital.vn/scm/vss/tts-shared-bmad.git"
DEFAULT_BRANCH = "master"
DEFAULT_SOURCE_PATH = "skills/bmad-tts-setup/assets/templates"
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_TARGET_DIR = SCRIPT_DIR.parent / "assets" / "templates"


def load_token(token_arg: str | None, config_user_path: str | None):
    if token_arg:
        return token_arg, "arg"
    env_token = os.environ.get("BITBUCKET_TOKEN")
    if env_token:
        return env_token, "env"
    if not config_user_path:
        return None, None
    p = Path(config_user_path)
    if not p.exists():
        return None, None
    if yaml is None:
        return None, "yaml-module-missing"
    try:
        cfg = yaml.safe_load(p.read_text()) or {}
    except yaml.YAMLError:
        return None, "config-parse-error"
    token = (((cfg.get("tts") or {}).get("bitbucket") or {})).get("token")
    if token:
        return token, f"config:{p}"
    return None, None


def redact(s: str, token: str) -> str:
    if not token:
        return s
    return s.replace(token, "***")


def run_git_clone(repo_url: str, branch: str, dest: Path, token: str) -> subprocess.CompletedProcess:
    cmd = [
        "git",
        "-c", f"http.extraHeader=Authorization: Bearer {token}",
        "clone", "--depth", "1", "--single-branch",
        "--branch", branch, repo_url, str(dest),
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def overwrite_sync(src: Path, dst: Path) -> list[str]:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    return [str(f.relative_to(dst)) for f in dst.rglob("*") if f.is_file()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo-url", default=DEFAULT_REPO_URL,
                    help=f"git URL of source repo (default: {DEFAULT_REPO_URL})")
    ap.add_argument("--branch", default=DEFAULT_BRANCH,
                    help=f"branch / tag to clone (default: {DEFAULT_BRANCH})")
    ap.add_argument("--source-path", default=DEFAULT_SOURCE_PATH,
                    help=f"path within repo to sync from (default: {DEFAULT_SOURCE_PATH})")
    ap.add_argument("--target-dir", default=str(DEFAULT_TARGET_DIR),
                    help=f"local directory to overwrite (default: {DEFAULT_TARGET_DIR})")
    ap.add_argument("--token", default=None, help="bitbucket bearer token (overrides env / config)")
    ap.add_argument("--config-user", default=None,
                    help="path to _bmad/config.user.yaml for token fallback")
    args = ap.parse_args()

    token, token_source = load_token(args.token, args.config_user)
    if not token:
        print(json.dumps({
            "status": "error",
            "error": ("No bitbucket token found. Pass --token, set $BITBUCKET_TOKEN, "
                      "or run /bmad-tts-bitbucket-connect to populate config.user.yaml."),
            "token_source": token_source,
        }, indent=2))
        return 2

    if shutil.which("git") is None:
        print(json.dumps({"status": "error", "error": "git CLI not found on PATH"}, indent=2))
        return 2

    with tempfile.TemporaryDirectory(prefix="bmad-tts-sync-") as td:
        clone_dest = Path(td) / "repo"
        result = run_git_clone(args.repo_url, args.branch, clone_dest, token)
        if result.returncode != 0:
            print(json.dumps({
                "status": "error",
                "error": "git clone failed",
                "stderr": redact(result.stderr.strip(), token),
                "returncode": result.returncode,
            }, indent=2))
            return 2

        src = clone_dest / args.source_path
        if not src.exists():
            print(json.dumps({
                "status": "error",
                "error": f"source path not found in repo: {args.source_path}",
                "branch": args.branch,
            }, indent=2))
            return 2

        target = Path(args.target_dir).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        files = overwrite_sync(src, target)

        print(json.dumps({
            "status": "ok",
            "repo_url": args.repo_url,
            "branch": args.branch,
            "source_path": args.source_path,
            "target_dir": str(target),
            "token_source": token_source,
            "files_synced_count": len(files),
            "files": files,
        }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
