# Handoff — BL-S-010-003

## État

Module `tokens` (JWT RS256) livré et validé localement (couverture 100 %). PR vers
`version/v0.1.0`, merge après CI verte.

## Acquis réutilisables

- `JwtTokenProvider` : à envelopper par `CoreTokenProviderAdapter` (BL-S-010-006).
- `PublicKeyResolver` (`kid -> RSAPublicKey`) : sera fourni par
  `InMemoryKeyProvider` (BL-S-010-005).
- `JwtAlgorithm` : pendant `tokens` de `KeyAlgorithm` (BL-005) — même jeu de noms.

## Prochaine étape

BL-S-010-004 (refresh tokens opaques) ou BL-S-010-005 (clés RSA + JWKS), tous deux
indépendants. Recommandé : BL-S-010-005 pour fournir le résolveur de clés.
