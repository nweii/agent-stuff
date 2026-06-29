#!/usr/bin/env python3
# ABOUTME: Search and validate Lucide icon names against the full set (unpkg lucide-static tags.json).
# ABOUTME: Fetches the catalog once, caches it, then answers search/validate/list locally — no per-icon network calls.

"""
Lucide icon helper. Zero dependencies (Python 3 stdlib only).

Usage:
  lucide.py search QUERY...        Find real icons matching a concept (name + semantic tags), ranked.
  lucide.py validate NAME...       Check which names exist; suggest near-matches for misses.
  lucide.py list                   Print every icon name.

Options:
  --limit N    Max results for search (default 25).
  --json       Machine-readable JSON instead of text.
  --refresh    Force re-download of the catalog (otherwise cached ~24h).

Exit codes: validate exits 1 if any name is missing, so it doubles as a check.
Source: https://unpkg.com/lucide-static@latest/tags.json
"""

import argparse
import json
import sys
import time
import urllib.request
from difflib import get_close_matches
from pathlib import Path
from tempfile import gettempdir

CATALOG_URL = "https://unpkg.com/lucide-static@latest/tags.json"
CACHE_PATH = Path(gettempdir()) / "lucide-static-tags.json"
CACHE_TTL_SECONDS = 24 * 60 * 60


def load_catalog(refresh: bool = False) -> dict:
    """Return {icon-name: [tags]}, fetching+caching the catalog as needed."""
    fresh = CACHE_PATH.exists() and (time.time() - CACHE_PATH.stat().st_mtime) < CACHE_TTL_SECONDS
    if fresh and not refresh:
        try:
            return json.loads(CACHE_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            pass  # corrupt cache → refetch
    try:
        with urllib.request.urlopen(CATALOG_URL, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
    except Exception as e:  # noqa: BLE001 — surface any network/HTTP failure plainly
        sys.exit(f"error: could not fetch Lucide catalog ({CATALOG_URL}): {e}")
    try:
        CACHE_PATH.write_text(raw)
    except OSError:
        pass  # cache is an optimization, not required
    return json.loads(raw)


def score(name: str, tags: list, tokens: list) -> int:
    name_tokens = name.split("-")
    s = 0
    for t in tokens:
        if t == name:
            s += 100
        elif t in name_tokens:
            s += 10
        elif t in name:
            s += 5
        if t in tags:
            s += 8
        elif any(t in tag for tag in tags):
            s += 3
    return s


def cmd_search(catalog: dict, query: list, limit: int, as_json: bool) -> int:
    tokens = [t.lower() for t in " ".join(query).replace(",", " ").split() if t]
    if not tokens:
        sys.exit("error: search needs a query, e.g. lucide.py search calendar schedule")
    ranked = sorted(
        ((name, tags, score(name, tags, tokens)) for name, tags in catalog.items()),
        key=lambda x: (-x[2], x[0]),
    )
    hits = [(n, tags) for n, tags, sc in ranked if sc > 0][:limit]
    if as_json:
        print(json.dumps([{"name": n, "tags": tags} for n, tags in hits], indent=2))
    elif not hits:
        print("(no matches — try broader or different terms)")
    else:
        for n, tags in hits:
            print(f"{n}  —  {', '.join(tags)}" if tags else n)
    return 0


def cmd_validate(catalog: dict, names: list, as_json: bool) -> int:
    all_names = list(catalog)
    results, missing = [], False
    for raw in names:
        name = raw.strip().lower()
        if name in catalog:
            results.append({"name": name, "exists": True, "suggestions": []})
        else:
            missing = True
            results.append(
                {"name": name, "exists": False, "suggestions": get_close_matches(name, all_names, n=3, cutoff=0.5)}
            )
    if as_json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            if r["exists"]:
                print(f"{r['name']}: ok")
            else:
                hint = f" (did you mean: {', '.join(r['suggestions'])}?)" if r["suggestions"] else ""
                print(f"{r['name']}: MISSING{hint}")
    return 1 if missing else 0


def main() -> int:
    # Common flags live on a parent so they can follow the subcommand (e.g. `search foo --json`).
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="JSON output")
    common.add_argument("--refresh", action="store_true", help="force catalog re-download")

    p = argparse.ArgumentParser(description="Search and validate Lucide icon names.")
    sub = p.add_subparsers(dest="command", required=True)
    sp = sub.add_parser("search", parents=[common], help="find icons matching a concept")
    sp.add_argument("query", nargs="+")
    sp.add_argument("--limit", type=int, default=25, help="max search results (default 25)")
    vp = sub.add_parser("validate", parents=[common], help="check that names exist")
    vp.add_argument("name", nargs="+")
    sub.add_parser("list", parents=[common], help="print all icon names")
    args = p.parse_args()

    catalog = load_catalog(refresh=args.refresh)

    if args.command == "search":
        return cmd_search(catalog, args.query, args.limit, args.json)
    if args.command == "validate":
        return cmd_validate(catalog, args.name, args.json)
    if args.command == "list":
        print(json.dumps(sorted(catalog)) if args.json else "\n".join(sorted(catalog)))
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
