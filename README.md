# bm26 · Dolomiten Winterreise 2026

Offline-fähiger Reiseplaner (`dolomiten.html`) mit Orts- und Aktivitätsfotos aus dem Repository.

## GitHub Pages

**Einmalig:** [Repository Settings → Pages](https://github.com/1337wheels-design/bm26/settings/pages) → **Build and deployment → Source: GitHub Actions** speichern. Danach unter **Actions** den fehlgeschlagenen Workflow **Re-run** ausführen.

*(Privates Repo: GitHub Pro/Team für öffentliche Pages-URL, oder Repo auf **Public** stellen.)*

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