"""Tests de :class:`SecurityTokenPair`.

:spec: FEAT-010.2, ADR-0006
"""

from __future__ import annotations

from baobab_auth_security.tokens.security_token_pair import SecurityTokenPair


class TestSecurityTokenPair:
    """Vérifie le masquage des tokens dans la représentation."""

    def test_FEAT_010_2_repr_masks_token_values(self) -> None:
        pair = SecurityTokenPair(
            access_token="header.payload.signature",
            refresh_token="opaque-secret-value",
            expires_in=900,
            refresh_expires_in=86400,
        )
        text = repr(pair)
        assert "header.payload.signature" not in text
        assert "opaque-secret-value" not in text
        assert "expires_in=900" in text
        assert pair.token_type == "Bearer"

    def test_FEAT_010_2_values_remain_accessible(self) -> None:
        pair = SecurityTokenPair(
            access_token="a",
            refresh_token="r",
            expires_in=1,
            refresh_expires_in=2,
        )
        assert pair.access_token == "a"
        assert pair.refresh_token == "r"
