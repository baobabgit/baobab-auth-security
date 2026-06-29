"""Tests de :class:`JwtValidator` (claims métier).

:spec: FEAT-010.2, ADR-0003
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.exceptions import (
    InvalidAlgorithmError,
    TokenExpiredError,
    TokenValidationError,
)
from baobab_auth_security.tokens.jwt_validator import JwtValidator
from baobab_auth_security.tokens.security_token_claims import SecurityTokenClaims

_NOW = datetime(2026, 6, 29, 12, 0, tzinfo=UTC)


def _claims(
    *,
    exp_delta: int = 300,
    issuer: str | None = None,
    audience: str | tuple[str, ...] | None = None,
) -> SecurityTokenClaims:
    return SecurityTokenClaims(
        sub="u",
        jti="j",
        issued_at=_NOW,
        expires_at=_NOW + timedelta(seconds=exp_delta),
        issuer=issuer,
        audience=audience,
    )


class TestJwtValidator:
    """Vérifie expiration, émetteur, audience et algorithme."""

    def test_FEAT_010_2_accepts_valid_claims(self) -> None:
        validator = JwtValidator(FixedClock(_NOW), issuer="iss", audience="api")
        validator.validate(_claims(issuer="iss", audience="api"))

    def test_FEAT_010_2_raises_on_expired(self) -> None:
        validator = JwtValidator(FixedClock(_NOW))
        with pytest.raises(TokenExpiredError):
            validator.validate(_claims(exp_delta=-1))

    def test_FEAT_010_2_leeway_allows_small_drift(self) -> None:
        validator = JwtValidator(FixedClock(_NOW), leeway_seconds=10)
        validator.validate(_claims(exp_delta=-5))

    def test_FEAT_010_2_raises_on_issuer_mismatch(self) -> None:
        validator = JwtValidator(FixedClock(_NOW), issuer="expected")
        with pytest.raises(TokenValidationError):
            validator.validate(_claims(issuer="other"))

    def test_FEAT_010_2_audience_tuple_match(self) -> None:
        validator = JwtValidator(FixedClock(_NOW), audience="api")
        validator.validate(_claims(audience=("web", "api")))

    def test_FEAT_010_2_raises_on_audience_mismatch(self) -> None:
        validator = JwtValidator(FixedClock(_NOW), audience="api")
        with pytest.raises(TokenValidationError):
            validator.validate(_claims(audience="web"))

    def test_FEAT_010_2_raises_when_audience_absent(self) -> None:
        validator = JwtValidator(FixedClock(_NOW), audience=("api",))
        with pytest.raises(TokenValidationError):
            validator.validate(_claims(audience=None))

    def test_FEAT_010_2_validate_algorithm_accepts_rs256(self) -> None:
        validator = JwtValidator(FixedClock(_NOW))
        assert validator.validate_algorithm("RS256").value == "RS256"

    @pytest.mark.parametrize("name", ["none", "HS256"])
    def test_FEAT_010_2_validate_algorithm_rejects(self, name: str) -> None:
        validator = JwtValidator(FixedClock(_NOW))
        with pytest.raises(InvalidAlgorithmError):
            validator.validate_algorithm(name)

    def test_FEAT_010_2_validate_algorithm_rejects_out_of_whitelist(self) -> None:
        from baobab_auth_security.tokens.jwt_algorithm import JwtAlgorithm

        validator = JwtValidator(
            FixedClock(_NOW), allowed_algorithms=(JwtAlgorithm.RS256,)
        )
        with pytest.raises(InvalidAlgorithmError):
            validator.validate_algorithm("RS512")
