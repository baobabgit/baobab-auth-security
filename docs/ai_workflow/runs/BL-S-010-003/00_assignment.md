# Assignment — BL-S-010-003

- **Backlog :** BL-S-010-003 — Implémenter JWT local RS256
- **FEAT :** FEAT-010.2 (US-010)
- **Version :** v0.1.0
- **Rôle :** Développeur Python
- **Branche :** `bl/S-010-003-jwt-rs256` (depuis `version/v0.1.0`)

## Objectif

Émettre et valider des access tokens JWT signés localement en RS256, avec
durcissement (`alg=none` refusé, liste blanche), claims structurés et clés
injectées (découplé du module `keys`).
