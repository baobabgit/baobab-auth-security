"""Tests de :class:`KeyStatus`.

:spec: FEAT-010.4
"""

from __future__ import annotations

from baobab_auth_security.keys.key_status import KeyStatus


class TestKeyStatus:
    """Vérifie les valeurs du cycle de vie des clés."""

    def test_FEAT_010_4_status_values(self) -> None:
        assert KeyStatus.ACTIVE.value == "active"
        assert KeyStatus.PENDING.value == "pending"
        assert KeyStatus.RETIRED.value == "retired"
