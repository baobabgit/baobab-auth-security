# Tests Report — BL-S-010-001

Exécution locale (`uv run`) :

| Gate | Résultat |
|------|----------|
| `black --check src tests` | ✅ |
| `ruff check src tests` | ✅ |
| `mypy src` | ✅ (7 fichiers) |
| `bandit -r src` | ✅ (0 issue) |
| `pytest` couverture | ✅ **100 %** (≥ 95 %) |
| `uv build` + `twine check` | ✅ PASSED |
| `check_traceability.py` | ✅ |

24 tests passés. Modules couverts : `version`, `exceptions`, `clock` (system,
fixed, port).
