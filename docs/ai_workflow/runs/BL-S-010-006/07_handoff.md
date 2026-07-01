# Handoff — BL-S-010-006

## État

Modules `revocation` et `integration` livrés et validés localement (couverture
100 %, intégration contractuelle verte). PR vers `version/v0.1.0`.

## Acquis réutilisables

- `CorePasswordHasherAdapter` / `CoreTokenProviderAdapter` : prêts à être injectés
  dans `baobab-auth-core` (ports `PasswordHasher` / `TokenProvider`).
- `CoreClaimsMapper` / `CoreTokenPairMapper` : pour `baobab-auth-client` / API.

## Prochaine étape

BL-S-010-007 (dernier backlog) : `SecuritySettings` (config injectée), module
`testing`, `tests/security/test_no_secret_leakage.py`, documentation MVP
(`README`, `CHANGELOG`, `docs/integration_core.md`, `docs/security.md`), matrice
de compatibilité. Puis validation interne + intégration (Phase D).
