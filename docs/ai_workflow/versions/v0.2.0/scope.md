# Périmètre — v0.2.0

## Objectif

Étendre le socle cryptographique pour les consommateurs distants (`api`, `client`) :
JWKS distant avec cache, algorithmes ES256/EdDSA, et révocation enrichie côté
consommateur.

## Backlogs inclus

| ID | Titre | Priorité |
|----|-------|---------|
| BL-S-020-001 | Algorithmes ES256 et EdDSA | P0 |
| BL-S-020-002 | JWKS distant (extra httpx) | P0 |
| BL-S-020-003 | Cache JWKS en mémoire | P1 |
| BL-S-020-004 | Révocation enrichie consommateur | P1 |
| BL-S-020-005 | Tests, documentation et validation v0.2.0 | P1 |

## Intégration de validation

- `baobab-auth-core >= 0.4.0, < 1.0.0` (PyPI).
- Consommateurs obligatoires : `baobab-auth-api`, `baobab-auth-client`.

## Backlogs reportés

- Métadonnées clés et rotation pilotable → `v0.3.0`.
- Rotation refresh tokens et anti-rejeu → `v0.4.0`.
