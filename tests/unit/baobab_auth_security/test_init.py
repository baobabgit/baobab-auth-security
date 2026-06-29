"""Tests du contrat public exposé par ``baobab_auth_security``.

:spec: FEAT-012.1
"""

from __future__ import annotations

import baobab_auth_security


class TestPublicApi:
    """Vérifie la stabilité du contrat public ``__all__``."""

    def test_FEAT_012_1_all_symbols_are_importable(self) -> None:
        for name in baobab_auth_security.__all__:
            assert hasattr(baobab_auth_security, name), name

    def test_FEAT_012_1_core_symbols_present(self) -> None:
        expected = {
            "Clock",
            "SystemClock",
            "FixedClock",
            "SecurityError",
            "__version__",
        }
        assert expected.issubset(set(baobab_auth_security.__all__))
