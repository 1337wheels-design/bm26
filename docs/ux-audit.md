# UI/UX-Audit — Dolomiten Planner (`dolomiten.html`)

Stand: 26.11.2026 (nach Umsetzung der Quick Wins)

## Nutzer & Kontext

- Zielgruppe: 2 Erwachsene, Planung unterwegs (Mobile), keine Anmeldung, localStorage.
- Hauptflow: Long-List → Short-List/Route → Präsentation.

## Stärken (unverändert gut)

| Bereich | Bewertung |
|--------|-----------|
| Klare Tabs + Funnel-Zähler | Orientierung im Prozess |
| Gewichtungsslider mit Live-Sortierung | Gute „Discovery“-Mechanik |
| Dark Mode via `prefers-color-scheme` | Barrierefreiheit Basis |
| Keine externen Tracker | Datenschutz & CSP schlank |
| Reliefkarte + Presets A–G | Raumliche und inhaltliche Helfer |

## Probleme (vorher) → Maßnahmen

| Problem | Schwere | Maßnahme |
|--------|---------|----------|
| Tagesplan: lange Kartenwand, viel Scroll | Hoch | Gesamtbereich + Einzeltage in `<details>`, Standard zu |
| Doppelte Karte auf Short-List | Mittel | Eine Karte in aufklappbarem Block; Zeitplan nur Timeline |
| Karte vor Prioritäten auf Long-List | Mittel | Karte unter Filter, eingeklappt |
| München 29.11. als Default-Hinreise wirkte wie Reisebeginn | Hoch | Standard: **Mo 30.11.** Abfahrt Bremen; München optional (So 29.11.) |
| Kleine Touch-Targets (`.btn.small`) | Mittel | Mobile `min-height: 44px` |
| Kein Skip-Link | Niedrig | „Zum Inhalt“ ergänzt |
| Navigation scrollt weg | Mittel | Sticky Header |
| Wochentage in UI uneinheitlich | Niedrig | `fmtDate` / `fmtDateLong` überall |

## Mobile (Stand 26.11. – nachgebessert)

- Kompakter **Sticky-Header** (kleinere Titelzeile, Meta gekürzt).
- **Funnel** + **Tab-Leiste** horizontal wischbar, kurze Tab-Labels („Route“, „Folien“).
- **Short-List-Tabelle**: mobil nur Ort + Passung; Kriterien ab Tablet/desktop oder Querformat.
- Reliefkarte auf Mobile **eingeklappt** (Standard).
- Preset-Buttons enger („Karte“ statt „Auf Karte zeigen“).

## Offen / nächste Iteration

1. **Short-List-Tab Reihenfolge**: Route-Builder vor Presets platzieren (aktuell Presets zuerst) — bei Bedarf tauschen.
2. **Ort-Karten Long-List**: Viele Fotos/Links — optional „Nur Kurzansicht“-Toggle global.
3. **Präsentation**: Stationsfolien weiterhin textlastig — Wanderungen/Highlights dort auch in `<details>`.
4. **Karten-Popup**: Viele Buttons — primäre Aktion „Bündel übernehmen“ visuell stärker, Rest sekundär.
5. **Tastatur**: Map-Pins fokussierbar (ok), aber kein Escape zum Schließen des Popups.
6. **Offline / file://**: `manifest.json`-Fetch scheitert still — Hinweis-Banner wenn Bilder fehlen.
7. **Performance**: 19 Orte × Medien — Lazy loading Bilder ist aktiv; Long-List Virtualisierung nur nötig bei >50 Karten.

## Heuristiken (Nielsen, Kurz)

- **Sichtbarkeit des Status**: Funnel + Nächte-Zähler ✓
- **Nutzerkontrolle**: Export/Import, Transit-Checkboxen ✓
- **Konsistenz**: Wochentage jetzt einheitlicher ✓
- **Fehlerprävention**: Route-Nacht-Limit mit Warnung ✓
- **Hilfe**: Rahmen-Tab mit Checkliste ✓; Tooltips für Karte knapp ausreichend

## Messung (manuell empfohlen)

- [ ] iPhone Viewport 390px: Short-List ohne horizontales Scrollen außer Tabellen
- [ ] Tagesplan eingeklappt: < 2 Bildschirmhöhen bis Route-Ende
- [ ] Lighthouse Accessibility ≥ 90 (inline-App, keine Form-Labels überall)