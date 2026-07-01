# Changelog

Toutes les modifications notables de ce projet sont documentées ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### Ajouté

- **Intégration aval** : version `v0.1.0` proposée aux consommateurs via git-ref
  `version/v0.1.0` (`INTEGRATION_PENDING`) ; `baobab-auth-api` déclaré PENDING
  dans `docs/integrations/compatibility_matrix.yaml`.

### Ajouté (socle v0.1.0)

- **Socle du package `baobab_auth_security`** (BL-S-010-001) : layout `src/`,
  `py.typed`, `version.py`, hiérarchie d'exceptions (`SecurityError` racine),
  module `clock` (`Clock`, `SystemClock`, `FixedClock`, UTC aware).
- Dépendances runtime : `baobab-auth-core>=0.4.0,<1.0.0`, `argon2-cffi`,
  `cryptography`, `PyJWT`, `pydantic-settings`.
- Cahier des charges v0.1.0 intégré ; US-010/011/012, FEAT-010.x/011.1/012.x,
  ADR-0001 à 0006.
- **Module `password`** (BL-S-010-002) : `Argon2PasswordHasher` (Argon2id),
  `PasswordHashPolicy`, `PasswordHashResult` (masqué), `PasswordVerificationResult`,
  `needs_rehash` pour la migration des paramètres.
- **Module `tokens`** (BL-S-010-003) : JWT local RS256 — `JwtAlgorithm` (liste
  blanche RS256/384/512, refus `alg=none`), `SecurityTokenClaims`,
  `SecurityTokenPair` (masqué), `JwtEncoder`, `JwtDecoder`, `JwtValidator`
  (expiration/issuer/audience), `JwtTokenProvider`.
- **Module `refresh_tokens`** (BL-S-010-004) : `RefreshTokenGenerator` (token
  opaque `secrets`), `RefreshTokenHasher` (SHA-256, comparaison temps constant),
  `RefreshTokenResult` (clair masqué, hash stockable, dates UTC).
- **Modules `keys` et `jwks`** (BL-S-010-005) : `KeyAlgorithm`, `KeyStatus`,
  `KeyPair` (clé privée masquée), `KeyGenerator` (RSA ≥ 2048), `InMemoryKeyProvider`
  (signature + résolveur par `kid`), `PemKeyLoader` ; `JWK`/`JWKS`,
  `RsaPublicJwkConverter`, `LocalJwksProvider` (JWKS public sans clé privée).
- **Modules `revocation` et `integration`** (BL-S-010-006) :
  `RevocationChecker`/`InMemoryRevocationChecker` (par `jti`) ;
  `CorePasswordHasherAdapter`, `CoreTokenProviderAdapter`, `CoreClaimsMapper`,
  `CoreTokenPairMapper`, `CoreRevocationAdapter` conformes aux ports **réels**
  (synchrones) de `baobab-auth-core` (cf. ADR-0005). Tests d'intégration
  contractuels sous `tests/integration/core/`.
- **Configuration, testing, sécurité et documentation** (BL-S-010-007) :
  `SecuritySettings` (`pydantic-settings`, préfixe `BAOBAB_SECURITY_`),
  `SecurityTestHarness` (pile déterministe pour consommateurs),
  `tests/security/test_no_secret_leakage.py`, `docs/integration_core.md`,
  `docs/security.md`, `.env.example`, matrice de compatibilité (core `v0.5.1`).
