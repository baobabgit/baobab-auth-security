# Handoff — BL-S-010-001

## État

Socle du package livré et validé localement (`make all` ✅, couverture 100 %).
PR ouverte vers `version/v0.1.0`. Merge après CI verte.

## Acquis réutilisables

- `baobab_auth_security.exceptions` : hiérarchie prête pour les modules suivants
  (`TokenError`, `KeyManagementError`, `PasswordHashingError`, etc.).
- `baobab_auth_security.clock` : `SystemClock` / `FixedClock` à injecter dans le
  `JwtTokenProvider` (BL-S-010-003) et les refresh tokens (BL-S-010-004).

## Prochaine étape

BL-S-010-002 (hash Argon2id) — dépendance `argon2-cffi` déjà déclarée et installée.
Branche `bl/S-010-002-...` depuis `version/v0.1.0` après merge de cette PR.
