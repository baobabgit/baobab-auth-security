"""Tests de :class:`JwtEncoder` (signature RS256).

:spec: FEAT-010.2, ADR-0003
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import jwt

from baobab_auth_security.tokens.jwt_decoder import JwtDecoder
from baobab_auth_security.tokens.jwt_encoder import JwtEncoder
from baobab_auth_security.tokens.security_token_claims import SecurityTokenClaims


def _claims() -> SecurityTokenClaims:
    now = datetime(2026, 6, 29, 12, 0, tzinfo=UTC)
    return SecurityTokenClaims(
        sub="user-42",
        jti="jti-xyz",
        issued_at=now,
        expires_at=now + timedelta(minutes=15),
        sid="sess-1",
        roles=("admin", "user"),
        permissions=("read", "write"),
        issuer="baobab-auth",
        audience=("api", "web"),
    )


class TestJwtEncoder:
    """Vérifie l'encodage RS256 et la présence du ``kid``."""

    def test_FEAT_010_2_header_contains_kid_and_alg(self, encoder: JwtEncoder) -> None:
        token = encoder.encode(_claims())
        header = jwt.get_unverified_header(token)
        assert header["kid"] == encoder.kid
        assert header["alg"] == "RS256"

    def test_FEAT_010_2_round_trip_preserves_claims(
        self, encoder: JwtEncoder, decoder: JwtDecoder
    ) -> None:
        decoded = decoder.decode(encoder.encode(_claims()))
        assert decoded.sub == "user-42"
        assert decoded.jti == "jti-xyz"
        assert decoded.sid == "sess-1"
        assert decoded.roles == ("admin", "user")
        assert decoded.permissions == ("read", "write")
        assert decoded.issuer == "baobab-auth"
        assert decoded.audience == ("api", "web")
        assert decoded.expires_at.tzinfo is not None
