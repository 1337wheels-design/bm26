# bm26 · Dolomiten Winterreise 2026

Offline-fähiger Reiseplaner (`dolomiten.html`) mit Orts- und Aktivitätsfotos aus dem Repository.

## GitHub Pages

**Integration:** Push auf `main` → Workflow baut Branch `gh-pages`. Einmalig Pages auf Branch **`gh-pages`** stellen — [DEPLOY.md](DEPLOY.md).

Dann erreichbar unter:

- **Start:** `https://1337wheels-design.github.io/bm26/` (Weiterleitung)
- **Planer:** `https://1337wheels-design.github.io/bm26/dolomiten.html`

Lokal testen:

```bash
python3 -m http.server 8080
# http://127.0.0.1:8080/dolomiten.html
```

## Bilder

Siehe [ATTRIBUTION.md](ATTRIBUTION.md). `index.html` leitet auf den Planer um; das BM25-Demo liegt in `bm25-search.html`.