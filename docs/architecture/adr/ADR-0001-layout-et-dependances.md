# ADR-0001 — Layout `src/` et dépendances runtime

- **Statut :** Accepté
- **Date :** 2026-06-29
- **Version :** v0.1.0
- **Backlog :** BL-S-010-001 (FEAT-012.1)

## Contexte

`baobab-auth-security` est une librairie consommable, indépendante de l'API HTTP,
de la base SQL et des applications métier. Elle doit fournir des primitives
cryptographiques et s'intégrer au port stable de `baobab-auth-core`.

## Décision

- Layout `src/baobab_auth_security/` (1 classe = 1 fichier), `py.typed` exporté.
- Dépendances **runtime obligatoires** : `baobab-auth-core>=0.4.0,<1.0.0`,
  `argon2-cffi`, `cryptography`, `PyJWT`, `pydantic` (via `pydantic-settings`).
- `httpx` et `redis` réservés à des extras optionnels de versions ultérieures
  (≥ v0.2.0 / ≥ v0.6.0) — **non** ajoutés en v0.1.0.
- Dépendances **interdites** en runtime obligatoire : `fastapi`, `sqlalchemy`,
  `alembic`, `psycopg`, `asyncpg`, `redis`, `uvicorn`, `docker`.
- Configuration **injectée** via `pydantic-settings` ; aucun état global.

## Conséquences

- La librairie reste embarquable dans un projet parent sans contrainte d'hôte.
- Le contrat public (`__all__`) est versionné en SemVer ; toute rupture impose un
  bump majeur + entrée CHANGELOG « BREAKING ».
- `baobab-auth-core` étant publié sur PyPI (≥ 0.4.0), la dépendance est résolue
  par PyPI ; la validation d'intégration croisée se fait par git-ref.
