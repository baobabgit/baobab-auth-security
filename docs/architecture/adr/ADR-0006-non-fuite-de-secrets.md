# ADR-0006 — Garantie de non-fuite des secrets

- **Statut :** Accepté
- **Date :** 2026-06-29
- **Version :** v0.1.0
- **Backlog :** BL-S-010-007 (FEAT-012.2)

## Contexte

La librairie manipule des secrets : mots de passe, refresh tokens, clés privées,
access tokens. Une fuite dans un log, une exception ou un `repr` est critique.

## Décision

- Tout value object ou résultat portant un secret **masque** sa valeur dans
  `__repr__` et `__str__` (`'***'`).
- Les exceptions du package ne contiennent jamais la valeur d'un secret dans leur
  message.
- La clé privée n'est jamais sérialisée dans un JWKS, un log, une métrique ou un
  `repr` ; seule la partie publique (`n`, `e`) est exposée.
- Règles transverses appliquées et testées :
  - ne jamais logger de mot de passe brut, de refresh token brut, d'access token
    complet ;
  - refuser `alg=none` et tout algorithme non autorisé ;
  - dates **UTC aware** uniquement.
- Un jeu de tests `tests/security/test_no_secret_leakage.py` vérifie ces
  invariants (cas positifs et négatifs) et sert de non-régression.

## Conséquences

- Les garanties sont mécaniquement vérifiées à chaque exécution de la suite.
- Bandit (`make quality`) complète la couverture par une analyse statique.
