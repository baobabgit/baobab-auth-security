"""Tests de :class:`JwtTokenProvider` (émission + vérification).

:spec: FEAT-010.2, ADR-0003
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.exceptions import TokenExpiredError
from baobab_auth_security.tokens.jwt_decoder import JwtDecoder
from baobab_auth_security.tokens.jwt_encoder import JwtEncoder
from baobab_auth_security.tokens.jwt_token_provider import JwtTokenProvider
from baobab_auth_security.tokens.jwt_validator import JwtValidator

_NOW = datetime(2026, 6, 29, 12, 0, tzinfo=UTC)


def _provider(
    encoder: JwtEncoder, decoder: JwtDecoder, clock: FixedClock
) -> JwtTokenProvider:
    validator = JwtValidator(clock, issuer="baobab-auth", audience="api")
    return JwtTokenProvider(
        encoder, decoder, validator, clock, issuer="baobab-auth", audience="api"
    )


class TestJwtTokenProvider:
    """Vérifie l'aller-retour émission → vérification."""

    def test_FEAT_010_2_issue_then_verify_round_trip(
        self, encoder: JwtEncoder, decoder: JwtDecoder
    ) -> None:
        provider = _provider(encoder, decoder, FixedClock(_NOW))

        token = provider.issue_access_token(
            subject="user-1",
            token_id="jti-1",
            ttl_seconds=900,
            session_id="sess-1",
            roles=("admin",),
            permissions=("read",),
        )
        claims = provider.verify_access_token(token)

        assert claims.sub == "user-1"
        assert claims.jti == "jti-1"
        assert claims.sid == "sess-1"
        assert claims.roles == ("admin",)
        assert claims.issuer == "baobab-auth"
        assert claims.audience == "api"

    def test_FEAT_010_2_verify_rejects_expired_token(
        self, encoder: JwtEncoder, decoder: JwtDecoder
    ) -> None:
        issuer_clock = FixedClock(_NOW)
        provider_issue = _provider(encoder, decoder, issuer_clock)
        token = provider_issue.issue_access_token(
            subject="u", token_id="j", ttl_seconds=60
        )

        # Vérification 1h plus tard : expiré.
        later = FixedClock(_NOW + timedelta(hours=1))
        provider_verify = _provider(encoder, decoder, later)
        with pytest.raises(TokenExpiredError):
            provider_verify.verify_access_token(token)
