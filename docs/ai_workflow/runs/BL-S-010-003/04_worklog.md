# Worklog — BL-S-010-003

- `tokens/jwt_algorithm.py` : `JwtAlgorithm` (StrEnum RS256/384/512), `from_name`
  refuse `none`/inconnu, `names()`.
- `tokens/security_token_claims.py` : `SecurityTokenClaims` (dates UTC aware
  imposées).
- `tokens/security_token_pair.py` : `SecurityTokenPair` (repr masqué).
- `tokens/jwt_encoder.py` : `JwtEncoder` (RS256, `kid`/`alg` au header).
- `tokens/jwt_decoder.py` : `JwtDecoder` (vérifie la signature, refuse
  `alg=none`/hors liste, `kid` manquant → erreur, résolveur de clé par `kid`).
- `tokens/jwt_validator.py` : `JwtValidator` (expiration + leeway, `iss`, `aud`).
- `tokens/jwt_token_provider.py` : `JwtTokenProvider` (émission + vérification).
- Tests miroir + conftest (clés RSA de session, résolveur, horloge fixe).

## Décisions

- Découplage : encoder/décodeur acceptent des clés `cryptography` injectées et un
  résolveur `kid -> RSAPublicKey` ; aucune dépendance au module `keys` (BL-005).
- Le décodeur ne vérifie que la signature (`verify_exp=False`) ; la validation
  métier (`exp`/`iss`/`aud`) revient au `JwtValidator` (exceptions typées).
