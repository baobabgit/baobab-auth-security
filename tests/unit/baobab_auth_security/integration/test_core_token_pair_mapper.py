"""Tests unitaires de :class:`CoreTokenPairMapper`.

:spec: FEAT-011.1, ADR-0005
"""

from __future__ import annotations

from baobab_auth_core.application.results.token_pair import TokenPair

from baobab_auth_security.integration.core_token_pair_mapper import CoreTokenPairMapper
from baobab_auth_security.tokens.security_token_pair import SecurityTokenPair


class TestCoreTokenPairMapper:
    """Vérifie le mapping vers le DTO ``TokenPair`` du core."""

    def test_FEAT_011_1_maps_all_fields(self) -> None:
        pair = SecurityTokenPair(
            access_token="a.b.c",
            refresh_token="r.s.t",
            expires_in=900,
            refresh_expires_in=86400,
        )
        core = CoreTokenPairMapper().to_core(pair)
        assert isinstance(core, TokenPair)
        assert core.access_token == "a.b.c"
        assert core.refresh_token == "r.s.t"
        assert core.token_type == "Bearer"
        assert core.expires_in == 900
        assert core.refresh_expires_in == 86400
