# Worklog — BL-S-010-004

- `refresh_tokens/refresh_token_hasher.py` : `RefreshTokenHasher` (SHA-256 hex,
  `hmac.compare_digest`).
- `refresh_tokens/refresh_token_result.py` : `RefreshTokenResult` (clair masqué,
  champs validés, dates UTC aware).
- `refresh_tokens/refresh_token_generator.py` : `RefreshTokenGenerator`
  (`secrets.token_urlsafe`, entropie >= 32 octets, TTL configurable, horloge
  injectée).
- Export racine, tests miroir.

## Décisions

- Hash sans sel : le token possède une entropie complète, SHA-256 suffit et
  permet la recherche par hash côté database/API.
- `baobab-auth-security` ne persiste rien : seul le hash est destiné au stockage
  externe (ADR-0004).
