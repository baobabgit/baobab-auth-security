# Intégration avec `baobab-auth-core`

`baobab-auth-security` fournit les implémentations concrètes des ports de
`baobab-auth-core`. Cette page décrit l'intégration de la version `v0.1.0`.

## Version minimale

| Brique | Contrainte | Validé contre |
|--------|-----------|---------------|
| `baobab-auth-core` | `>=0.4.0,<1.0.0` | `v0.5.1` |

## Écart par rapport au cahier des charges (ADR-0005)

Le cahier décrit des ports **idéalisés et asynchrones**
(`async def issue_token_pair(...) -> TokenPair`). Les ports **réels** publiés par
`baobab-auth-core` sont **synchrones** et plus granulaires. Conformément à
`AGENTS.md` (« utiliser les types réels du core »), les adaptateurs implémentent
les ports réels :

```python
# baobab_auth_core.ports.password_hasher.PasswordHasher (réel, synchrone)
def hash(self, password: PlainPassword) -> PasswordHash: ...
def verify(self, password: PlainPassword, password_hash: PasswordHash) -> bool: ...

# baobab_auth_core.ports.token_provider.TokenProvider (réel, synchrone)
def generate_token_id(self) -> TokenId: ...
def create_access_token(self, subject, ttl_seconds, claims=None) -> str: ...
def verify_access_token(self, token) -> dict[str, Any]: ...
def create_refresh_token(self, subject, token_id, ttl_seconds, claims=None) -> str: ...
def verify_refresh_token(self, token) -> dict[str, Any]: ...
def revoke_token(self, token) -> None: ...
```

Le port `PasswordHasher` du core n'expose **pas** `needs_rehash` : cette capacité
reste disponible sur `Argon2PasswordHasher` (service technique), hors contrat
d'adaptateur.

## Adaptateurs fournis

| Adaptateur | Port / VO du core |
|------------|-------------------|
| `CorePasswordHasherAdapter` | `ports.password_hasher.PasswordHasher` |
| `CoreTokenProviderAdapter` | `ports.token_provider.TokenProvider` |
| `CoreClaimsMapper` | `application.results.token_claims.TokenClaims` |
| `CoreTokenPairMapper` | `application.results.token_pair.TokenPair` |
| `CoreRevocationAdapter` | `domain.value_objects.token_id.TokenId` |

Les exceptions de vérification sont traduites vers
`baobab_auth_core.exceptions.auth.TokenInvalidError` / `TokenExpiredError`.

## Exemple de câblage

```python
from datetime import UTC, datetime
from baobab_auth_core.domain.value_objects.plain_password import PlainPassword
from baobab_auth_security.testing import SecurityTestHarness

harness = SecurityTestHarness(datetime(2026, 1, 1, tzinfo=UTC))

# Mots de passe (port PasswordHasher du core)
hasher = harness.password_hasher_adapter
digest = hasher.hash(PlainPassword("s3cret"))
assert hasher.verify(PlainPassword("s3cret"), digest)

# Tokens (port TokenProvider du core)
tokens = harness.token_provider_adapter
access = tokens.create_access_token("user-1", 900, {"roles": ["ADMIN"]})
claims = tokens.verify_access_token(access)  # -> dict

# JWKS public (pour /auth/jwks)
jwks = harness.jwks_provider.jwks().to_dict()
```

## Refresh tokens

L'adaptateur `CoreTokenProviderAdapter` émet les refresh tokens en **JWT signés
auto-portants** (modèle du port `create_refresh_token` / `verify_refresh_token`).
Le **générateur opaque** (`RefreshTokenGenerator`, hash SHA-256) reste disponible
pour les flux gérés par l'API/database (stockage du hash, ADR-0004).
