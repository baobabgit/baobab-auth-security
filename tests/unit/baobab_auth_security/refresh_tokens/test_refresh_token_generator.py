"""Tests de :class:`RefreshTokenGenerator`.

:spec: FEAT-010.3
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.exceptions import ConfigurationError
from baobab_auth_security.refresh_tokens.refresh_token_generator import (
    RefreshTokenGenerator,
)
from baobab_auth_security.refresh_tokens.refresh_token_hasher import RefreshTokenHasher

_NOW = datetime(2026, 6, 29, 12, 0, tzinfo=UTC)


class TestRefreshTokenGenerator:
    """Vérifie l'entropie, le hash et les dates des refresh tokens."""

    def test_FEAT_010_3_generate_produces_consistent_result(self) -> None:
        generator = RefreshTokenGenerator(FixedClock(_NOW))

        result = generator.generate(ttl_seconds=3600)

        assert result.token
        assert result.token_id
        assert RefreshTokenHasher().hash(result.token) == result.token_hash
        assert result.issued_at == _NOW
        assert result.expires_at == _NOW + timedelta(seconds=3600)

    def test_FEAT_010_3_tokens_are_unique(self) -> None:
        generator = RefreshTokenGenerator(FixedClock(_NOW))
        first = generator.generate()
        second = generator.generate()
        assert first.token != second.token
        assert first.token_id != second.token_id

    def test_FEAT_010_3_accepts_explicit_token_id(self) -> None:
        generator = RefreshTokenGenerator(FixedClock(_NOW))
        result = generator.generate(token_id="jti-provided")
        assert result.token_id == "jti-provided"

    def test_FEAT_010_3_uses_default_ttl_when_unset(self) -> None:
        generator = RefreshTokenGenerator(FixedClock(_NOW), default_ttl_seconds=120)
        result = generator.generate()
        assert result.expires_at == _NOW + timedelta(seconds=120)

    def test_FEAT_010_3_rejects_low_entropy(self) -> None:
        with pytest.raises(ConfigurationError):
            RefreshTokenGenerator(FixedClock(_NOW), token_nbytes=16)
