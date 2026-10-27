# deploy/

Entwürfe für den Betrieb auf vps01. Nicht Teil der ausgelieferten Website (nur `public/` wird ausgeliefert).

- `nginx/default.conf` – Nginx-Konfiguration (kein Access-Log, 404-Seite, 301 für alte URLs, Caching, gzip).
  Wird auf dem Host unter `/opt/containers/hawser/itmitkopf-conf/default.conf` abgelegt (im Hawser-Container: `/opt/hawser-stacks/itmitkopf-conf/default.conf`).
- `compose.staging.yaml` – Teststack ohne Traefik-Labels (nur intern erreichbar), zieht den Branch `feat/initial-site`.
- `compose.yaml` – Produktionsstack mit `git-sync`-Sidecar (zieht `main` alle 60 Minuten).

Reihenfolge: Teststack prüfen, dann Merge nach `main`, dann Produktionsstack. Änderungen am Produktivsystem erfolgen nur nach ausdrücklicher Freigabe.
