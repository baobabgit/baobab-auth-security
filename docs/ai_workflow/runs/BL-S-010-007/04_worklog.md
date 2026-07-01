# Worklog — BL-S-010-007

- `config/security_settings.py` : `SecuritySettings` (`pydantic-settings`, préfixe
  `BAOBAB_SECURITY_`) ; dérive `PasswordHashPolicy`, `JwtAlgorithm`, `KeyAlgorithm`.
- `testing/security_test_harness.py` : `SecurityTestHarness` (horloge fixe, clé
  RSA en mémoire, provider JWT, adaptateurs core, JWKS) — pile prête pour les
  consommateurs.
- `tests/security/test_no_secret_leakage.py` : non-fuite de mot de passe brut,
  refresh token brut, access token complet, clé privée ; dates UTC.
- Documentation : `docs/integration_core.md`, `docs/security.md`, `.env.example`,
  `docs/contracts/public_api.md`, matrice `compatibility_matrix.yaml`
  (dépendance `baobab-auth-core v0.5.1`).

## Décisions

- `SecurityTestHarness` mutualise le câblage répété dans les tests ; exporté dans
  le contrat public pour les briques consommatrices.
