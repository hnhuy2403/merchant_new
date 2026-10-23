#!/usr/bin/env python3
"""Figma CLI — fetch screens (top-level frames) from the project's Figma file.

Reads credentials from `_bmad/config.user.yaml`:
  tts.figma.token     personal access token (prefix figd_)
  tts.figma.file_key  optional override; default is the project's design file

Subcommands:
  list-screens [--page NAME] [--raw]
      List top-level FRAME/COMPONENT/SECTION nodes across all pages.

  get-screen <name|id> [--depth N] [--raw]
      Fetch design tree of one screen. Default output is a compact indented
      view (id, type, name, size, text, color). --raw prints the full JSON.

  export <name|id> --format png|svg|jpg|pdf [--scale N] [--output PATH]
      Download an image of the screen into _bmad-output/figma-exports/.

Run from project root.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Optional

try:
    import yaml
except ImportError:
    sys.exit("ERROR: PyYAML required. Install with `pip install pyyaml` or `python3 -m pip install pyyaml`.")

API = "https://api.figma.com/v1"
CONFIG_PATH = "_bmad/config.user.yaml"
DEFAULT_FILE_KEY = "I3jxlZZi9hUlSAC2YBis8j"
DEFAULT_EXPORT_DIR = "_bmad-output/figma-exports"
SCREEN_TYPES = {"FRAME", "COMPONENT", "COMPONENT_SET", "SECTION"}


def load_config() -> tuple[str, str]:
    path = pathlib.Path(CONFIG_PATH)
    if not path.exists():
        sys.exit(
            f"ERROR: {CONFIG_PATH} not found. Run this script from the project root."
        )
    data = yaml.safe_load(path.read_text()) or {}
    figma = (data.get("tts") or {}).get("figma") or {}
    token = figma.get("token")
    if not token:
        sys.exit(
            f"ERROR: tts.figma.token not set in {CONFIG_PATH}.\n"
            "Get a personal access token at https://www.figma.com/settings "
            "→ Personal access tokens, then paste into the template block at the bottom of the file."
        )
    file_key = figma.get("file_key") or DEFAULT_FILE_KEY
    return token, file_key


def figma_get(path: str, token: str, params: Optional[dict[str, Any]] = None) -> dict:
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"X-Figma-Token": token})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="ignore")
        sys.exit(f"ERROR: Figma API {e.code}: {body}")
    except urllib.error.URLError as e:
        sys.exit(f"ERROR: Network error: {e}")


def _box_size(node: dict) -> str:
    box = node.get("absoluteBoundingBox") or {}
    w, h = box.get("width"), box.get("height")
    if w is None or h is None:
        return ""
    return f"{int(w)}x{int(h)}"


def _hex_from_color(c: dict) -> str:
    r = int(round(c.get("r", 0) * 255))
    g = int(round(c.get("g", 0) * 255))
    b = int(round(c.get("b", 0) * 255))
    return f"#{r:02x}{g:02x}{b:02x}"


def list_all_screens(file_key: str, token: str, page_filter: Optional[str] = None) -> list[dict]:
    data = figma_get(f"/files/{file_key}", token, {"depth": "2"})
    doc = data.get("document", {})
    screens = []
    for page in doc.get("children", []):
        if page.get("type") != "CANVAS":
            continue
        page_name = page.get("name", "")
        if page_filter and page_filter.lower() not in page_name.lower():
            continue
        for frame in page.get("children", []):
            if frame.get("type") in SCREEN_TYPES:
                screens.append({
                    "page": page_name,
                    "page_id": page["id"],
                    "id": frame["id"],
                    "name": frame.get("name", ""),
                    "type": frame.get("type"),
                    "size": _box_size(frame),
                })
    return screens


def resolve_screen(target: str, file_key: str, token: str) -> dict:
    screens = list_all_screens(file_key, token)
    for s in screens:
        if s["id"] == target:
            return s
    matches = [s for s in screens if s["name"].lower() == target.lower()]
    if not matches:
        matches = [s for s in screens if target.lower() in s["name"].lower()]
    if not matches:
        sys.exit(
            f"ERROR: No screen matching '{target}'. Run `list-screens` to see available names."
        )
    if len(matches) > 1:
        lines = "\n".join(
            f"  [{m['id']}] {m['name']}  (page: {m['page']})" for m in matches
        )
        sys.exit(
            f"ERROR: '{target}' matches multiple screens:\n{lines}\nUse the id (e.g. 1:23) instead."
        )
    return matches[0]


def fetch_screen_tree(node_id: str, file_key: str, token: str, depth: int) -> dict:
    data = figma_get(
        f"/files/{file_key}/nodes",
        token,
        {"ids": node_id, "depth": str(depth)},
    )
    entry = (data.get("nodes") or {}).get(node_id)
    if not entry:
        sys.exit(f"ERROR: Node {node_id} not returned by the API.")
    return entry["document"]


def compact_node(node: dict, indent: int = 0, out: Optional[list[str]] = None) -> list[str]:
    if out is None:
        out = []
    name = node.get("name", "")
    typ = node.get("type", "")
    info: list[str] = []
    size = _box_size(node)
    if size:
        info.append(size)
    if typ == "TEXT":
        text = (node.get("characters") or "")[:80].replace("\n", " ")
        info.append(f'text="{text}"')
    for fill in node.get("fills") or []:
        if fill.get("type") == "SOLID" and fill.get("visible", True):
            color = fill.get("color") or {}
            info.append(_hex_from_color(color))
            break
    info_str = "  ".join(info)
    out.append(
        "  " * indent
        + f"[{node.get('id', '?')}] ({typ}) {name}".rstrip()
        + (f"  {info_str}" if info_str else "")
    )
    for child in node.get("children") or []:
        compact_node(child, indent + 1, out)
    return out


def safe_filename(name: str) -> str:
    s = re.sub(r"[^\w\-.]+", "_", name.strip()).strip("_")
    return s[:80] or "screen"


def export_image(
    node_id: str,
    file_key: str,
    token: str,
    fmt: str,
    scale: float,
    out_path: pathlib.Path,
) -> None:
    params = {"ids": node_id, "format": fmt, "scale": str(scale)}
    data = figma_get(f"/images/{file_key}", token, params)
    if data.get("err"):
        sys.exit(f"ERROR: Figma export failed: {data['err']}")
    url = (data.get("images") or {}).get(node_id)
    if not url:
        sys.exit(f"ERROR: No image URL returned for node {node_id}.")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as resp, open(out_path, "wb") as f:
        f.write(resp.read())
    print(f"OK exported {fmt.upper()} -> {out_path}")


def cmd_list_screens(args: argparse.Namespace) -> None:
    token, file_key = load_config()
    screens = list_all_screens(file_key, token, page_filter=args.page)
    if args.raw:
        json.dump(screens, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return
    if not screens:
        print("(no screens found)")
        return
    current_page = None
    for s in screens:
        if s["page"] != current_page:
            current_page = s["page"]
            print(f"\n== {current_page}  [{s['page_id']}] ==")
        print(f"  [{s['id']:<10}] {s['type']:<14} {s['size']:<12} {s['name']}")


def cmd_get_screen(args: argparse.Namespace) -> None:
    token, file_key = load_config()
    screen = resolve_screen(args.target, file_key, token)
    tree = fetch_screen_tree(screen["id"], file_key, token, depth=args.depth)
    if args.raw:
        json.dump(tree, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return
    print(f"# {screen['name']}  (page: {screen['page']})")
    print(f"id: {screen['id']}   type: {screen['type']}   size: {screen['size']}")
    print()
    for line in compact_node(tree):
        print(line)


def cmd_export(args: argparse.Namespace) -> None:
    token, file_key = load_config()
    screen = resolve_screen(args.target, file_key, token)
    out = args.output or f"{DEFAULT_EXPORT_DIR}/{safe_filename(screen['name'])}.{args.format}"
    export_image(screen["id"], file_key, token, args.format, args.scale, pathlib.Path(out))


def main() -> None:
    parser = argparse.ArgumentParser(prog="figma-cli", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    ls = sub.add_parser("list-screens", help="List top-level frames (screens).")
    ls.add_argument("--page", help="Substring filter on page name.")
    ls.add_argument("--raw", action="store_true", help="Output raw JSON.")
    ls.set_defaults(func=cmd_list_screens)

    gs = sub.add_parser("get-screen", help="Fetch design tree of a screen by name or id.")
    gs.add_argument("target", help="Screen name (case-insensitive substring) or id (e.g. 1:23).")
    gs.add_argument("--depth", type=int, default=4, help="Tree depth (default 4).")
    gs.add_argument("--raw", action="store_true", help="Output raw JSON tree.")
    gs.set_defaults(func=cmd_get_screen)

    ex = sub.add_parser("export", help="Export PNG/SVG of a screen to disk.")
    ex.add_argument("target", help="Screen name or id.")
    ex.add_argument("--format", choices=["png", "svg", "jpg", "pdf"], default="png")
    ex.add_argument("--scale", type=float, default=2.0, help="PNG/JPG scale (default 2).")
    ex.add_argument(
        "--output",
        help=f"Output path. Default: {DEFAULT_EXPORT_DIR}/<safe-name>.<fmt>",
    )
    ex.set_defaults(func=cmd_export)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
