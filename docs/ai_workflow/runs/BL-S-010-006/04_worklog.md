# Worklog — BL-S-010-006

## Module `revocation`

- `revocation_checker.py` : `RevocationChecker` (Protocol runtime_checkable).
- `in_memory_revocation_checker.py` : `InMemoryRevocationChecker` (set de `jti`).

## Module `integration`

- `core_password_hasher_adapter.py` : `CorePasswordHasherAdapter` (port réel
  `PasswordHasher`).
- `core_token_provider_adapter.py` : `CoreTokenProviderAdapter` (port réel
  `TokenProvider`, 6 méthodes ; `verify_*` → `dict` ; traduction des exceptions
  vers `TokenInvalidError`/`TokenExpiredError` du core ; révocation par `jti`).
- `core_claims_mapper.py` / `core_token_pair_mapper.py` : mapping vers les VO
  réels du core (`TokenClaims`, `TokenPair`), sans recalcul rôle → permissions.
- `core_revocation_adapter.py` : `CoreRevocationAdapter` (traduit `TokenId` ⇄ `jti`).

## Décisions

- Conformité aux ports **réels synchrones** du core (ADR-0005), vérifiée par
  `isinstance` (runtime_checkable) en intégration.
- L'adaptateur émet les refresh tokens en **JWT signés auto-portants** (modèle du
  port `create_refresh_token`/`verify_refresh_token`) ; le générateur opaque
  (`refresh_tokens`) reste disponible pour les flux gérés par l'API/database.
- `pyproject` : ajout `--import-mode=importlib` (bases de noms de tests dupliquées
  unit/intégration) et exclusion couverture des stubs `...` de Protocol.
