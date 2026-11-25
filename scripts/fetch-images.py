#!/usr/bin/env python3
"""Fetch curated Wikimedia Commons images for Dolomiten planner."""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
UA = "bm26-dolomiten-planner/2.0 (contact: github.com/1337wheels-design/bm26)"
CURATED = ROOT / "images" / "curated.json"
API_GAP_S = 2.5
DOWNLOAD_GAP_S = 5.0


def api(params: dict) -> dict:
    q = urllib.parse.urlencode({**params, "format": "json"})
    url = f"https://commons.wikimedia.org/w/api.php?{q}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                data = json.load(r)
            time.sleep(API_GAP_S)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 5:
                wait = 45 * (attempt + 1)
                print(f"  API 429 — warte {wait}s …", flush=True)
                time.sleep(wait)
                continue
            raise


def thumb_from_file(file_title: str, width: int) -> str | None:
    data = api(
        {
            "action": "query",
            "titles": file_title,
            "prop": "imageinfo",
            "iiprop": "url|size",
            "iiurlwidth": width,
        }
    )
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        if page.get("missing") or "imageinfo" not in page:
            return None
        ii = page["imageinfo"][0]
        if ii.get("width", 0) < 640:
            return None
        return ii.get("thumburl") or ii.get("url")
    return None


def search_image(query: str, width: int) -> str | None:
    data = api(
        {
            "action": "query",
            "generator": "search",
            "gsrsearch": f"filetype:bitmap {query}",
            "gsrnamespace": "6",
            "gsrlimit": "12",
            "prop": "imageinfo",
            "iiprop": "url|size",
            "iiurlwidth": width,
        }
    )
    pages = data.get("query", {}).get("pages", {})
    best = []
    for page in sorted(pages.values(), key=lambda p: p.get("index", 99)):
        if "imageinfo" not in page:
            continue
        title = page.get("title", "")
        if re.search(r"(logo|icon|map|diagram|coat|flag|signature)", title, re.I):
            continue
        ii = page["imageinfo"][0]
        w, h = ii.get("width", 0), ii.get("height", 0)
        if w < 800 or h < 500:
            continue
        best.append((w * h, ii.get("thumburl") or ii.get("url")))
    if not best:
        return None
    best.sort(reverse=True)
    return best[0][1]


def resolve(file_title: str | None, search: str | None, width: int) -> tuple[str | None, str]:
    if file_title:
        url = thumb_from_file(file_title, width)
        if url:
            return url, file_title
    if search:
        url = search_image(search, width)
        if url:
            return url, search
    return None, search or file_title or ""


def curl_download(url: str, dest: pathlib.Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(4):
        r = subprocess.run(
            [
                "curl",
                "-fsSL",
                "-A",
                UA,
                "-o",
                str(dest),
                url,
            ],
            capture_output=True,
            timeout=180,
        )
        if r.returncode == 0 and dest.stat().st_size > 8000:
            time.sleep(DOWNLOAD_GAP_S)
            return True
        wait = 20 * (attempt + 1)
        print(f"  curl retry in {wait}s …", flush=True)
        time.sleep(wait)
    return False


def main() -> None:
    cfg = json.loads(CURATED.read_text(encoding="utf-8"))
    width = int(cfg.get("width", 1280))
    place_map: dict[str, dict] = {}
    act_map: dict[str, list] = {pid: [] for pid in cfg["places"]}

    for pid, spec in cfg["places"].items():
        rel = f"images/places/{pid}.jpg"
        dest = ROOT / rel
        print(f"place {pid} …", flush=True)
        if dest.exists() and dest.stat().st_size > 8000:
            src = spec.get("file") or spec.get("search") or "cached"
            place_map[pid] = {"img": rel, "imgSource": src}
            print(f"KEEP {rel}")
            continue
        url, src = resolve(spec.get("file"), spec.get("search"), width)
        if url and curl_download(url, dest):
            place_map[pid] = {"img": rel, "imgSource": src}
            print(f"OK {rel}")
        elif dest.exists() and dest.stat().st_size > 8000:
            place_map[pid] = {"img": rel, "imgSource": src or "cached"}
            print(f"KEEP {rel}")
        else:
            print(f"MISS place {pid}")

    for row in cfg["activities"]:
        pid, slug, kind, label = row[0], row[1], row[2], row[3]
        file_title = row[4] if len(row) > 4 else None
        extra = row[5] if len(row) > 5 else None
        match = None
        search = label
        if file_title:
            if extra and not str(extra).startswith("File:"):
                match = extra
        else:
            if extra:
                search = extra
        rel = f"images/activities/{slug}.jpg"
        dest = ROOT / rel
        print(f"activity {slug} …", flush=True)
        item = {"src": rel, "title": label, "kind": kind, "imgSource": file_title or search}
        if match:
            item["match"] = match
        if dest.exists() and dest.stat().st_size > 8000:
            act_map.setdefault(pid, []).append(item)
            print(f"KEEP {rel}")
            continue
        url, src = resolve(file_title, search, width)
        item["imgSource"] = src
        if url and curl_download(url, dest):
            act_map.setdefault(pid, []).append(item)
            print(f"OK {rel}")
        else:
            print(f"MISS activity {slug}")

    out = ROOT / "images" / "manifest.json"
    out.write_text(
        json.dumps({"places": place_map, "activities": act_map}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {out} ({len(place_map)} places)")


if __name__ == "__main__":
    main()