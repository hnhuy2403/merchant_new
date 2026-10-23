#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
First Breath — Deterministic sanctum scaffolding for Senior QA.

Creates the personal sanctum + shared module memory directory tree, copies
template files with config substitution, copies all capability prompts and
supporting references into the sanctum, and auto-generates CAPABILITIES.md
from capability frontmatter.

After this runs, the sanctum is fully self-contained — the agent does
not depend on the skill bundle location for normal operation.

Usage:
    python3 init-sanctum.py <project-root> <skill-path>

    project-root: The root of the project (where _bmad/ lives)
    skill-path:   Path to the skill directory (where SKILL.md, references/, assets/ live)
"""

import sys
import re
import shutil
from datetime import date
from pathlib import Path

# --- Agent-specific configuration ---

SKILL_NAME = "bmad-tts-qc-agent-senior-qa"
SANCTUM_DIR = SKILL_NAME

# Files in references/ that should NOT be copied into the sanctum
# (used only during First Breath, lives in skill bundle)
SKILL_ONLY_FILES = {"first-breath.md"}

# Sanctum templates from assets/ to copy + substitute
TEMPLATE_FILES = [
    "PERSONA-template.md",
    "CREED-template.md",
    "BOND-template.md",
    "MEMORY-template.md",
    "INDEX-template.md",
]

# Whether the owner can teach this agent new capabilities
# (we set False for v1 — capabilities are designed by the builder)
EVOLVABLE = False

# Shared module memory layout (created if missing)
MODULE_MEMORY_DIRS = [
    "_bmad/memory/tts-qc",
    "_bmad/memory/tts-qc/curated",
    "_bmad/memory/tts-qc/curated/legacy-logic",
    "_bmad/memory/tts-qc/curated/regression-suite",
    "_bmad/memory/tts-qc/daily",
]

# Output directory tree (created if missing)
OUTPUT_DIRS = [
    "_bmad-output/qc",
    "_bmad-output/qc/test-cases",
    "_bmad-output/qc/regression-suite",
    "_bmad-output/qc/test-reports",
    "_bmad-output/qc/peer-reviews",
    "_bmad-output/qc/static-traces",
    "_bmad-output/qc/automation",
    "_bmad-output/qc/automation/web",
    "_bmad-output/qc/automation/mobile",
    "_bmad-output/qc/automation/miniapp",
]

# --- End agent-specific configuration ---


def parse_yaml_config(config_path: Path) -> dict:
    """Simple YAML key-value parser. Handles top-level scalar values only."""
    config = {}
    if not config_path.exists():
        return config
    with open(config_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line and not line.endswith(":"):
                key, _, value = line.partition(":")
                value = value.strip().strip("'\"")
                if value:
                    config[key.strip()] = value
    return config


def parse_frontmatter(file_path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    meta = {}
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return meta
    for line in match.group(1).strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip("'\"")
    return meta


def copy_references(source_dir: Path, dest_dir: Path) -> list[str]:
    """Copy reference files (excluding SKILL_ONLY_FILES) into the sanctum."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    for source_file in sorted(source_dir.iterdir()):
        if source_file.name in SKILL_ONLY_FILES:
            continue
        if source_file.is_file():
            shutil.copy2(source_file, dest_dir / source_file.name)
            copied.append(source_file.name)
    return copied


def copy_scripts(source_dir: Path, dest_dir: Path) -> list[str]:
    """Copy supporting scripts into the sanctum (excluding init-sanctum.py)."""
    if not source_dir.exists():
        return []
    dest_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    for source_file in sorted(source_dir.iterdir()):
        if source_file.is_file() and source_file.name != "init-sanctum.py":
            shutil.copy2(source_file, dest_dir / source_file.name)
            copied.append(source_file.name)
    return copied


def discover_capabilities(references_dir: Path, sanctum_refs_path: str) -> list[dict]:
    """Scan references/ for capability prompts with frontmatter (name, code)."""
    capabilities = []
    for md_file in sorted(references_dir.glob("*.md")):
        if md_file.name in SKILL_ONLY_FILES:
            continue
        # Skip non-capability references (memory-guidance, first-breath, etc.)
        # by requiring both `name` and `code` frontmatter fields.
        meta = parse_frontmatter(md_file)
        if meta.get("name") and meta.get("code"):
            capabilities.append({
                "name": meta["name"],
                "description": meta.get("description", ""),
                "code": meta["code"],
                "source": f"{sanctum_refs_path}/{md_file.name}",
            })
    return capabilities


def generate_capabilities_md(capabilities: list[dict], evolvable: bool) -> str:
    """Generate CAPABILITIES.md content from discovered capabilities."""
    lines = [
        "# Capabilities",
        "",
        "## Built-in",
        "",
        "| Code | Name | Description | Source |",
        "|------|------|-------------|--------|",
    ]
    for cap in capabilities:
        lines.append(
            f"| [{cap['code']}] | {cap['name']} | {cap['description']} | `{cap['source']}` |"
        )
    if evolvable:
        lines.extend([
            "",
            "## Learned",
            "",
            "_Capabilities added by the owner over time._",
            "",
            "| Code | Name | Description | Source | Added |",
            "|------|------|-------------|--------|-------|",
        ])
    lines.extend([
        "",
        "## Tools",
        "",
        "Prefer crafting your own tools over depending on external ones. "
        "A script you wrote and saved is more reliable than an external API. "
        "Use the file system creatively.",
        "",
        "### User-Provided Tools",
        "",
        "_MCP servers, APIs, or services the owner has made available. Document them here._",
    ])
    return "\n".join(lines) + "\n"


def substitute_vars(content: str, variables: dict) -> str:
    """Replace {var_name} placeholders with values from the variables dict."""
    for key, value in variables.items():
        content = content.replace(f"{{{key}}}", value)
    return content


def seed_module_index(qc_memory_dir: Path) -> Path:
    """Seed the shared module memory index.md if missing."""
    index_path = qc_memory_dir / "index.md"
    if index_path.exists():
        return index_path
    today = date.today().isoformat()
    content = f"""# QC Module Memory — Index

_Shared knowledge for the qc/ module. Loaded on demand by qc-agent-senior-qa and the qc-* standalone slash skills._

_Created: {today}_

## Curated Files

| File | Purpose | Last Updated |
|------|---------|--------------|
| `curated/project-profile.md` | Domain, tech stack, target users | {today} (seed) |
| `curated/business-rules.md` | Domain rules learned across requirements | {today} (seed) |
| `curated/stakeholders.md` | Who to ask what (BA, Dev lead, PO) | {today} (seed) |
| `curated/qa-conventions.md` | Severity scale, priority scale, naming | {today} (seed) |
| `curated/defect-history.md` | Past bugs + root causes for pattern matching | {today} (seed) |
| `curated/common-edge-cases.md` | Edge cases the team encounters often | {today} (seed) |
| `curated/legacy-logic/` | Distilled domain knowledge per topic | empty |
| `curated/regression-suite/` | Curated regression cases per feature | empty |
| `daily/YYYY-MM-DD.md` | Chronological log across all qc skills | empty |

## Recent Activity

_Updated by capabilities as they run. Most recent first._

- {today}: Index seeded by `init-sanctum.py`. Curated files are placeholders — fill during First Breath or as project context emerges.
"""
    index_path.write_text(content, encoding="utf-8")
    return index_path


def seed_curated_placeholders(curated_dir: Path) -> list[str]:
    """Seed empty placeholder curated files so they exist for capabilities to read."""
    seeds = {
        "project-profile.md": "# Project Profile\n\n_Filled during First Breath. Domain, tech stack, target users, current epic, release cadence._\n",
        "business-rules.md": "# Business Rules\n\n_Domain rules learned across requirements. Each entry: rule + source + first-seen date._\n",
        "stakeholders.md": "# Stakeholders\n\n_Filled during First Breath._\n\n- **BA**: _Not yet discovered._\n- **Dev lead**: _Not yet discovered._\n- **PO**: _Not yet discovered._\n",
        "qa-conventions.md": "# QA Conventions\n\n_Confirmed during First Breath. Update when team conventions change._\n\n- **Severity scale**: _Not yet discovered._\n- **Priority scale**: _Not yet discovered._\n- **Test case naming**: _Not yet discovered._\n",
        "defect-history.md": "# Defect History\n\n_Auto-appended by `qc-bug` capability. Each entry: bug summary, root cause, related code area, date._\n",
        "common-edge-cases.md": "# Common Edge Cases\n\n_Edge cases the team encounters often. Auto-appended by `qc-edge` and during curate phase._\n",
    }
    created = []
    for filename, content in seeds.items():
        path = curated_dir / filename
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            created.append(filename)
    return created


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 init-sanctum.py <project-root> <skill-path>")
        sys.exit(1)

    project_root = Path(sys.argv[1]).resolve()
    skill_path = Path(sys.argv[2]).resolve()

    # Personal sanctum paths
    bmad_dir = project_root / "_bmad"
    memory_dir = bmad_dir / "memory"
    sanctum_path = memory_dir / SANCTUM_DIR
    assets_dir = skill_path / "assets"
    references_dir = skill_path / "references"
    scripts_dir = skill_path / "scripts"
    sanctum_refs = sanctum_path / "references"
    sanctum_scripts = sanctum_path / "scripts"
    sanctum_refs_path = "./references"

    # Check if personal sanctum already exists
    if sanctum_path.exists():
        print(f"Sanctum already exists at {sanctum_path}")
        print("This agent has already been born. Skipping First Breath scaffolding.")
        # Still ensure shared module memory exists in case it was deleted
        for d in MODULE_MEMORY_DIRS:
            (project_root / d).mkdir(parents=True, exist_ok=True)
        for d in OUTPUT_DIRS:
            (project_root / d).mkdir(parents=True, exist_ok=True)
        sys.exit(0)

    # Load config from both core and module sections
    config = {}
    for cfg_file in ["config.yaml", "config.user.yaml"]:
        config.update(parse_yaml_config(bmad_dir / cfg_file))

    # Build variable substitution map
    today = date.today().isoformat()
    variables = {
        "user_name": config.get("user_name", "friend"),
        "communication_language": config.get("communication_language", "English"),
        "birth_date": today,
        "project_root": str(project_root),
        "sanctum_path": str(sanctum_path),
        "skillName": SKILL_NAME,
    }

    # Create personal sanctum structure
    sanctum_path.mkdir(parents=True, exist_ok=True)
    (sanctum_path / "sessions").mkdir(exist_ok=True)
    print(f"Created personal sanctum at {sanctum_path}")

    # Copy reference files (capability prompts + memory-guidance) into sanctum
    copied_refs = copy_references(references_dir, sanctum_refs)
    print(f"  Copied {len(copied_refs)} reference files to sanctum/references/")

    # Copy supporting scripts (xlsx-utils, codegen-*) into sanctum
    copied_scripts = copy_scripts(scripts_dir, sanctum_scripts)
    if copied_scripts:
        print(f"  Copied {len(copied_scripts)} scripts to sanctum/scripts/")

    # Copy and substitute template files into sanctum root
    for template_name in TEMPLATE_FILES:
        template_path = assets_dir / template_name
        if not template_path.exists():
            print(f"  Warning: template {template_name} not found, skipping")
            continue
        # PERSONA-template.md -> PERSONA.md
        output_name = template_name.replace("-template", "").upper()
        output_name = output_name[:-3] + ".md"
        content = template_path.read_text(encoding="utf-8")
        content = substitute_vars(content, variables)
        (sanctum_path / output_name).write_text(content, encoding="utf-8")
        print(f"  Created {output_name}")

    # Auto-generate CAPABILITIES.md from references/ frontmatter
    capabilities = discover_capabilities(references_dir, sanctum_refs_path)
    capabilities_content = generate_capabilities_md(capabilities, evolvable=EVOLVABLE)
    (sanctum_path / "CAPABILITIES.md").write_text(capabilities_content, encoding="utf-8")
    print(f"  Created CAPABILITIES.md ({len(capabilities)} built-in capabilities)")

    # Create shared module memory tree
    print()
    print("Creating shared module memory at _bmad/memory/tts-qc/...")
    for d in MODULE_MEMORY_DIRS:
        full = project_root / d
        full.mkdir(parents=True, exist_ok=True)
    qc_memory = project_root / "_bmad" / "memory" / "qc"
    seed_module_index(qc_memory)
    seeded = seed_curated_placeholders(qc_memory / "curated")
    print(f"  Seeded {len(seeded)} curated placeholder files: {', '.join(seeded)}")

    # Create output directory tree
    print()
    print("Creating output directory tree at _bmad-output/qc/...")
    for d in OUTPUT_DIRS:
        (project_root / d).mkdir(parents=True, exist_ok=True)
    print(f"  Created {len(OUTPUT_DIRS)} output directories.")

    print()
    print("First Breath scaffolding complete.")
    print("The conversational awakening can now begin.")
    print(f"Personal sanctum: {sanctum_path}")
    print(f"Shared module memory: {qc_memory}")


if __name__ == "__main__":
    main()
