# Changelog

Toutes les modifications notables de ce projet sont documentées ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### Ajouté

- **Socle du package `baobab_auth_security`** (BL-S-010-001) : layout `src/`,
  `py.typed`, `version.py`, hiérarchie d'exceptions (`SecurityError` racine),
  module `clock` (`Clock`, `SystemClock`, `FixedClock`, UTC aware).
- Dépendances runtime : `baobab-auth-core>=0.4.0,<1.0.0`, `argon2-cffi`,
  `cryptography`, `PyJWT`, `pydantic-settings`.
- Cahier des charges v0.1.0 intégré ; US-010/011/012, FEAT-010.x/011.1/012.x,
  ADR-0001 à 0006.
