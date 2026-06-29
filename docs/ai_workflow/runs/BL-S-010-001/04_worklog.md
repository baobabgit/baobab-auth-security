# Worklog — BL-S-010-001

- `pyproject.toml` : nom `baobab-auth-security`, dépendances runtime
  (`baobab-auth-core>=0.4.0,<1.0.0`, `argon2-cffi`, `cryptography`, `PyJWT`,
  `pydantic-settings`), `packages = ["src/baobab_auth_security"]`, classifiers
  sécurité.
- Suppression de `example_package` (src + tests).
- `src/baobab_auth_security/` : `__init__.py` (contrat `__all__`), `py.typed`,
  `version.py` (`__version__ = "0.1.0"`), `exceptions.py` (hiérarchie complète
  sous `SecurityError`).
- Module `clock/` : `clock.py` (réexport du port `Clock` du core), `system_clock.py`
  (`SystemClock`), `fixed_clock.py` (`FixedClock`, rejet des datetimes naïfs).
- Tests miroir : `test_version`, `test_exceptions`, `test_init`, `clock/test_*`.
- `README.md` réécrit pour la librairie ; `CHANGELOG.md` réinitialisé.

## Décisions

- Le port `Clock` est **réexporté** depuis `baobab-auth-core` (pas de redéfinition)
  — cf. ADR-0005. `SystemClock`/`FixedClock` le satisfont structurellement
  (`runtime_checkable`).
- Hiérarchie d'exceptions regroupée dans `exceptions.py` (dérogation « 1 classe =
  1 fichier » pour les hiérarchies d'exceptions courtes).
