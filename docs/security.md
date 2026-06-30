# Sécurité — `baobab-auth-security`

## Règles transverses (garanties et testées)

- Ne jamais logger de **mot de passe brut**, de **refresh token brut** ni
  d'**access token complet**.
- Ne jamais exposer de **clé privée** dans `repr`, `str`, exception, log, JWKS,
  métrique ou audit.
- **Refuser `alg=none`** et tout algorithme non explicitement autorisé
  (liste blanche `RS256`/`RS384`/`RS512`).
- Utiliser uniquement des **datetimes timezone-aware en UTC**.
- Fournir des tests **positifs et négatifs** pour chaque règle.

Ces invariants sont vérifiés par `tests/security/test_no_secret_leakage.py`
(non-régression) et complétés par l'analyse statique `bandit`.

## Masquage des secrets

| Objet | Champ masqué |
|-------|--------------|
| `PasswordHashResult` | hash (`repr`/`str` → `***`) |
| `RefreshTokenResult` | token en clair + hash |
| `SecurityTokenPair` | access + refresh tokens |
| `KeyPair` | clé privée (`private_key='***'`) |

Le JWKS public ne contient que `kty`, `use`, `alg`, `kid`, `n`, `e` — jamais
`d`, `p`, `q`.

## Algorithmes

| Algorithme | Statut |
|------------|--------|
| `RS256` (défaut) | Autorisé |
| `RS384`, `RS512` | Autorisés |
| `none` | **Refusé** |
| `HS*`, `ES*`, `EdDSA` | Hors périmètre v0.1.0 (refusés) |

## Variables de configuration

Préfixe : `BAOBAB_SECURITY_` (chargées via `pydantic-settings`).

| Variable | Défaut | Description |
|----------|--------|-------------|
| `ISSUER` | `None` | Émetteur (`iss`) |
| `AUDIENCE` | `None` | Audience (`aud`) |
| `ALGORITHM` | `RS256` | Algorithme de signature |
| `ACCESS_TTL_SECONDS` | `900` | TTL access token |
| `REFRESH_TTL_SECONDS` | `1209600` | TTL refresh token |
| `KEY_SIZE` | `2048` | Taille des clés RSA |
| `ARGON2_TIME_COST` | `3` | Coût temps Argon2 |
| `ARGON2_MEMORY_COST` | `65536` | Coût mémoire Argon2 (KiB) |
| `ARGON2_PARALLELISM` | `4` | Parallélisme Argon2 |

## Dépendances

- **Runtime obligatoires** : `baobab-auth-core`, `argon2-cffi`, `cryptography`,
  `PyJWT`, `pydantic-settings`.
- **Optionnelles** (versions ultérieures) : `httpx` (JWKS distant, ≥ v0.2.0),
  `redis` (cache distribué, ≥ v0.6.0).
- **Interdites** en runtime obligatoire : `fastapi`, `sqlalchemy`, `alembic`,
  `psycopg`, `asyncpg`, `redis`, `uvicorn`, `docker`.

## Limites de la version `v0.1.0`

- JWKS **local** uniquement (pas de JWKS distant ni de cache — v0.2.0).
- Pas de rotation pilotable des clés ni d'anti-rejeu de refresh tokens
  (v0.3.0 / v0.4.0).
- Algorithmes RSA uniquement (ES256/EdDSA en v0.2.0).
- Signalez toute vulnérabilité en privé (voir [`SECURITY.md`](../SECURITY.md)).
