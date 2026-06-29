# ADR-0004 — Refresh tokens opaques et hash stocké à l'extérieur

- **Statut :** Accepté
- **Date :** 2026-06-29
- **Version :** v0.1.0
- **Backlog :** BL-S-010-004 (FEAT-010.3)

## Contexte

Les refresh tokens ont une durée de vie longue et doivent pouvoir être révoqués.
Les stocker en clair ou les rendre auto-portants (JWT) augmente la surface
d'attaque.

## Décision

- Refresh tokens **opaques** : valeur aléatoire à forte entropie (`secrets.token_urlsafe`).
- Le token en clair n'est exposé **qu'une seule fois** (dans `RefreshTokenResult`,
  masqué dans `repr`/`str`).
- Seul le **hash SHA-256** est destiné au stockage externe (API / database).
  `baobab-auth-security` ne persiste **rien** lui-même.
- `RefreshTokenResult` porte `token` (clair, éphémère), `token_hash`, `token_id`
  (`jti`), `issued_at`, `expires_at` (UTC aware).
- Comparaison de hash en **temps constant** (`hmac.compare_digest`).

## Conséquences

- La révocation et la rotation (versions ultérieures) s'appuient sur le `token_id`
  et le hash stocké côté consommateur.
- La librairie reste sans état de persistance, conforme à son périmètre.
