#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Copy bundled template files into a project, mirroring directory structure.

Walks --source (default: assets/templates/ relative to skill root), and for
each regular file under it, copies to the matching path under --target
(default: the BMad project root). Directory layout under --source is
mirrored verbatim — drop new files into assets/templates/ and they get
picked up on the next run, no script changes required.

Default behavior is SAFE: existing destination files are skipped (never
silently overwritten). Use --overwrite to force replacement of every file,
or --overwrite-glob PATTERN (repeatable) to force only files whose path
matches a glob — useful for "authoritative" subtrees like `.claude/rules/`
that should always track the git source of truth while leaving starter
files like `.claude/claude.md` untouched.

Use --only-glob PATTERN (repeatable) to RESTRICT the copy to just the files
matching it — every other template is ignored entirely. Combined with the
matching --overwrite-glob, this drives the focused "update rules" flow that
refreshes only `.claude/rules/*` and leaves the rest of the project alone.

Output: JSON to stdout summarizing what was copied, skipped, or errored.
Exit code 0 on success (even if files were skipped); non-zero only for
unrecoverable errors (missing source dir, permission failures, etc.).

Examples:
  # Dry-run from skill root, target = project-root two dirs up:
  python3 scripts/copy-templates.py \\
    --source assets/templates \\
    --target /path/to/project \\
    --dry-run

  # Force overwrite (used during reconfiguration):
  python3 scripts/copy-templates.py \\
    --source assets/templates \\
    --target /path/to/project \\
    --overwrite

  # Always overwrite authoritative subtrees, skip-existing for the rest:
  python3 scripts/copy-templates.py \\
    --source assets/templates \\
    --target /path/to/project \\
    --overwrite-glob '.claude/rules/*'
"""

import argparse
import fnmatch
import json
import shutil
import sys
from pathlib import Path


def _walk_files(root: Path) -> list[Path]:
    """All regular files under root, sorted for deterministic output."""
    return sorted([p for p in root.rglob("*") if p.is_file()])


def _matches_any_glob(rel: str, patterns: list[str]) -> bool:
    """fnmatch-based glob match. `*` matches across separators (good enough for our cases)."""
    if not patterns:
        return False
    norm = rel.replace("\\", "/")
    for pat in patterns:
        normalized_pat = pat.replace("\\", "/").replace("**", "*")
        if fnmatch.fnmatch(norm, normalized_pat):
            return True
    return False


def copy_templates(
    source: Path,
    target: Path,
    overwrite: bool,
    dry_run: bool,
    overwrite_globs: list[str] | None = None,
    only_globs: list[str] | None = None,
) -> dict:
    """Mirror every file under `source` into `target`. Pure dict-out for tests.

    When `only_globs` is non-empty, files whose source-relative path does NOT
    match any of the patterns are ignored entirely (not copied, not reported as
    skipped) — used by the focused "update rules" flow to touch only
    `.claude/rules/*` and leave every other template alone.
    """
    if not source.exists() or not source.is_dir():
        return {
            "status": "error",
            "message": f"Source directory does not exist: {source}",
            "copied": [], "skipped": [], "errors": [],
        }

    overwrite_globs = overwrite_globs or []
    only_globs = only_globs or []
    copied: list[dict] = []
    skipped: list[dict] = []
    errors: list[dict] = []

    for src_path in _walk_files(source):
        rel = src_path.relative_to(source)
        dest_path = target / rel
        rel_str = str(rel)

        if only_globs and not _matches_any_glob(rel_str, only_globs):
            continue

        glob_authoritative = _matches_any_glob(rel_str, overwrite_globs)
        effective_overwrite = overwrite or glob_authoritative

        if dest_path.exists() and not effective_overwrite:
            skipped.append({
                "source": rel_str,
                "destination": str(dest_path),
                "reason": "destination already exists (pass --overwrite or --overwrite-glob to replace)",
            })
            continue

        existed_before = dest_path.exists()
        if dry_run:
            copied.append({
                "source": rel_str,
                "destination": str(dest_path),
                "action": "would-overwrite" if existed_before else "would-create",
                "via": "overwrite-glob" if glob_authoritative and not overwrite else
                       ("overwrite-flag" if overwrite else "new"),
            })
            continue

        try:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dest_path)
            copied.append({
                "source": rel_str,
                "destination": str(dest_path),
                "action": "overwrote" if existed_before else "created",
                "via": "overwrite-glob" if glob_authoritative and not overwrite else
                       ("overwrite-flag" if overwrite else "new"),
            })
        except OSError as e:
            errors.append({
                "source": rel_str,
                "destination": str(dest_path),
                "error": str(e),
            })

    return {
        "status": "ok" if not errors else "partial",
        "source": str(source),
        "target": str(target),
        "dry_run": dry_run,
        "overwrite": overwrite,
        "overwrite_globs": overwrite_globs,
        "only_globs": only_globs,
        "copied": copied,
        "skipped": skipped,
        "errors": errors,
        "summary": {
            "copied_count": len(copied),
            "skipped_count": len(skipped),
            "error_count": len(errors),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--source", required=True, help="Source dir (e.g. assets/templates)")
    parser.add_argument("--target", required=True, help="Target dir (project root)")
    parser.add_argument("--overwrite", action="store_true", help="Replace every existing destination file")
    parser.add_argument("--overwrite-glob", action="append", default=[], metavar="PATTERN",
                        help="Force-overwrite files whose relative path matches PATTERN (fnmatch glob). "
                             "Repeatable. Example: --overwrite-glob '.claude/rules/*'")
    parser.add_argument("--only-glob", action="append", default=[], metavar="PATTERN",
                        help="Restrict the copy to ONLY files whose relative path matches PATTERN "
                             "(fnmatch glob). Repeatable. Everything else is ignored entirely. "
                             "Example (rules-only refresh): --only-glob '.claude/rules/*'")
    parser.add_argument("--dry-run", action="store_true", help="Report only, no writes")
    args = parser.parse_args()

    result = copy_templates(
        source=Path(args.source).resolve(),
        target=Path(args.target).resolve(),
        overwrite=args.overwrite,
        dry_run=args.dry_run,
        overwrite_globs=args.overwrite_glob,
        only_globs=args.only_glob,
    )
    print(json.dumps(result, indent=2))
    return 0 if result["status"] != "error" else 1


if __name__ == "__main__":
    sys.exit(main())
