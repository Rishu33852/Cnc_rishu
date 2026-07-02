#!/usr/bin/env python3
"""
generate_repo.py
────────────────
Scans a directory of built CloudStream .cs3 plugin files and generates
a CloudStream-compatible repository JSON file (e.g. CNC.json).

CloudStream repository JSON format:
{
  "name": "<repo name>",
  "plugins": [
    {
      "url":        "https://.../PluginName.cs3",
      "status":     1,
      "version":    23,
      "apiVersion": "2",
      "name":       "PluginName",
      "authors":    ["Author"],
      "description": "...",
      "repositoryUrl": "https://github.com/...",
      "language":   "ta",
      "tvTypes":    ["Movie", "TvSeries"],
      "iconUrl":    "https://...",
      "requiresResources": false
    },
    ...
  ]
}
"""
import argparse
import json
import os
import re
import sys
import zipfile


# ── Metadata embedded by the cloudstream gradle plugin ──────────────────────
# The plugin writes a cloudstream.json inside each .cs3 (which is a zip).
# If it's absent we fall back to parsing build.gradle.kts in the source tree.

def read_cs3_meta(cs3_path: str) -> dict:
    """Try to read cloudstream.json from inside the .cs3 zip."""
    try:
        with zipfile.ZipFile(cs3_path, 'r') as z:
            names = z.namelist()
            for candidate in ("cloudstream.json", "plugin.json"):
                if candidate in names:
                    return json.loads(z.read(candidate).decode())
    except Exception:
        pass
    return {}


def parse_gradle(gradle_path: str) -> dict:
    """Fallback: parse build.gradle.kts for cloudstream metadata."""
    if not os.path.exists(gradle_path):
        return {}
    text = open(gradle_path, encoding="utf-8", errors="replace").read()

    def get(key, default=""):
        m = re.search(rf'{key}\s*=\s*"([^"]*)"', text)
        return m.group(1) if m else default

    def get_int(key, default=0):
        m = re.search(rf'(?:^|\n)\s*{key}\s*=\s*(\d+)', text)
        return int(m.group(1)) if m else default

    def get_list(key):
        m = re.search(rf'{key}\s*=\s*listOf\(([^)]*)\)', text, re.DOTALL)
        if not m:
            return []
        return [x.strip().strip('"').strip("'") for x in m.group(1).split(',') if x.strip().strip('"\'')]

    def get_bool(key):
        m = re.search(rf'{key}\s*=\s*(true|false)', text)
        return m.group(1) == 'true' if m else False

    return {
        "version":          get_int("version"),
        "description":      get("description"),
        "language":         get("language", "en"),
        "status":           get_int("status", 3),
        "tvTypes":          get_list("tvTypes"),
        "iconUrl":          get("iconUrl"),
        "authors":          get_list("authors"),
        "requiresResources": get_bool("requiresResources"),
    }


def find_gradle(plugin_name: str, source_root: str) -> str:
    """Locate the build.gradle.kts for a given plugin name."""
    # Exact match first
    candidate = os.path.join(source_root, plugin_name, "build.gradle.kts")
    if os.path.exists(candidate):
        return candidate
    # Fuzzy: dir whose name matches (case-insensitive, ignoring spaces)
    norm = plugin_name.lower().replace(" ", "")
    for entry in os.listdir(source_root):
        if entry.lower().replace(" ", "") == norm:
            candidate = os.path.join(source_root, entry, "build.gradle.kts")
            if os.path.exists(candidate):
                return candidate
    return ""


def build_plugin_entry(cs3_path: str, repo_url: str, source_root: str) -> dict:
    filename = os.path.basename(cs3_path)
    plugin_name = os.path.splitext(filename)[0]

    # 1. Try metadata embedded inside the .cs3
    meta = read_cs3_meta(cs3_path)

    # 2. Fallback to build.gradle.kts
    if not meta:
        gradle = find_gradle(plugin_name, source_root)
        meta = parse_gradle(gradle)

    plugin_url = repo_url.rstrip("/") + "/" + filename

    entry = {
        "url":               plugin_url,
        "status":            meta.get("status", 1),
        "version":           meta.get("version", 1),
        "apiVersion":        meta.get("apiVersion", "2"),
        "name":              meta.get("name", plugin_name),
        "authors":           meta.get("authors", []),
        "description":       meta.get("description", ""),
        "repositoryUrl":     meta.get("repositoryUrl", ""),
        "language":          meta.get("language", "en"),
        "tvTypes":           meta.get("tvTypes", []),
        "iconUrl":           meta.get("iconUrl", ""),
        "requiresResources": meta.get("requiresResources", False),
    }
    return entry


def main():
    parser = argparse.ArgumentParser(description="Generate CloudStream repo JSON")
    parser.add_argument("--cs3_dir",   required=True,  help="Directory containing .cs3 files")
    parser.add_argument("--repo_url",  required=True,  help="Base raw URL where .cs3 files will be served")
    parser.add_argument("--out",       required=True,  help="Output path for the JSON file")
    parser.add_argument("--name",      default="CNCVerse", help="Repository name")
    parser.add_argument("--source_root", default="",   help="Path to repo root for gradle fallback")
    args = parser.parse_args()

    cs3_files = sorted(
        f for f in os.listdir(args.cs3_dir) if f.endswith(".cs3")
    )

    if not cs3_files:
        print("WARNING: no .cs3 files found in", args.cs3_dir, file=sys.stderr)

    # Auto-detect source root: script lives in .github/scripts/, so go up two levels
    source_root = args.source_root
    if not source_root:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        source_root = os.path.normpath(os.path.join(script_dir, "..", ".."))

    plugins = []
    for fname in cs3_files:
        cs3_path = os.path.join(args.cs3_dir, fname)
        try:
            entry = build_plugin_entry(cs3_path, args.repo_url, source_root)
            plugins.append(entry)
            print(f"  ✓ {fname}  v{entry['version']}  {entry['language']}  {entry['tvTypes']}")
        except Exception as e:
            print(f"  ✗ {fname}: {e}", file=sys.stderr)

    repo = {
        "name": args.name,
        "plugins": plugins,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(repo, f, indent=2, ensure_ascii=False)

    print(f"\nWrote {len(plugins)} plugins → {args.out}")


if __name__ == "__main__":
    main()
