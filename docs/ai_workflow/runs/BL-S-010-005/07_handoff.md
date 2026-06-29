# Handoff — BL-S-010-005

## État

Modules `keys` et `jwks` livrés et validés localement (couverture 100 %). PR vers
`version/v0.1.0`, merge après CI verte.

## Acquis réutilisables

- `KeyGenerator` + `InMemoryKeyProvider` : fournissent la clé active (signature)
  et le résolveur `public_key_for_kid` pour câbler `JwtEncoder`/`JwtDecoder`.
- `LocalJwksProvider` : exposera `/auth/jwks` côté API.

## Prochaine étape

BL-S-010-006 (adaptateurs core) : assembler password + tokens + refresh + keys +
révocation derrière les ports réels de `baobab-auth-core`. Dernier backlog de code
avant tests/doc MVP (BL-S-010-007).
