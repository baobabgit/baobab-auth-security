"""Tests unitaires de :class:`CoreClaimsMapper`.

:spec: FEAT-011.1, ADR-0005
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from baobab_auth_core.application.results.token_claims import TokenClaims
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_name import RoleName

from baobab_auth_security.integration.core_claims_mapper import CoreClaimsMapper
from baobab_auth_security.tokens.security_token_claims import SecurityTokenClaims

_NOW = datetime(2026, 6, 29, 12, 0, tzinfo=UTC)


class TestCoreClaimsMapper:
    """Vérifie le mapping vers le VO ``TokenClaims`` du core."""

    def test_FEAT_011_1_maps_all_fields(self) -> None:
        claims = SecurityTokenClaims(
            sub="user-1",
            jti="jti-1",
            issued_at=_NOW,
            expires_at=_NOW + timedelta(minutes=15),
            sid="sess-1",
            roles=("ADMIN",),
            permissions=("auth:user:read",),
            issuer="baobab",
            audience="api",
        )

        core = CoreClaimsMapper().to_core(claims)

        assert isinstance(core, TokenClaims)
        assert core.subject.value == "user-1"
        assert core.session_id is not None
        assert core.session_id.value == "sess-1"
        assert core.token_id.value == "jti-1"
        assert core.roles == (RoleName("ADMIN"),)
        assert core.permissions == (PermissionName("auth:user:read"),)
        assert core.issued_at == _NOW

    def test_FEAT_011_1_maps_absent_session_to_none(self) -> None:
        claims = SecurityTokenClaims(
            sub="u", jti="j", issued_at=_NOW, expires_at=_NOW + timedelta(minutes=1)
        )
        assert CoreClaimsMapper().to_core(claims).session_id is None
