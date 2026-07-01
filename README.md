# baobab-auth-security

[![CI](https://github.com/baobabgit/baobab-auth-security/actions/workflows/ci.yml/badge.svg)](https://github.com/baobabgit/baobab-auth-security/actions/workflows/ci.yml)
[![Integration](https://github.com/baobabgit/baobab-auth-security/actions/workflows/integration.yml/badge.svg)](https://github.com/baobabgit/baobab-auth-security/actions/workflows/integration.yml)
[![Release](https://github.com/baobabgit/baobab-auth-security/actions/workflows/release.yml/badge.svg)](https://github.com/baobabgit/baobab-auth-security/actions/workflows/release.yml)
[![PyPI version](https://img.shields.io/pypi/v/baobab-auth-security.svg)](https://pypi.org/project/baobab-auth-security/)
[![Python versions](https://img.shields.io/pypi/pyversions/baobab-auth-security.svg)](https://pypi.org/project/baobab-auth-security/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

> Brique technique de **sécurité** de l'écosystème [`baobab-auth`](https://github.com/baobabgit).
> Elle fournit les implémentations concrètes que `baobab-auth-core` ne porte pas :
> hachage Argon2id, JWT signés localement (RS256), refresh tokens opaques, clés RSA
> et JWKS public local, plus des **adaptateurs stricts** vers les ports du core.

## Table des matières

- [Positionnement](#positionnement)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Qualité](#qualité)
- [Tests](#tests)
- [Release](#release)
- [Intégration inter-briques](#intégration-inter-briques)
- [Sécurité](#sécurité)
- [Licence](#licence)

## Positionnement

`baobab-auth-security` est **indépendante** de l'API HTTP, de la base SQL et des
applications métier. Elle **n'embarque ni** FastAPI, SQLAlchemy, Alembic, psycopg,
asyncpg, redis, uvicorn **ni** logique métier.

| Module | Responsabilité |
|--------|----------------|
| `password` | `Argon2PasswordHasher`, `PasswordHashPolicy`, résultats typés |
| `tokens` | `SecurityTokenClaims`, `SecurityTokenPair`, `JwtEncoder/Decoder/Validator`, `JwtTokenProvider` |
| `refresh_tokens` | `RefreshTokenGenerator`, `RefreshTokenHasher`, `RefreshTokenResult` |
| `keys` | `KeyAlgorithm`, `KeyStatus`, `KeyPair`, `KeyGenerator`, `InMemoryKeyProvider`, loader PEM |
| `jwks` | `JWK`, `JWKS`, `LocalJwksProvider`, conversion RSA publique |
| `revocation` | `InMemoryRevocationChecker` (par `jti`) |
| `integration` | adaptateurs et mappers vers `baobab-auth-core` |
| `clock` | `Clock`, `SystemClock`, `FixedClock` (UTC) |
| `config` | `SecuritySettings` (`pydantic-settings`) |

## Installation

```bash
uv add baobab-auth-security        # ou : pip install baobab-auth-security
```

Dépendances runtime : `baobab-auth-core>=0.4.0,<1.0.0`, `argon2-cffi`,
`cryptography`, `PyJWT`, `pydantic-settings`. Python ≥ 3.13.

## Usage

> ⚠️ v0.1.0 — socle MVP. Les exemples complets (hachage, émission JWT, JWKS,
> adaptateurs core) sont documentés dans [`docs/`](docs/) au fil des modules.

```python
from datetime import UTC, datetime
from baobab_auth_security import SystemClock, FixedClock

clock = SystemClock()
assert clock.now().tzinfo is not None          # toujours UTC aware

# Horloge déterministe pour les tests
fixed = FixedClock(datetime(2026, 1, 1, tzinfo=UTC))
assert fixed.now() == datetime(2026, 1, 1, tzinfo=UTC)
```

## Configuration

La configuration est **injectée** via `pydantic-settings` (aucun état global).
Voir [`.env.example`](.env.example) et `SecuritySettings` (préfixe `BAOBAB_SECURITY_`).

## Qualité

```bash
uv run black --check src tests
uv run ruff check src tests
uv run mypy src
uv run bandit -r src -c pyproject.toml
```

## Tests

```bash
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=95
```

Couverture globale ≥ 95 % imposée. Suites : `tests/unit/`, `tests/integration/`,
`tests/security/`, `tests/contracts/`.

## Release

```bash
uv build
uv run twine check dist/*
```

Modèle de branches : `main → version/vX.Y.Z → bl/XXX-description`. Tag `vX.Y.Z`
sur `main` après validation interne et d'intégration.

## Intégration inter-briques

Matrice de compatibilité :
[`docs/integrations/compatibility_matrix.yaml`](docs/integrations/compatibility_matrix.yaml).
v0.1.0 valide l'intégration contractuelle avec **`baobab-auth-core >=0.4.0,<1.0.0`**
(validé contre `v0.5.1`). Détails : [`docs/integration_core.md`](docs/integration_core.md).

**Intégration aval (`INTEGRATION_PENDING`)** — ref proposée `version/v0.1.0` ;
intégration active **en attente** (gate) tant que `baobab-auth-api`,
`baobab-auth-client` et `baobab-auth-admin` n'ont pas validé
`baobab-auth-core v0.5.1`. Voir
[`docs/integrations/integration_gate.md`](docs/integrations/integration_gate.md).

Quand le gate est levé, les consommateurs testent via :

```bash
uv add "baobab-auth-security @ git+https://github.com/baobabgit/baobab-auth-security.git@version/v0.1.0"
```

Consommateur cible v0.1.0 : `baobab-auth-api` (login, refresh, JWKS local).

## Sécurité

- **Aucun secret** dans le code ou Git (`.env` gitignoré, `.env.example` versionné).
- Mots de passe, refresh tokens, access tokens et clés privées **masqués** dans
  `repr`/`str`/logs/exceptions ; JWKS **public uniquement**.
- `alg=none` et les algorithmes hors liste blanche sont **refusés**.
- Politique : [`docs/security.md`](docs/security.md) et [`SECURITY.md`](SECURITY.md).

## Licence

Distribué sous licence **MIT**. Voir [`LICENSE`](LICENSE).
