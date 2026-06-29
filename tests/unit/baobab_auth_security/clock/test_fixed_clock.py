"""Tests de :class:`FixedClock`.

:spec: FEAT-012.1
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from baobab_auth_security.clock.clock import Clock
from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.exceptions import ConfigurationError


class TestFixedClock:
    """Vérifie le comportement déterministe de l'horloge fixe."""

    def test_FEAT_012_1_now_returns_fixed_moment(self) -> None:
        # Arrange
        moment = datetime(2026, 6, 29, 12, 0, tzinfo=UTC)
        clock = FixedClock(moment)

        # Act / Assert
        assert clock.now() == moment
        assert clock.now() == moment  # stable entre appels

    def test_FEAT_012_1_rejects_naive_datetime(self) -> None:
        with pytest.raises(ConfigurationError):
            FixedClock(datetime(2026, 6, 29, 12, 0))

    def test_FEAT_012_1_satisfies_clock_protocol(self) -> None:
        clock = FixedClock(datetime(2026, 6, 29, tzinfo=UTC))
        assert isinstance(clock, Clock)
