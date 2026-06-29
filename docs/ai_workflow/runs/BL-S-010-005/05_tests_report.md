# Tests Report — BL-S-010-005

| Gate | Résultat |
|------|----------|
| `black --check` | ✅ |
| `ruff check` | ✅ |
| `mypy src` | ✅ (36 fichiers) |
| `bandit -r src` | ✅ (0 High) |
| `pytest` couverture | ✅ **100 %** |
| `uv build` + `twine check` | ✅ PASSED |
| `traceability` | ✅ |

127 tests passés. Cas de sécurité : clé privée masquée dans `repr`, JWKS sans
champ privé (`d`/`p`/`q`), clés PENDING omises, refus de clés PEM non-RSA.
