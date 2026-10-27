# deploy/

Entwürfe für den Betrieb auf vps01. Nicht Teil der ausgelieferten Website (nur `public/` wird ausgeliefert).

- `nginx/default.conf` – Nginx-Konfiguration (kein Access-Log, 404-Seite, Redirects der alten URLs, Caching, gzip)
- `compose.yaml` – Stack mit `git-sync`-Sidecar (zieht `main` alle 60 Minuten)

Status: Entwurf, noch nicht angewendet. Änderungen am Produktivsystem erfolgen erst nach ausdrücklicher Freigabe.
