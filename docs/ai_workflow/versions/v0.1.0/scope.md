# Périmètre — v0.1.0

## Objectif

Socle MVP de sécurité technique : hachage Argon2id, JWT local RS256, refresh
tokens opaques, clés RSA + JWKS public local, et adaptateurs stricts vers les
ports réels de `baobab-auth-core` (≥ 0.4.0). Garantie de non-fuite des secrets.

## Backlogs inclus

| ID | Titre | Priorité |
|----|-------|---------|
| BL-S-010-001 | Initialiser le package | P0 |
| BL-S-010-002 | Hash de mot de passe Argon2id | P0 |
| BL-S-010-003 | JWT local RS256 | P0 |
| BL-S-010-004 | Refresh tokens opaques | P1 |
| BL-S-010-005 | Clés RSA et JWKS local | P0 |
| BL-S-010-006 | Adaptateurs core | P0 |
| BL-S-010-007 | Tests sécurité et documentation MVP | P1 |

## Intégration de validation

- `baobab-auth-core >= 0.4.0, < 1.0.0` (validé contre `v0.5.1`) — tests d'intégration
  contractuels (ports réels `PasswordHasher` / `TokenProvider`).
- Validation exploratoire recommandée avec un prototype `baobab-auth-api`.

## Backlogs reportés

- JWKS distant, cache, ES256/EdDSA → `v0.2.0`.
- Rotation pilotable, anti-rejeu, familles de refresh tokens → `v0.3.0` / `v0.4.0`.
