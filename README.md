# itmitkopf-website

Statische Website für **IT mit Kopf** (https://itmitkopf.de): reines HTML, CSS und minimales JavaScript, kein Build-Schritt.

- `public/` – wird ausgeliefert (Webroot des Nginx-Containers). Nur dieser Ordner ist öffentlich erreichbar.
- `brand/` – Logo-Generator und Vorschau (nicht Teil der Auslieferung).
- Schriften (Space Grotesk, DM Sans, IBM Plex Mono; SIL OFL) liegen lokal unter `public/assets/fonts/`. Es werden keine externen Ressourcen geladen.
- Hell-/Dunkel-Modus: folgt dem System, Umschalter speichert die Wahl nur lokal im Browser.

## Arbeitsweise

Änderungen laufen über Branches (`feat/…`, `fix/…`) und Pull Requests; `main` ist die Produktion. Releases sind Git-Tags (`v1.x.y`) und dienen als Rollback-Punkte.

**Keine Secrets, Zugangsdaten oder `.env`-Dateien einchecken.** Das Repository ist öffentlich.
