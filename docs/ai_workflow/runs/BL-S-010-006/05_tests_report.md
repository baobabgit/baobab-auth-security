# Tests Report — BL-S-010-006

| Gate | Résultat |
|------|----------|
| `black --check` | ✅ |
| `ruff check` | ✅ |
| `mypy src` | ✅ (45 fichiers) |
| `bandit -r src` | ✅ (0 High) |
| `pytest` couverture | ✅ **100 %** |
| `uv build` + `twine check` | ✅ PASSED |
| `traceability` | ✅ |

152 tests passés. Intégration contractuelle (`tests/integration/core/`) :
`isinstance(adapter, PasswordHasher)` et `isinstance(adapter, TokenProvider)`
(ports réels runtime_checkable), aller-retour hash/verify, émission/vérification
access et refresh, révocation par `jti`, traduction des exceptions du core.
