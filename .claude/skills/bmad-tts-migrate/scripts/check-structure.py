#!/usr/bin/env python3
"""
TTS Project Structure Checker

Deterministic checks on story folder layout, file naming, sprint-status
consistency, and module config. Outputs a JSON findings report to stdout.

Exit codes: 0 = success (findings may still exist), 1 = fatal error
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


# ---------------------------------------------------------------------------
# Severity constants
# ---------------------------------------------------------------------------
ERROR = "error"      # Must be fixed — blocks workflow
WARNING = "warning"  # Should be fixed — may cause issues
INFO = "info"        # Nice to fix — convention drift


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_yaml(path: Path):
    if yaml is None:
        return None, "pyyaml not installed — install with: pip install pyyaml"
    if not path.exists():
        return None, f"File not found: {path}"
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f), None
    except Exception as e:
        return None, str(e)


def story_key_from_folder(name: str) -> bool:
    """Return True if the folder name matches story key pattern N-N-slug."""
    return bool(re.match(r"^\d+-\d+-.+", name))


def parse_status_from_story(story_md: Path) -> str | None:
    """Extract 'Status: <value>' from the second line area of story.md."""
    try:
        text = story_md.read_text(encoding="utf-8")
        m = re.search(r"^Status:\s*(\S+)", text, re.MULTILINE)
        return m.group(1).strip() if m else None
    except Exception:
        return None


def detect_srs_file(story_dir: Path, story_key: str):
    """Return (canonical_path, old_path|None) for the SRS file in a story dir."""
    canonical = story_dir / "srs.md"
    old_name_pattern = re.compile(r"^srs-.+\.md$", re.IGNORECASE)
    old_files = [f for f in story_dir.iterdir()
                 if f.is_file() and old_name_pattern.match(f.name) and f.name != "srs.md"]
    return canonical, old_files[0] if old_files else None


def detect_design_doc(impl_dir: Path, story_key: str):
    """Return path of design doc — checks story folder first, then root (legacy)."""
    in_folder = impl_dir / story_key / "detail-design.md"
    if in_folder.exists():
        return in_folder
    legacy = impl_dir / f"{story_key}-design.md"
    return legacy if legacy.exists() else None


def check_story_md_sections(story_md: Path) -> list:
    """Check required sections in story.md, return list of finding dicts."""
    findings = []
    try:
        text = story_md.read_text(encoding="utf-8")
    except Exception as e:
        return [{"code": "story-unreadable", "severity": ERROR, "message": f"Cannot read story.md: {e}"}]

    required_sections = {
        "## Story": "story-section-missing",
        "## Acceptance Criteria": "ac-section-missing",
        "## Tasks / Subtasks": "tasks-section-missing",
        "## Dev Notes": "dev-notes-section-missing",
        "## Dev Agent Record": "dev-agent-record-missing",
        "### File List": "file-list-missing",
    }
    for heading, code in required_sections.items():
        if heading not in text:
            findings.append({
                "code": code,
                "severity": WARNING,
                "message": f"Missing section '{heading}' in story.md",
            })

    # Template placeholder check
    placeholders = [
        ("[Add acceptance criteria", "ac-placeholder-unfilled"),
        ("{{role}}", "story-placeholder-unfilled"),
        ("{{action}}", "story-placeholder-unfilled"),
        ("Relevant architecture patterns and constraints", "dev-notes-placeholder"),
    ]
    seen_codes = set()
    for placeholder, code in placeholders:
        if placeholder in text and code not in seen_codes:
            findings.append({
                "code": code,
                "severity": ERROR,
                "message": f"Template placeholder not filled: '{placeholder}'",
            })
            seen_codes.add(code)

    # AC items check — need at least one numbered AC
    ac_match = re.search(r"## Acceptance Criteria\s*\n(.*?)(?=\n##|\Z)", text, re.DOTALL)
    if ac_match:
        ac_body = ac_match.group(1)
        ac_items = re.findall(r"^\d+\.", ac_body, re.MULTILINE)
        if not ac_items:
            findings.append({
                "code": "ac-no-items",
                "severity": ERROR,
                "message": "Acceptance Criteria section has no numbered items",
            })
        else:
            # Check tasks reference AC numbers
            tasks_match = re.search(r"## Tasks / Subtasks\s*\n(.*?)(?=\n##|\Z)", text, re.DOTALL)
            if tasks_match:
                tasks_body = tasks_match.group(1)
                has_ac_ref = bool(re.search(r"\(AC:", tasks_body))
                if not has_ac_ref:
                    findings.append({
                        "code": "tasks-no-ac-refs",
                        "severity": WARNING,
                        "message": "Tasks/Subtasks have no '(AC: ...)' references — hard to trace coverage",
                    })

    # "As a ... I want ... so that" check
    story_match = re.search(r"## Story\s*\n(.*?)(?=\n##|\Z)", text, re.DOTALL)
    if story_match:
        story_body = story_match.group(1).strip()
        if not story_body or not re.search(r"As a .+,?\s*\n", story_body, re.IGNORECASE):
            findings.append({
                "code": "story-format-invalid",
                "severity": WARNING,
                "message": "Story section doesn't follow 'As a / I want / so that' format",
            })

    # Status check
    status = parse_status_from_story(story_md)
    valid_statuses = {
        "backlog", "ready-for-dev", "designed", "in-progress",
        "done", "cancelled", "blocked",
    }
    if status is None:
        findings.append({"code": "status-missing", "severity": ERROR, "message": "story.md has no 'Status:' field"})
    elif status.lower() not in valid_statuses:
        findings.append({
            "code": "status-invalid",
            "severity": WARNING,
            "message": f"story.md Status '{status}' not in expected set: {sorted(valid_statuses)}",
        })

    # Design doc reference when status=designed
    if status and status.lower() == "designed":
        if "design.md" not in text and "detail-design" not in text and "-design.md" not in text:
            findings.append({
                "code": "designed-no-design-ref",
                "severity": WARNING,
                "message": "Status=designed but no design doc reference found in Dev Notes",
            })
        if "srs" not in text.lower():
            findings.append({
                "code": "designed-no-srs-ref",
                "severity": WARNING,
                "message": "Status=designed but no SRS reference found in Dev Notes",
            })

    # SRS path reference — check it points to canonical srs.md, not old naming
    srs_refs = re.findall(r"srs[-_a-z0-9./ ]*\.md", text, re.IGNORECASE)
    for ref in srs_refs:
        if re.match(r"srs-\w+", ref):
            findings.append({
                "code": "story-srs-ref-old-naming",
                "severity": WARNING,
                "message": f"Dev Notes references old SRS path '{ref}' — should point to 'srs.md'",
            })
            break

    return findings


def check_srs_sections(srs_path: Path) -> list:
    """Check required sections in srs.md (supports both KBNV and BDD formats)."""
    findings = []
    try:
        text = srs_path.read_text(encoding="utf-8")
    except Exception as e:
        return [{"code": "srs-unreadable", "severity": ERROR, "message": f"Cannot read srs file: {e}"}]

    # Detect format: KBNV (has "Kịch bản nghiệp vụ" or "Luồng nghiệp vụ")
    #                BDD  (has "Bối cảnh nghiệp vụ" or "Happy-path")
    is_kbnv = bool(re.search(r"Luồng nghiệp vụ|kịch bản nghiệp vụ|KBNV|Activity diagram", text, re.IGNORECASE))
    is_bdd = bool(re.search(r"Bối cảnh nghiệp vụ|H#|E#|R#|Happy.path scenario", text, re.IGNORECASE))

    if is_kbnv:
        # KBNV-style required sections
        required = [
            ("Mô tả chung", "srs-missing-mo-ta-chung"),
            ("Luồng nghiệp vụ", "srs-missing-luong-nghiep-vu"),
            ("Business rules", "srs-missing-business-rules"),
            ("Tiêu chí nghiệm thu", "srs-missing-tieu-chi-nghiem-thu"),
        ]
    elif is_bdd:
        # BDD-style required sections (srs-template.md)
        required = [
            ("Bối cảnh nghiệp vụ", "srs-missing-boi-canh"),
            ("Đối tượng người dùng", "srs-missing-personas"),
            ("Phạm vi", "srs-missing-pham-vi"),
            ("Acceptance Criterion\\|AC-", "srs-missing-acs"),
        ]
    else:
        # Unknown format — minimal checks
        findings.append({
            "code": "srs-format-unknown",
            "severity": INFO,
            "message": "Could not detect SRS format (KBNV or BDD). Applying minimal checks.",
        })
        required = []

    for pattern, code in required:
        if not re.search(pattern, text, re.IGNORECASE):
            findings.append({
                "code": code,
                "severity": WARNING,
                "message": f"SRS missing section matching '{pattern}'",
            })

    # Universal checks — apply to any format
    # Unfilled placeholders
    todos = re.findall(r"\[CẦN BỔ SUNG[^\]]*\]|\[TODO[^\]]*\]", text)
    if todos:
        findings.append({
            "code": "srs-has-unfilled-todos",
            "severity": WARNING,
            "message": f"SRS has {len(todos)} unfilled placeholder(s): {todos[:3]}{'...' if len(todos) > 3 else ''}",
        })

    # Business rules check
    br_count = len(re.findall(r"BR-\d+[-.]?\d*", text))
    if br_count == 0:
        findings.append({
            "code": "srs-no-business-rules",
            "severity": WARNING,
            "message": "No business rules (BR-N) found in SRS",
        })

    # Error codes check
    has_error_codes = bool(re.search(r"(CAT|ADM|ERR|ERR-|mã lỗi)", text, re.IGNORECASE))
    if not has_error_codes:
        findings.append({
            "code": "srs-no-error-codes",
            "severity": INFO,
            "message": "No error codes section detected in SRS",
        })

    # Template variable not substituted
    unsubstituted = re.findall(r"\{\{[a-z_]+\}\}", text)
    if unsubstituted:
        findings.append({
            "code": "srs-template-vars-unsubstituted",
            "severity": ERROR,
            "message": f"SRS still has template variables: {unsubstituted[:5]}",
        })

    return findings


def check_design_doc_sections(design_path: Path) -> list:
    """Check required sections in detail-design.md."""
    findings = []
    try:
        text = design_path.read_text(encoding="utf-8")
    except Exception as e:
        return [{"code": "design-unreadable", "severity": ERROR, "message": f"Cannot read design doc: {e}"}]

    required_sections = {
        "Component Breakdown": "design-missing-component-breakdown",
        "Data Model": "design-missing-data-model",
        "API Contract": "design-missing-api-contracts",
        "Test Plan": "design-missing-test-plan",
    }
    for pattern, code in required_sections.items():
        if not re.search(pattern, text, re.IGNORECASE):
            findings.append({
                "code": code,
                "severity": WARNING,
                "message": f"Design doc missing section '{pattern}'",
            })

    # Status field check
    status_match = re.search(r"Status[:|]\s*(\S+)", text)
    if not status_match:
        findings.append({
            "code": "design-no-status",
            "severity": WARNING,
            "message": "Design doc has no Status field",
        })
    else:
        valid_design_statuses = {"draft", "self-reviewed", "approved"}
        ds = status_match.group(1).lower().strip(".,")
        if ds not in valid_design_statuses:
            findings.append({
                "code": "design-invalid-status",
                "severity": WARNING,
                "message": f"Design doc Status '{ds}' not in {valid_design_statuses}",
            })

    # File Changes table check
    if not re.search(r"File Changes|File List|path.*NEW.*UPDATE", text, re.IGNORECASE):
        findings.append({
            "code": "design-no-file-changes",
            "severity": INFO,
            "message": "Design doc has no File Changes table",
        })

    # Sequence diagrams check
    if "```mermaid" not in text and "sequenceDiagram" not in text:
        findings.append({
            "code": "design-no-sequence-diagram",
            "severity": INFO,
            "message": "Design doc has no Mermaid sequence diagram",
        })

    # Unsubstituted template vars
    unsubstituted = re.findall(r"\{\{[a-z_]+\}\}", text)
    if unsubstituted:
        findings.append({
            "code": "design-template-vars",
            "severity": ERROR,
            "message": f"Design doc has unsubstituted template variables: {unsubstituted[:5]}",
        })

    return findings


# ---------------------------------------------------------------------------
# Main check
# ---------------------------------------------------------------------------

def run_checks(impl_dir: Path, planning_dir: Path, bmad_dir: Path, story_filter: str | None) -> dict:
    findings = []
    summary = {
        "errors": 0,
        "warnings": 0,
        "infos": 0,
    }
    stories_report = []

    def add(finding: dict, story_key: str | None = None):
        finding.setdefault("story_key", story_key)
        findings.append(finding)
        summary[finding["severity"] + "s"] += 1

    # ── Config checks ──────────────────────────────────────────────────────
    config_yaml = bmad_dir / "config.yaml"
    config_toml = bmad_dir / "config.toml"
    if not config_yaml.exists() and not config_toml.exists():
        add({"code": "config-missing", "severity": ERROR,
             "message": "Neither _bmad/config.yaml nor _bmad/config.toml found"})
    elif not config_yaml.exists() and config_toml.exists():
        add({"code": "config-toml-only", "severity": WARNING,
             "message": "_bmad/config.yaml missing — skills expecting YAML config will fall back or fail. Run bmad-tts-setup to create it."})

    # Old-format directories
    for old_dir in ["bmm", "core", "tea", "bmb"]:
        if (bmad_dir / old_dir).is_dir():
            add({"code": "old-module-dir-exists", "severity": WARNING,
                 "message": f"_bmad/{old_dir}/ still exists (old installer format). Run bmad-tts-setup to migrate and clean up."})

    # module-help.csv
    if not (bmad_dir / "module-help.csv").exists():
        add({"code": "module-help-missing", "severity": WARNING,
             "message": "_bmad/module-help.csv not found — help system won't show TTS capabilities"})

    # ── Sprint-status ──────────────────────────────────────────────────────
    sprint_status_path = impl_dir / "sprint-status.yaml"
    sprint_data = {}
    sprint_keys = set()
    if not sprint_status_path.exists():
        add({"code": "sprint-status-missing", "severity": WARNING,
             "message": "sprint-status.yaml not found in implementation_artifacts — auto-discovery will fail"})
    else:
        sprint_data, err = load_yaml(sprint_status_path)
        if err:
            add({"code": "sprint-status-invalid", "severity": ERROR,
                 "message": f"sprint-status.yaml parse error: {err}"})
            sprint_data = {}
        else:
            dev_status = sprint_data.get("development_status", {}) if sprint_data else {}
            sprint_keys = {k for k in dev_status if re.match(r"^\d+-\d+-.+", k)}

    # ── Story folders scan ─────────────────────────────────────────────────
    folder_keys = set()
    if impl_dir.exists():
        for entry in impl_dir.iterdir():
            if entry.is_dir() and story_key_from_folder(entry.name):
                folder_keys.add(entry.name)

    # Apply filter
    keys_to_check = folder_keys
    if story_filter:
        keys_to_check = {k for k in folder_keys if k.startswith(story_filter)}
        if not keys_to_check:
            # Maybe filter matches sprint key prefix
            keys_to_check = {k for k in folder_keys if story_filter in k}

    # Orphan checks
    for key in sprint_keys - folder_keys:
        add({"code": "sprint-orphan-no-folder", "severity": WARNING,
             "message": f"sprint-status has story '{key}' but no matching folder found",
             "story_key": key})

    for key in folder_keys - sprint_keys:
        if not story_filter or story_filter in key:
            add({"code": "folder-orphan-not-in-sprint", "severity": INFO,
                 "message": f"Folder '{key}' exists but has no matching sprint-status entry",
                 "story_key": key})

    # ── Per-story checks ───────────────────────────────────────────────────
    for story_key in sorted(keys_to_check):
        story_dir = impl_dir / story_key
        story_findings = []

        # ---- story.md ----
        story_md = story_dir / "story.md"
        if not story_md.exists():
            story_findings.append({
                "code": "story-md-missing",
                "severity": ERROR,
                "message": "story.md not found — required by design-story, create-srs, and dev-story workflows",
            })
        else:
            story_findings.extend(check_story_md_sections(story_md))

        # ---- srs.md naming ----
        srs_canonical, srs_old = detect_srs_file(story_dir, story_key)
        has_srs = srs_canonical.exists()
        if not has_srs and srs_old:
            story_findings.append({
                "code": "srs-naming-old",
                "severity": ERROR,
                "message": f"SRS named '{srs_old.name}' — must be 'srs.md'. Auto-fixable with 'fix' mode.",
                "fix": {"action": "rename", "from": str(srs_old), "to": str(srs_canonical)},
            })
        elif not has_srs and not srs_old:
            story_findings.append({
                "code": "srs-missing",
                "severity": WARNING,
                "message": "srs.md not found — run /bmad-tts-create-srs to generate",
            })

        # ---- srs content ----
        srs_to_check = srs_canonical if has_srs else (srs_old if srs_old else None)
        if srs_to_check and srs_to_check.exists():
            story_findings.extend(check_srs_sections(srs_to_check))

        # ---- design doc ----
        design_doc = detect_design_doc(impl_dir, story_key)
        story_status = parse_status_from_story(story_md) if story_md.exists() else None
        sprint_status_val = (sprint_data or {}).get("development_status", {}).get(story_key)

        if story_status and story_status.lower() in {"designed", "in-progress", "done"}:
            if design_doc is None:
                story_findings.append({
                    "code": "design-doc-missing",
                    "severity": WARNING,
                    "message": f"story Status='{story_status}' but design doc not found at expected path '{impl_dir}/{story_key}/detail-design.md'",
                })
            else:
                story_findings.extend(check_design_doc_sections(design_doc))

        # ---- status consistency ----
        if sprint_status_val and story_status:
            if sprint_status_val.lower() != story_status.lower():
                story_findings.append({
                    "code": "status-mismatch",
                    "severity": WARNING,
                    "message": f"Status mismatch: story.md='{story_status}' vs sprint-status='{sprint_status_val}'",
                    "fix": {"action": "update-sprint-status", "story_key": story_key, "correct_value": story_status},
                })

        # ---- source-code-links.md ----
        links_file = story_dir / "source-code-links.md"
        if not links_file.exists():
            story_findings.append({
                "code": "source-code-links-missing",
                "severity": INFO,
                "message": "source-code-links.md not found (created by bmad-tts-create-story — may be intentionally absent for older stories)",
            })

        # Tag all story findings with story_key
        for f in story_findings:
            f["story_key"] = story_key
            summary[f["severity"] + "s"] += 1
        findings.extend(story_findings)
        stories_report.append({
            "story_key": story_key,
            "story_status": story_status,
            "sprint_status": sprint_status_val,
            "has_story_md": story_md.exists(),
            "has_srs": has_srs or (srs_old is not None),
            "srs_naming_ok": has_srs,
            "has_design_doc": design_doc is not None,
            "findings_count": len(story_findings),
        })

    # ── Planning artifacts ─────────────────────────────────────────────────
    for required_file in ["epics.md"]:
        found = list(planning_dir.rglob(required_file)) if planning_dir.exists() else []
        if not found:
            add({"code": f"planning-{required_file.replace('.','')}-missing", "severity": WARNING,
                 "message": f"'{required_file}' not found under planning_artifacts — create-story cannot load epics"})

    return {
        "summary": summary,
        "total_stories_checked": len(keys_to_check),
        "stories": stories_report,
        "findings": findings,
    }


# ---------------------------------------------------------------------------
# Apply auto-fixes
# ---------------------------------------------------------------------------

def apply_auto_fixes(findings: list, dry_run: bool) -> list:
    """Apply fix actions embedded in findings. Returns list of fix results."""
    results = []
    for f in findings:
        fix = f.get("fix")
        if not fix:
            continue
        action = fix.get("action")
        if action == "rename":
            src = Path(fix["from"])
            dst = Path(fix["to"])
            if dry_run:
                results.append({"action": "rename", "from": str(src), "to": str(dst), "dry_run": True})
            else:
                if src.exists() and not dst.exists():
                    src.rename(dst)
                    results.append({"action": "rename", "from": str(src), "to": str(dst), "done": True})
                elif dst.exists():
                    results.append({"action": "rename", "skipped": True, "reason": "destination already exists"})
                else:
                    results.append({"action": "rename", "skipped": True, "reason": "source not found"})
    return results


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(description="TTS project structure checker")
    p.add_argument("--impl-dir", required=True, help="Path to implementation_artifacts folder")
    p.add_argument("--planning-dir", required=True, help="Path to planning_artifacts folder")
    p.add_argument("--bmad-dir", required=True, help="Path to _bmad/ folder")
    p.add_argument("--story", help="Check/fix a single story key (prefix match)")
    p.add_argument("--fix", action="store_true", help="Apply auto-fixable corrections")
    p.add_argument("--dry-run", action="store_true", help="Show what --fix would do without writing")
    return p.parse_args()


def main():
    args = parse_args()

    impl_dir = Path(args.impl_dir)
    planning_dir = Path(args.planning_dir)
    bmad_dir = Path(args.bmad_dir)

    if not impl_dir.exists():
        print(json.dumps({"error": f"impl_dir not found: {impl_dir}"}))
        sys.exit(1)

    result = run_checks(impl_dir, planning_dir, bmad_dir, args.story)

    if args.fix or args.dry_run:
        fix_results = apply_auto_fixes(result["findings"], dry_run=args.dry_run)
        result["fix_results"] = fix_results
        result["fix_mode"] = "dry_run" if args.dry_run else "applied"

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
