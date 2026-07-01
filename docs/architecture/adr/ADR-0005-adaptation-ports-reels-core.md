# ADR-0005 — Adaptation aux ports réels (synchrones) de `baobab-auth-core`

- **Statut :** Accepté
- **Date :** 2026-06-29
- **Version :** v0.1.0
- **Backlog :** BL-S-010-006 (FEAT-011.1)

## Contexte

Le cahier des charges (section 7) décrit des `Protocol` **idéalisés** et
**asynchrones** :

```python
class PasswordHasher(Protocol):
    async def hash(self, plain_password: PlainPassword) -> PasswordHash: ...
    async def verify(...) -> bool: ...
    async def needs_rehash(...) -> bool: ...

class TokenProvider(Protocol):
    async def issue_token_pair(self, context: TokenIssueContext) -> TokenPair: ...
    async def verify_access_token(self, raw_token: str) -> TokenClaims: ...
    async def verify_refresh_token(self, raw_token: str) -> TokenClaims: ...
    async def revoke_token(self, token_id: TokenId) -> None: ...
```

Or les ports **réels** publiés par `baobab-auth-core` 0.5.1 sont **synchrones**
et de signatures différentes :

```python
class PasswordHasher(Protocol):            # baobab_auth_core.ports.password_hasher
    def hash(self, password: PlainPassword) -> PasswordHash: ...
    def verify(self, password: PlainPassword, password_hash: PasswordHash) -> bool: ...

class TokenProvider(Protocol):             # baobab_auth_core.ports.token_provider
    def generate_token_id(self) -> TokenId: ...
    def create_access_token(self, subject, ttl_seconds, claims=None) -> str: ...
    def verify_access_token(self, token: str) -> dict[str, Any]: ...
    def create_refresh_token(self, subject, token_id, ttl_seconds, claims=None) -> str: ...
    def verify_refresh_token(self, token: str) -> dict[str, Any]: ...
    def revoke_token(self, token: str) -> None: ...
```

La règle AGENTS.md prévaut : « utiliser les types réels du core si disponibles ;
documenter tout écart ».

## Décision

- Les adaptateurs `CorePasswordHasherAdapter` et `CoreTokenProviderAdapter`
  implémentent les ports **réels** (synchrones) du core, vérifiés via
  `runtime_checkable` dans les tests d'intégration.
- `PasswordHasher` du core n'expose **pas** `needs_rehash` ; cette capacité reste
  disponible sur le service technique `Argon2PasswordHasher` mais hors contrat
  d'adaptateur core.
- `verify_access_token` / `verify_refresh_token` retournent un `dict` (payload
  décodé), conformément au port réel. `CoreClaimsMapper` fournit en plus la
  conversion vers le VO `TokenClaims` du core pour les consommateurs qui le
  souhaitent (ex. `baobab-auth-client`).
- `CoreTokenPairMapper` produit le `TokenPair` réel du core
  (`access_token`, `refresh_token`, `token_type`, `expires_in`,
  `refresh_expires_in`).
- Les value objects du core (`PlainPassword`, `PasswordHash`, `TokenId`,
  `TokenClaims`, `TokenPair`, `AuthSubject`, `RoleName`, `PermissionName`,
  `SessionId`) sont **réutilisés**, jamais redéfinis.

## Conséquences

- L'intégration runtime est réelle et testée contre le port publié.
- Si le core publie ultérieurement des ports async ou un `issue_token_pair`, un
  nouvel adaptateur sera ajouté sans rupture (ADR de suivi).
