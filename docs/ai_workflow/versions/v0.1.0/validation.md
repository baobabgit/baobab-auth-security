# Validation interne — v0.1.0

## Critères

- [x] Tous les backlogs mergés sur `version/v0.1.0`
- [x] `make all` passe (qualité + tests ≥ 95 % + build)
- [x] `make traceability` passe sans erreur
- [x] CHANGELOG.md à jour
- [x] Badges README cohérents

## Résultat

Status : **INTERNAL_VALIDATED** (2026-06-30)

- 7 backlogs mergés (BL-S-010-001 → BL-S-010-007).
- Dernière PR : #19.
- Couverture : 100 % (169 tests).
- Intégration core `v0.5.1` : PASSED (rapport dans `docs/integrations/reports/`).

## Intégration aval (producteur)

Status : **INTEGRATION_PENDING** (2026-06-30)

- Ref git proposée : `version/v0.1.0`
- Consommateur déclaré : `baobab-auth-api` (PENDING)
- Matrice : `docs/integrations/compatibility_matrix.yaml`

### Gate actif (décision 2026-06-30)

**Attente** optionnelle de la validation `baobab-auth-core v0.5.1` par
`baobab-auth-api`, `baobab-auth-client` et `baobab-auth-admin` avant
l'intégration aval security → api. **Non bloquant** pour la release PyPI v0.1.0.

Détail : [`docs/integrations/integration_gate.md`](../../integrations/integration_gate.md)

## Release

Status : **RELEASE_READY** (2026-06-30)

- Merge `version/v0.1.0` → `main` puis tag `v0.1.0` → `release.yml` (PyPI + GitHub).
