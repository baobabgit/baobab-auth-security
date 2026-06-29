# ADR-0003 — JWT RS256 par défaut et durcissement

- **Statut :** Accepté
- **Date :** 2026-06-29
- **Version :** v0.1.0
- **Backlog :** BL-S-010-003 (FEAT-010.2)

## Contexte

Les access tokens doivent être vérifiables par des consommateurs via une clé
publique (JWKS), sans partager de secret symétrique.

## Décision

- Signature **asymétrique RS256** par défaut (extensible RS384/RS512), via `PyJWT`.
- Header portant `kid` (résolution de clé) et `alg`.
- Séparation des responsabilités : `JwtEncoder` (signe), `JwtDecoder` (vérifie la
  signature), `JwtValidator` (valide les claims), `JwtTokenProvider` (orchestre).
- **Durcissement obligatoire** :
  - refus de `alg=none` ;
  - **allowlist** d'algorithmes : tout algorithme hors liste est rejeté ;
  - `alg` du header confronté à l'algorithme attendu de la clé ;
  - vérification `exp`, `iss`, `aud` ; dates **UTC aware** uniquement.
- Claims structurés dans `SecurityTokenClaims` ; paire dans `SecurityTokenPair`
  (valeurs masquées dans `repr`).

## Conséquences

- Les consommateurs valident hors-ligne via JWKS public.
- Les attaques par confusion d'algorithme (`alg=none`, HS256 avec clé publique)
  sont neutralisées et testées (cas négatifs).
