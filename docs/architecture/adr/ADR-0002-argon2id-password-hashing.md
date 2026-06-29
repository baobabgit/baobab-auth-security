# ADR-0002 — Argon2id pour le hachage de mot de passe

- **Statut :** Accepté
- **Date :** 2026-06-29
- **Version :** v0.1.0
- **Backlog :** BL-S-010-002 (FEAT-010.1)

## Contexte

Le hachage de mot de passe doit être résistant aux attaques GPU/ASIC et
permettre une migration des paramètres dans le temps.

## Décision

- Utiliser **Argon2id** via `argon2-cffi` (`PasswordHasher` natif), variante
  recommandée par l'OWASP.
- Encapsuler les paramètres (`time_cost`, `memory_cost`, `parallelism`,
  `hash_len`, `salt_len`) dans une `PasswordHashPolicy` (dataclass figée),
  injectable.
- Exposer des résultats typés `PasswordHashResult` et
  `PasswordVerificationResult` masquant tout secret dans `repr`/`str`.
- Fournir `needs_rehash()` pour piloter la migration future des paramètres.
- `verify()` ne lève pas sur mauvais mot de passe : il retourne `is_valid=False`
  (l'API `verify` d'Argon2 lève `VerifyMismatchError`, capturée).

## Conséquences

- La sécurité des paramètres est centralisée et auditable.
- Le service technique reste plus riche que le port du core (qui n'expose que
  `hash`/`verify`) ; l'adaptateur core (ADR-0005) restreint la surface.
