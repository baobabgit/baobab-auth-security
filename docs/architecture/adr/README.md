# Architecture Decision Records — `baobab-auth-security`

Décisions d'architecture structurantes, une par fichier, numérotées `ADR-XXXX`.

| ADR | Titre | Statut |
|-----|-------|--------|
| [ADR-0001](ADR-0001-layout-et-dependances.md) | Layout `src/` et dépendances runtime | Accepté |
| [ADR-0002](ADR-0002-argon2id-password-hashing.md) | Argon2id pour le hachage de mot de passe | Accepté |
| [ADR-0003](ADR-0003-jwt-rs256-et-durcissement.md) | JWT RS256 par défaut et durcissement (`alg=none`, allowlist) | Accepté |
| [ADR-0004](ADR-0004-refresh-tokens-opaques.md) | Refresh tokens opaques et hash stocké à l'extérieur | Accepté |
| [ADR-0005](ADR-0005-adaptation-ports-reels-core.md) | Adaptation aux ports réels (synchrones) du core | Accepté |
| [ADR-0006](ADR-0006-non-fuite-de-secrets.md) | Garantie de non-fuite des secrets | Accepté |
