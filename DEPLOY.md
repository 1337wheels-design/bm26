# Deployment (GitHub Pages)

## Integration

| Was | Wie |
|-----|-----|
| **CI** | Push auf `main` → Workflow [Publish site](https://github.com/1337wheels-design/bm26/actions/workflows/publish-site.yml) schreibt Branch `gh-pages` (nur HTML + `images/`) |
| **Hosting** | Einmalig: [Settings → Pages](https://github.com/1337wheels-design/bm26/settings/pages) → **Deploy from a branch** → Branch **`gh-pages`** · **`/ (root)`** → **Save** |

Danach aktualisiert sich die Live-Seite bei jedem Push auf `main` (nach dem Workflow, ca. 1–2 Min.).

## URLs

- https://1337wheels-design.github.io/bm26/
- https://1337wheels-design.github.io/bm26/dolomiten.html

## Warum nicht „GitHub Actions“ als Pages-Source?

Der offizielle `deploy-pages`-Flow braucht manuell aktiviertes Pages **und** OIDC (`pages: write`).  
`configure-pages` mit `enablement: true` schlägt nach ~5 s mit *Resource not accessible by integration* fehl.  
Der **`gh-pages`-Branch** nutzt nur `contents: write` und funktioniert zuverlässig mit dem Standard-`GITHUB_TOKEN`.

## Lokal testen

```bash
python3 -m http.server 8080
# http://127.0.0.1:8080/dolomiten.html
```