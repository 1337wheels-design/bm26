#!/usr/bin/env bash
# Download place/activity thumbnails from Wikimedia Commons (CC-licensed).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/images/places" "$ROOT/images/activities"

fetch_thumb() {
  local file_title="$1"
  local out_path="$2"
  local url
  url=$(python3 - <<PY
import json, urllib.parse, urllib.request
title = urllib.parse.quote("$file_title".replace(" ", "_"))
api = f"https://commons.wikimedia.org/w/api.php?action=query&titles={title}&prop=imageinfo&iiprop=url&iiurlwidth=960&format=json"
req = urllib.request.Request(api, headers={"User-Agent": "bm26-dolomiten-planner/1.0 (GitHub Pages; educational)"})
with urllib.request.urlopen(req, timeout=60) as r:
    data = json.load(r)
pages = data["query"]["pages"]
for p in pages.values():
    if "imageinfo" in p:
        print(p["imageinfo"][0]["thumburl"])
        break
PY
)
  if [[ -z "${url:-}" ]]; then
    echo "SKIP (no URL): $file_title" >&2
    return 1
  fi
  curl -fsSL "$url" -o "$out_path"
  echo "OK $out_path"
}

# id|commons file title|output under images/
while IFS='|' read -r id file out; do
  [[ -z "$id" || "$id" == \#* ]] && continue
  fetch_thumb "$file" "$ROOT/$out" || true
done <<'EOF'
meran|File:Meran im Winter.jpg|images/places/meran.jpg
meran-hike|File:Tappeiner Promenade Meran.jpg|images/activities/meran-tappeiner.jpg
meran-hl|File:Therme Meran Außenansicht.jpg|images/activities/meran-therme.jpg
bozen|File:Bozen Panorama.jpg|images/places/bozen.jpg
bozen-hl|File:Christkindlmarkt Bozen.jpg|images/activities/bozen-markt.jpg
brixen|File:Brixen Südtirol.jpg|images/places/brixen.jpg
brixen-hike|File:Geislerspitzen Villnöss.jpg|images/activities/brixen-villnoess.jpg
groeden|File:Langkofel Gröden.jpg|images/places/groeden.jpg
bruneck|File:Bruneck Stadtansicht.jpg|images/places/bruneck.jpg
bruneck-hl|File:Pragser Wildsee Winter.jpg|images/activities/bruneck-pragser.jpg
hochpustertal|File:Pragser Wildsee.jpg|images/places/hochpustertal.jpg
hochpustertal-hl|File:Drei Zinnen von Süden.jpg|images/activities/hochpustertal-dreizinnen.jpg
cortina|File:Cortina d'Ampezzo panorama.jpg|images/places/cortina.jpg
fiemme|File:Val di Fiemme panorama.jpg|images/places/fiemme.jpg
trient|File:Trento Piazza Duomo.jpg|images/places/trient.jpg
levico|File:Lago di Levico.jpg|images/places/levico.jpg
bassano|File:Ponte degli Alpini Bassano.jpg|images/places/bassano.jpg
vicenza|File:Palladio Basilica Palladiana.jpg|images/places/vicenza.jpg
hallstatt|File:Hallstatt Winter.jpg|images/places/hallstatt.jpg
EOF