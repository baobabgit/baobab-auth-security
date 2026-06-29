# Tests Report — BL-S-010-004

| Gate | Résultat |
|------|----------|
| `black --check` | ✅ |
| `ruff check` | ✅ |
| `mypy src` | ✅ (24 fichiers) |
| `bandit -r src` | ✅ (0 High) |
| `pytest` couverture | ✅ **100 %** |
| `uv build` + `twine check` | ✅ PASSED |
| `traceability` | ✅ |

94 tests passés. Couvre : unicité/entropie des tokens, hash déterministe et
vérification temps constant, masquage du clair, validation des champs et dates.
