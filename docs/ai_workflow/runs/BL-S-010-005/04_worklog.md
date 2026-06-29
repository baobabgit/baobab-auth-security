# Worklog — BL-S-010-005

## Module `keys`

- `key_algorithm.py` : `KeyAlgorithm` (StrEnum RS256/384/512).
- `key_status.py` : `KeyStatus` (PENDING/ACTIVE/RETIRED).
- `key_pair.py` : `KeyPair` (clé privée masquée dans `repr`, `created_at` UTC).
- `key_generator.py` : `KeyGenerator` (RSA ≥ 2048, `kid` dérivé SHA-256 de la clé
  publique si absent).
- `in_memory_key_provider.py` : `InMemoryKeyProvider` (clé active, résolution par
  `kid`, `set_active`).
- `pem_key_loader.py` : `PemKeyLoader` (charge clés RSA PEM, refuse non-RSA).

## Module `jwks`

- `jwk.py` / `jwks.py` : `JWK` (champs publics seuls) / `JWKS` (`to_dict`).
- `rsa_public_jwk_converter.py` : encodage base64url RFC 7518 de `n`/`e`.
- `jwks_provider.py` : `LocalJwksProvider` (publie ACTIVE+RETIRED, omet PENDING ;
  aucune clé privée).

## Décisions

- `InMemoryKeyProvider.public_key_for_kid` est structurellement un
  `PublicKeyResolver` (consommé par `JwtDecoder` — câblage en BL-S-010-006).
- Le JWKS ne contient jamais `d`/`p`/`q` (vérifié par test, ADR-0006).
