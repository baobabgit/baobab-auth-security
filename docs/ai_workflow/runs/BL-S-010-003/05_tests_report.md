# Tests Report — BL-S-010-003

| Gate | Résultat |
|------|----------|
| `black --check` | ✅ |
| `ruff check` | ✅ |
| `mypy src` | ✅ (20 fichiers) |
| `bandit -r src` | ✅ (0 High) |
| `pytest` couverture | ✅ **100 %** |
| `uv build` + `twine check` | ✅ PASSED |
| `traceability` | ✅ |

82 tests passés. Cas de sécurité couverts : refus `alg=none`, algorithme hors
liste blanche, `kid` manquant/inconnu, signature invalide (mauvaise clé / token
altéré), charge utile non-JSON, token expiré, `iss`/`aud` incohérents.
