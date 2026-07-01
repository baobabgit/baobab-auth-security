"""Tests de :class:`SecurityTokenClaims`.

:spec: FEAT-010.2
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from baobab_auth_security.exceptions import ConfigurationError
from baobab_auth_security.tokens.security_token_claims import SecurityTokenClaims


class TestSecurityTokenClaims:
    """Vérifie la structure et la contrainte UTC des claims."""

    def test_FEAT_010_2_holds_required_fields(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        claims = SecurityTokenClaims(
            sub="user-1",
            jti="jti-1",
            issued_at=now,
            expires_at=now + timedelta(minutes=15),
            roles=("admin",),
        )
        assert claims.sub == "user-1"
        assert claims.roles == ("admin",)
        assert claims.permissions == ()

    def test_FEAT_010_2_rejects_naive_dates(self) -> None:
        naive = datetime(2026, 1, 1)
        aware = datetime(2026, 1, 1, tzinfo=UTC)
        with pytest.raises(ConfigurationError):
            SecurityTokenClaims(sub="u", jti="j", issued_at=naive, expires_at=aware)
