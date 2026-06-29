"""Tests de :class:`SystemClock`.

:spec: FEAT-012.1
"""

from __future__ import annotations

from datetime import UTC

from baobab_auth_security.clock.clock import Clock
from baobab_auth_security.clock.system_clock import SystemClock


class TestSystemClock:
    """Vérifie que l'horloge système renvoie un instant UTC aware."""

    def test_FEAT_012_1_now_is_timezone_aware_utc(self) -> None:
        # Arrange
        clock = SystemClock()

        # Act
        moment = clock.now()

        # Assert
        assert moment.tzinfo is not None
        assert moment.utcoffset() == UTC.utcoffset(None)

    def test_FEAT_012_1_satisfies_clock_protocol(self) -> None:
        assert isinstance(SystemClock(), Clock)
