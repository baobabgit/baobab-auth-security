# Worklog — BL-S-010-002

- `password/password_hash_policy.py` : `PasswordHashPolicy` (dataclass figée,
  défauts OWASP : time_cost=3, memory_cost=65536, parallelism=4, hash_len=32,
  salt_len=16) avec validation des bornes (dont `memory_cost >= 8 * parallelism`).
- `password/password_hash_result.py` : `PasswordHashResult` (valeur exposée pour
  stockage, masquée dans `repr`/`str`).
- `password/password_verification_result.py` : `PasswordVerificationResult`
  (`is_valid`, `needs_rehash`, `__bool__`).
- `password/argon2_password_hasher.py` : `Argon2PasswordHasher`
  (`hash`/`verify`/`needs_rehash`) sur `argon2-cffi` (Type.ID).
- Export des symboles au niveau du package racine.
- Tests miroir : nominal + négatifs (mauvais mot de passe sans exception, hash
  malformé → `PasswordHashingError`, mot de passe vide, re-hash).

## Décisions

- `verify` ne lève pas sur mauvais mot de passe (`VerifyMismatchError` → `is_valid=False`).
- Un hash malformé lève `PasswordHashingError` (mappe `InvalidHashError`).
- Le service riche travaille sur `str` ; l'adaptateur core (BL-S-010-006)
  convertira depuis/vers `PlainPassword`/`PasswordHash`.
