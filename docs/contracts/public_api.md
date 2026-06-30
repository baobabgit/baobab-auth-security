# Contrat — API publique

> Ce fichier documente les symboles exportés dans `__all__` de
> `baobab_auth_security`. Toute modification incompatible d'un symbole public
> déclenche un **bump SemVer majeur**.

## Symboles exportés (`v0.1.0`)

| Symbole | Type | Module | Spec |
|---------|------|--------|------|
| `__version__` | Constante | `version` | FEAT-012.1 |
| `SecurityError` (+ hiérarchie) | Exceptions | `exceptions` | FEAT-012.1 |
| `Clock`, `SystemClock`, `FixedClock` | Horloge | `clock` | FEAT-012.1 |
| `SecuritySettings` | Config | `config` | FEAT-012.2 |
| `Argon2PasswordHasher` | Classe | `password` | FEAT-010.1 |
| `PasswordHashPolicy` | Dataclass | `password` | FEAT-010.1 |
| `PasswordHashResult`, `PasswordVerificationResult` | Dataclass | `password` | FEAT-010.1 |
| `SecurityTokenClaims`, `SecurityTokenPair` | Dataclass | `tokens` | FEAT-010.2 |
| `JwtAlgorithm` | Enum | `tokens` | FEAT-010.2 |
| `JwtEncoder`, `JwtDecoder`, `JwtValidator`, `JwtTokenProvider` | Classe | `tokens` | FEAT-010.2 |
| `RefreshTokenGenerator`, `RefreshTokenHasher`, `RefreshTokenResult` | Classe | `refresh_tokens` | FEAT-010.3 |
| `KeyAlgorithm`, `KeyStatus` | Enum | `keys` | FEAT-010.4 |
| `KeyPair`, `KeyGenerator`, `InMemoryKeyProvider`, `PemKeyLoader` | Classe | `keys` | FEAT-010.4 |
| `JWK`, `JWKS`, `RsaPublicJwkConverter`, `LocalJwksProvider` | Classe | `jwks` | FEAT-010.4 |
| `RevocationChecker`, `InMemoryRevocationChecker` | Révocation | `revocation` | FEAT-011.1 |
| `CorePasswordHasherAdapter`, `CoreTokenProviderAdapter` | Adaptateur | `integration` | FEAT-011.1 |
| `CoreClaimsMapper`, `CoreTokenPairMapper`, `CoreRevocationAdapter` | Adaptateur | `integration` | FEAT-011.1 |
| `SecurityTestHarness` | Aide de test | `testing` | FEAT-012.2 |

## Règle de rupture de contrat

- Suppression d'un symbole public → **MAJOR bump**
- Changement de signature incompatible → **MAJOR bump**
- Ajout d'un paramètre obligatoire → **MAJOR bump**
- Ajout d'un symbole → **MINOR bump**
- Correction de comportement sans rupture → **PATCH bump**
