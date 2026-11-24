#!/usr/bin/env python3
"""Fetch CC images from Wikimedia Commons for Dolomiten planner."""
from __future__ import annotations

import json
import pathlib
import re
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
UA = "bm26-dolomiten-planner/1.0 (contact: github.com/1337wheels-design/bm26)"

# place_id -> search terms for commons
PLACES = {
    "meran": "Meran Südtirol",
    "bozen": "Bozen Südtirol",
    "brixen": "Brixen Südtirol",
    "groeden": "Gröden Dolomiten",
    "bruneck": "Bruneck Südtirol",
    "hochpustertal": "Pragser Wildsee",
    "cortina": "Cortina d Ampezzo",
    "fiemme": "Val di Fiemme",
    "trient": "Trento Piazza Duomo",
    "levico": "Lago di Levico",
    "bassano": "Ponte degli Alpini Bassano",
    "vicenza": "Basilica Palladiana Vicenza",
    "hallstatt": "Hallstatt Austria",
}

ACTIVITIES = [
    ("meran", "meran-tappeiner", "Tappeinerweg Meran"),
    ("meran", "meran-markt", "Therme Meran"),
    ("bozen", "bozen-markt", "Christkindlmarkt Bozen"),
    ("brixen", "brixen-villnoess", "Geislerspitzen Villnöss"),
    ("bruneck", "bruneck-pragser", "Pragser Wildsee"),
    ("hochpustertal", "hochpustertal-dreizinnen", "Drei Zinnen"),
    ("cortina", "cortina-corso", "Cortina Corso Italia"),
    ("trient", "trient-muse", "MUSE Trento"),
]


def api(params: dict) -> dict:
    q = urllib.parse.urlencode({**params, "format": "json"})
    url = f"https://commons.wikimedia.org/w/api.php?{q}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def search_image(query: str) -> str | None:
    data = api(
        {
            "action": "query",
            "generator": "search",
            "gsrsearch": f'filetype:bitmap {query}',
            "gsrnamespace": "6",
            "gsrlimit": "8",
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": "960",
        }
    )
    pages = data.get("query", {}).get("pages", {})
    for page in sorted(pages.values(), key=lambda p: p.get("index", 99)):
        if "imageinfo" not in page:
            continue
        title = page.get("title", "")
        if re.search(r"(logo|icon|map|diagram|coat|flag)", title, re.I):
            continue
        return page["imageinfo"][0]["thumburl"]
    return None


def download(url: str, dest: pathlib.Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        dest.write_bytes(r.read())


def main() -> None:
    mapping: dict[str, dict] = {}
    for pid, query in PLACES.items():
        url = search_image(query)
        if not url:
            print(f"MISS place {pid}: {query}")
            continue
        rel = f"images/places/{pid}.jpg"
        dest = ROOT / rel
        download(url, dest)
        mapping[pid] = {"img": rel, "imgSource": query}
        print(f"OK {rel}")

    act_map: dict[str, list] = {pid: [] for pid in PLACES}
    for pid, slug, query in ACTIVITIES:
        url = search_image(query)
        if not url:
            print(f"MISS activity {slug}: {query}")
            continue
        rel = f"images/activities/{slug}.jpg"
        download(url, ROOT / rel)
        act_map.setdefault(pid, []).append({"src": rel, "title": query, "imgSource": query})
        print(f"OK {rel}")

    out = ROOT / "images" / "manifest.json"
    out.write_text(
        json.dumps({"places": mapping, "activities": act_map}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()