    # Cahier des charges — `baobab-auth-security` — version `v0.1.0`

    **Projet :** `baobab-auth-security`  
    **Version cible :** `v0.1.0`  
    **Titre :** Socle sécurité minimal, intégration core et JWT local  
    **Destination :** IA de développement  
    **Format :** Markdown  
    **Statut :** cahier des charges versionné  

    ---


## 1. Contexte et positionnement

`baobab-auth-security` est la brique technique de sécurité de l’écosystème `baobab-auth`. Elle fournit les implémentations concrètes que `baobab-auth-core` ne doit pas porter : hash de mot de passe, vérification de mot de passe, génération et validation de JWT, refresh tokens opaques, hash de refresh tokens, JWKS, génération et rotation de clés, et vérifications de révocation.

La librairie doit rester indépendante de l’API HTTP, de la base SQL et des applications métier. Elle ne doit pas contenir de routes FastAPI, de modèles SQLAlchemy, de migrations Alembic, de dépendance PostgreSQL obligatoire, ni de logique spécifique Riftbound, Altered ou autre application consommatrice.

### Dépendances autorisées et interdites

Dépendances runtime autorisées selon les versions :

```text
baobab-auth-core
argon2-cffi
cryptography
PyJWT
pydantic ou dataclasses standard selon choix du projet
typing-extensions si nécessaire
httpx en extra optionnel pour JWKS distant ou discovery
redis en extra optionnel à partir de v0.6.0 uniquement
```

Dépendances interdites en dépendance obligatoire :

```text
fastapi
sqlalchemy
alembic
psycopg
asyncpg
redis
uvicorn
docker
```

### Règles transverses de sécurité

- Ne jamais logger de mot de passe brut.
- Ne jamais logger de refresh token brut.
- Ne jamais logger d’access token complet.
- Ne jamais exposer de clé privée dans `repr`, `str`, exception, log, JWKS, métrique ou audit.
- Refuser `alg=none`.
- Refuser tout algorithme non explicitement autorisé.
- Utiliser uniquement des datetimes timezone-aware en UTC.
- Fournir des tests positifs et négatifs pour chaque règle de sécurité.
- Garder les services techniques plus riches possibles, mais exposer des adaptateurs stricts vers les ports du core.



## 2. Matrice d’intégration inter-briques

Cette matrice indique à partir de quelle version `baobab-auth-security` doit être intégrée à d’autres librairies pour valider réellement la version.

| Version security | Intégration `baobab-auth-core` | Intégration obligatoire pour validation de la version | Objectif de validation croisée |
|---|---|---|---|
| `v0.1.0` | Oui, `baobab-auth-core >=0.4.0,<1.0.0` | `baobab-auth-core`, puis prototype `baobab-auth-api` | Valider `PasswordHasher`, `TokenProvider`, claims et token pair. |
| `v0.2.0` | Oui | `baobab-auth-client` et `baobab-auth-api` | Valider JWKS distant, cache, algorithmes ES256/EdDSA et révocation enrichie côté consommateur. |
| `v0.3.0` | Oui | `baobab-auth-database`, `baobab-auth-admin` | Valider stockage externe des métadonnées de clés et rotation pilotable. |
| `v0.4.0` | Oui | `baobab-auth-database`, `baobab-auth-api` | Valider rotation des refresh tokens, anti-rejeu et révocation de famille. |
| `v0.5.0` | Oui | `baobab-auth-api`, `baobab-auth-client` | Valider profils de tokens, audiences multiples et tokens de service. |
| `v0.6.0` | Oui | `baobab-auth-service`, `baobab-auth-api`, `baobab-auth-client` | Valider cache distribué optionnel, résilience et observabilité. |
| `v0.7.0` | Oui | `baobab-auth-api`, `baobab-auth-client` | Valider discovery interne ou OIDC limitée. |
| `v0.8.0` | Oui | `baobab-auth-admin`, `baobab-auth-service` | Valider politiques crypto et rapports de conformité. |
| `v0.9.0` | Oui | Toutes les briques `core`, `database`, `api`, `client`, `admin`, `service` | Release candidate et non-régression inter-briques complète. |
| `v1.0.0` | Oui, version stable compatible `core >=1.0.0,<2.0.0` ou matrice documentée | Toutes les briques | Validation stable production de l’écosystème. |

Règle importante : `baobab-auth-security` intègre `baobab-auth-core` dès `v0.1.0`, mais cette intégration suppose que le core expose déjà ses ports stables `PasswordHasher` et `TokenProvider`, ainsi que les value objects associés. Le seuil recommandé est donc `baobab-auth-core >=0.4.0`.


    ## 3. Positionnement de la version `v0.1.0`

    ```text
    v0.1.0 → Socle MVP de sécurité technique
    ```

    ### 3.1 Intégration avec `baobab-auth-core`

    Intégration obligatoire dès cette version avec `baobab-auth-core >=0.4.0,<1.0.0` via adaptateurs `PasswordHasher` et `TokenProvider`.

    ### 3.2 Intégration à réaliser pour valider cette version

    À valider avec `baobab-auth-core` en tests d’intégration contractuels. Une validation exploratoire avec `baobab-auth-api v0.1.0` est recommandée pour login, refresh et JWKS local.

    ## 4. Objectifs fonctionnels

    - Créer le package Python `baobab_auth_security` en structure `src/`.
- Fournir le hash Argon2id des mots de passe et la vérification sécurisée.
- Générer et valider des JWT signés localement en RS256 par défaut.
- Générer des refresh tokens opaques et leurs hashes.
- Générer des clés RSA et publier un JWKS local public.
- Fournir des adaptateurs stricts vers les ports du core.
- Garantir l’absence de fuite de secrets dans logs, exceptions et représentations.

    ## 5. Architecture cible

    | Module | Responsabilité |
|---|---|
| `password` | Argon2PasswordHasher, PasswordHashPolicy, PasswordHashResult, PasswordVerificationResult. |
| `tokens` | SecurityTokenClaims, SecurityTokenPair, JwtEncoder, JwtDecoder, JwtValidator, JwtTokenProvider. |
| `refresh_tokens` | RefreshTokenGenerator, RefreshTokenHasher, RefreshTokenResult. |
| `keys` | KeyAlgorithm RS256/RS384/RS512, KeyStatus, KeyPair, KeyGenerator, InMemoryKeyProvider, PEM loader. |
| `jwks` | JWK, JWKS, JwksProvider local, conversion RSA publique. |
| `revocation` | InMemoryRevocationChecker minimal par `jti`. |
| `integration` | CorePasswordHasherAdapter, CoreTokenProviderAdapter, CoreClaimsMapper, CoreTokenPairMapper. |
| `clock` | Clock, SystemClock, FixedClock. |

    Arborescence recommandée :

    ```text
    baobab-auth-security/
    ├── pyproject.toml
    ├── README.md
    ├── CHANGELOG.md
    ├── LICENSE
    ├── src/
    │   └── baobab_auth_security/
    │       ├── __init__.py
    │       ├── py.typed
    │       ├── version.py
    │       ├── exceptions.py
    │       ├── password/
    │       ├── tokens/
    │       ├── refresh_tokens/
    │       ├── keys/
    │       ├── revocation/
    │       ├── integration/
    │       ├── config/
    │       └── testing/
    ├── tests/
    │   ├── unit/
    │   ├── integration/
    │   ├── security/
    │   └── regression/
    └── docs/
    ```

    L’IA de développement peut adapter l’arborescence aux modules déjà existants, mais elle doit conserver la séparation entre primitives techniques, intégration core, configuration, tests et documentation.

    ## 6. Exigences techniques détaillées

    - `Argon2PasswordHasher.hash` retourne un hash non réversible et non vide.
- `verify` doit utiliser les API sûres d’Argon2 et retourner un booléen.
- `needs_rehash` doit permettre une migration future des paramètres Argon2.
- Le JWT doit contenir `sub`, `jti`, `sid` si session, `roles`, `permissions`, `iat`, `exp`, `iss`, `aud` selon configuration.
- Le header JWT doit contenir `kid` et `alg`.
- Les claims doivent être mappables vers le `TokenClaims` du core.
- Le `TokenPair` retourné au core doit conserver `access_token`, `refresh_token`, `token_type`, `expires_in`, `refresh_expires_in`.
- Les refresh tokens doivent être opaques, aléatoires et retournés une seule fois en clair.
- Le hash de refresh token doit être stockable par l’API ou la database, mais non persisté directement par security.
- Le JWKS public ne doit contenir aucune clé privée.

    ## 7. Contrats avec `baobab-auth-core`

    Les contrats suivants doivent rester valides à chaque version :

    ```python
    class PasswordHasher(Protocol):
        async def hash(self, plain_password: PlainPassword) -> PasswordHash: ...
        async def verify(self, plain_password: PlainPassword, password_hash: PasswordHash) -> bool: ...
        async def needs_rehash(self, password_hash: PasswordHash) -> bool: ...
    ```

    ```python
    class TokenProvider(Protocol):
        async def issue_token_pair(self, context: TokenIssueContext) -> TokenPair: ...
        async def verify_access_token(self, raw_token: str) -> TokenClaims: ...
        async def verify_refresh_token(self, raw_token: str) -> TokenClaims: ...
        async def revoke_token(self, token_id: TokenId) -> None: ...
    ```

    Les adaptateurs suivants doivent être maintenus :

    - `CorePasswordHasherAdapter` ;
    - `CoreTokenProviderAdapter` ;
    - `CoreClaimsMapper` ;
    - `CoreTokenPairMapper` ;
    - `CoreRevocationAdapter` si la version manipule la révocation.

    Règles :

    - ne pas redéfinir inutilement les value objects du core ;
    - utiliser les types réels du core si disponibles ;
    - documenter tout écart de chemin d’import ;
    - conserver les dates UTC aware ;
    - ne pas recalculer le mapping rôle → permissions ;
    - transporter les rôles et permissions fournis par le core ou l’API.

    ## 8. Contrats avec les autres briques

    ### `baobab-auth-database`

    `baobab-auth-security` ne doit pas dépendre directement de SQLAlchemy, mais doit fournir des ports ou DTO permettant à `baobab-auth-database` de persister :

    - hashes de refresh tokens ;
    - métadonnées de clés ;
    - états de rotation ;
    - enregistrements de révocation ;
    - états de familles de refresh tokens selon la version.

    ### `baobab-auth-api`

    `baobab-auth-api` utilisera la librairie pour :

    - hasher les mots de passe lors de l’inscription ;
    - vérifier les mots de passe lors du login ;
    - émettre les paires de tokens ;
    - exposer `/auth/jwks` ;
    - rafraîchir les sessions ;
    - révoquer les tokens/sessions ;
    - transformer les exceptions security en erreurs HTTP.

    ### `baobab-auth-client`

    `baobab-auth-client` consommera surtout les capacités de validation :

    - validation via JWKS distant ;
    - cache JWKS ;
    - algorithmes supportés ;
    - claims compatibles ;
    - construction d’un utilisateur authentifié côté API métier.

    ### `baobab-auth-admin`

    `baobab-auth-admin` utilisera les primitives de sécurité pour :

    - rotationner les clés ;
    - afficher les métadonnées non sensibles ;
    - vérifier l’état de conformité ;
    - déclencher des révocations techniques.

    ### `baobab-auth-service`

    `baobab-auth-service` validera l’assemblage runtime :

    - configuration des clés ;
    - configuration JWKS ;
    - configuration des caches optionnels ;
    - variables d’environnement ;
    - durcissement production.

    ## 9. Tests à produire

    - `tests/unit/password/test_argon2_password_hasher.py`
- `tests/unit/tokens/test_jwt_encoder_decoder_rs256.py`
- `tests/unit/tokens/test_jwt_validator_claims.py`
- `tests/unit/refresh_tokens/test_refresh_token_generator.py`
- `tests/unit/keys/test_rsa_key_generator.py`
- `tests/unit/jwks/test_jwks_provider.py`
- `tests/integration/core/test_core_password_hasher_adapter.py`
- `tests/integration/core/test_core_token_provider_adapter.py`
- `tests/security/test_no_secret_leakage.py`

    Objectifs de couverture :

    ```text
    coverage globale >= 90 %
    coverage modules critiques >= 95 % recommandée
    ```

    ## 10. Documentation attendue

    Chaque version doit mettre à jour :

    - `README.md` ;
    - `CHANGELOG.md` ;
    - `docs/integration_core.md` ;
    - `docs/security.md` ;
    - les pages spécifiques aux modules modifiés ;
    - les exemples d’utilisation ;
    - la matrice de compatibilité inter-briques.

    La documentation doit préciser :

    - les dépendances optionnelles ;
    - les dépendances interdites ;
    - les variables de configuration ;
    - les erreurs possibles ;
    - les limites de la version ;
    - la version minimale des autres briques nécessaires à la validation.

    ## 11. Backlog détaillé

    ### BL-S-010-001 — Initialiser le package

**Objectif :** Créer structure `src`, `pyproject.toml`, `README`, `CHANGELOG`, `py.typed`.

**Tâches :**

- analyser le code existant ;
- créer ou modifier les modules nécessaires ;
- ajouter les tests unitaires ;
- ajouter les tests d’intégration si la tâche touche une autre brique ;
- documenter l’usage public ;
- vérifier l’absence de fuite de secret.

**Critères d’acceptation :**

- la fonctionnalité est implémentée ;
- les tests dédiés passent ;
- `ruff`, `mypy` et `pytest` passent ;
- aucune dépendance interdite n’est ajoutée ;
- la documentation est mise à jour.

### BL-S-010-002 — Implémenter le hash de mot de passe

**Objectif :** Créer Argon2PasswordHasher et résultats typés.

**Tâches :**

- analyser le code existant ;
- créer ou modifier les modules nécessaires ;
- ajouter les tests unitaires ;
- ajouter les tests d’intégration si la tâche touche une autre brique ;
- documenter l’usage public ;
- vérifier l’absence de fuite de secret.

**Critères d’acceptation :**

- la fonctionnalité est implémentée ;
- les tests dédiés passent ;
- `ruff`, `mypy` et `pytest` passent ;
- aucune dépendance interdite n’est ajoutée ;
- la documentation est mise à jour.

### BL-S-010-003 — Implémenter JWT local RS256

**Objectif :** Créer encodeur, décodeur, validateur et provider.

**Tâches :**

- analyser le code existant ;
- créer ou modifier les modules nécessaires ;
- ajouter les tests unitaires ;
- ajouter les tests d’intégration si la tâche touche une autre brique ;
- documenter l’usage public ;
- vérifier l’absence de fuite de secret.

**Critères d’acceptation :**

- la fonctionnalité est implémentée ;
- les tests dédiés passent ;
- `ruff`, `mypy` et `pytest` passent ;
- aucune dépendance interdite n’est ajoutée ;
- la documentation est mise à jour.

### BL-S-010-004 — Implémenter refresh tokens opaques

**Objectif :** Générer token, hash, identifiant et dates UTC.

**Tâches :**

- analyser le code existant ;
- créer ou modifier les modules nécessaires ;
- ajouter les tests unitaires ;
- ajouter les tests d’intégration si la tâche touche une autre brique ;
- documenter l’usage public ;
- vérifier l’absence de fuite de secret.

**Critères d’acceptation :**

- la fonctionnalité est implémentée ;
- les tests dédiés passent ;
- `ruff`, `mypy` et `pytest` passent ;
- aucune dépendance interdite n’est ajoutée ;
- la documentation est mise à jour.

### BL-S-010-005 — Implémenter clés RSA et JWKS local

**Objectif :** Générer clés, convertir en JWK public, exposer JWKS.

**Tâches :**

- analyser le code existant ;
- créer ou modifier les modules nécessaires ;
- ajouter les tests unitaires ;
- ajouter les tests d’intégration si la tâche touche une autre brique ;
- documenter l’usage public ;
- vérifier l’absence de fuite de secret.

**Critères d’acceptation :**

- la fonctionnalité est implémentée ;
- les tests dédiés passent ;
- `ruff`, `mypy` et `pytest` passent ;
- aucune dépendance interdite n’est ajoutée ;
- la documentation est mise à jour.

### BL-S-010-006 — Implémenter adaptateurs core

**Objectif :** Brancher PasswordHasher et TokenProvider du core.

**Tâches :**

- analyser le code existant ;
- créer ou modifier les modules nécessaires ;
- ajouter les tests unitaires ;
- ajouter les tests d’intégration si la tâche touche une autre brique ;
- documenter l’usage public ;
- vérifier l’absence de fuite de secret.

**Critères d’acceptation :**

- la fonctionnalité est implémentée ;
- les tests dédiés passent ;
- `ruff`, `mypy` et `pytest` passent ;
- aucune dépendance interdite n’est ajoutée ;
- la documentation est mise à jour.

### BL-S-010-007 — Ajouter tests et documentation MVP

**Objectif :** Couvrir les cas de sécurité et usages de base.

**Tâches :**

- analyser le code existant ;
- créer ou modifier les modules nécessaires ;
- ajouter les tests unitaires ;
- ajouter les tests d’intégration si la tâche touche une autre brique ;
- documenter l’usage public ;
- vérifier l’absence de fuite de secret.

**Critères d’acceptation :**

- la fonctionnalité est implémentée ;
- les tests dédiés passent ;
- `ruff`, `mypy` et `pytest` passent ;
- aucune dépendance interdite n’est ajoutée ;
- la documentation est mise à jour.


    ## 12. Critères de définition de terminé

    La version `v0.1.0` est considérée terminée si :

    - tous les objectifs fonctionnels sont implémentés ;
    - les contrats avec `baobab-auth-core` sont respectés ;
    - l’intégration indiquée pour valider la version est testée ;
    - les tests unitaires passent ;
    - les tests d’intégration passent ;
    - les tests de sécurité ne détectent aucune fuite de secret ;
    - la documentation est à jour ;
    - `ruff format .` passe ;
    - `ruff check .` passe ;
    - `mypy src` passe ;
    - `pytest` passe ;
    - `python -m build` passe ;
    - `twine check dist/*` passe.

    ## 13. Commandes de validation

    ```bash
    ruff format .
    ruff check .
    mypy src
    pytest
    pytest --cov=baobab_auth_security --cov-report=term-missing
    python -m build
    twine check dist/*
    ```

    ## 14. Notes de livraison

    La livraison doit inclure :

    - le code source ;
    - les tests ;
    - la documentation ;
    - le changelog ;
    - la matrice de compatibilité ;
    - les limitations connues ;
    - les éventuelles tâches reportées.
