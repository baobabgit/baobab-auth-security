"""Tests du port ``Clock`` réexporté.

:spec: FEAT-012.1
"""

from __future__ import annotations

from baobab_auth_core.ports.clock import Clock as CoreClock

from baobab_auth_security.clock.clock import Clock


class TestClock:
    """Vérifie l'alignement du port ``Clock`` sur ``baobab-auth-core``."""

    def test_FEAT_012_1_clock_is_core_protocol(self) -> None:
        assert Clock is CoreClock
