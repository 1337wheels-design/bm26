# Dolomiten-Planer online stellen (GitHub Pages)

## Empfohlen: Deploy from a branch (kein Actions-Fehler)

1. [Settings → Pages](https://github.com/1337wheels-design/bm26/settings/pages)
2. **Build and deployment → Source:** **Deploy from a branch**
3. **Branch:** `main` · Ordner **`/ (root)`** → **Save**
4. Nach 1–2 Minuten öffnen: **https://1337wheels-design.github.io/bm26/dolomiten.html**

Der Workflow „Deploy GitHub Pages“ wird dabei **nicht** benötigt.

## Alternative: GitHub Actions

Nur wenn du bewusst **GitHub Actions** als Source willst:

1. Unter Pages zuerst **GitHub Actions** wählen und **Save** (einmalig).
2. [Actions → Deploy GitHub Pages → Run workflow](https://github.com/1337wheels-design/bm26/actions/workflows/pages.yml)

**Nicht** `configure-pages` mit `enablement: true` verwenden — das bricht nach ~5 s mit *Resource not accessible by integration* ab.