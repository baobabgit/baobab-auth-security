# Handoff — BL-S-010-002

## État

Module `password` livré et validé localement (couverture 100 %). PR vers
`version/v0.1.0`, merge après CI verte.

## Acquis réutilisables

- `Argon2PasswordHasher` : à envelopper par `CorePasswordHasherAdapter`
  (BL-S-010-006) pour satisfaire le port `PasswordHasher` du core.

## Prochaine étape

BL-S-010-005 (clés RSA + JWKS) recommandée avant BL-S-010-003 (JWT), car le
`JwtTokenProvider` consomme un résolveur de clé. Les composants JWT acceptent
toutefois des clés `cryptography` injectées, donc l'ordre reste flexible.
