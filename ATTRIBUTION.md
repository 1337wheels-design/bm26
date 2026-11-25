# Bildnachweise

Die Fotos unter `images/` stammen von **Wikimedia Commons** und werden im Projekt nur als illustrative Vorschaubilder für Orte und geplante Aktivitäten genutzt. Vor Reisebeginn bitte die jeweilige Commons-Dateiseite für genaue Lizenz und Urheber prüfen.

Kurate Auswahl und Abfrage: `images/curated.json`. Neu erzeugen (gedrosselt, sonst Wikimedia 429):

```bash
python3 scripts/fetch-images.py
```

Nach Rate-Limits ggf. einige Minuten warten. Platzhalter für neue italienische Stationen werden beim ersten Lauf ersetzt.

Die Zuordnung liegt in `images/manifest.json` (Felder `kind`: `hike` | `highlight`).

## Reliefkarte

`images/region-map.jpg` — [Northern Italy relief location map](https://commons.wikimedia.org/wiki/File:Northern_Italy_relief_location_map.jpg) (Wikimedia Commons, Kartografie-Workshop). Georeferenz in `dolomiten.html` (`MAP_GEO`).