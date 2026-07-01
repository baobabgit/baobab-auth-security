# Tests Report — BL-S-010-002

| Gate | Résultat |
|------|----------|
| `black --check` | ✅ |
| `ruff check` | ✅ |
| `mypy src` | ✅ (12 fichiers) |
| `bandit -r src` | ✅ (0 High) |
| `pytest` couverture | ✅ **100 %** |
| `uv build` + `twine check` | ✅ PASSED |
| `traceability` | ✅ |

46 tests passés. Cas couverts : hash Argon2id non réversible et salé, vérification
correcte/incorrecte, hash malformé, mot de passe vide, `needs_rehash` (changement
de paramètres), bornes de la politique.
