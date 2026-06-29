"""Tests unitaires de :class:`CoreTokenProviderAdapter`.

:spec: FEAT-011.1, ADR-0005
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta

import pytest
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.exceptions.auth import TokenExpiredError, TokenInvalidError

from baobab_auth_security.integration.core_revocation_adapter import (
    CoreRevocationAdapter,
)
from baobab_auth_security.integration.core_token_provider_adapter import (
    CoreTokenProviderAdapter,
)
from baobab_auth_security.tokens.jwt_token_provider import JwtTokenProvider


class TestCoreTokenProviderAdapter:
    """Vérifie le respect du port ``TokenProvider`` réel."""

    def test_FEAT_011_1_generate_token_id_returns_core_token_id(
        self, adapter: CoreTokenProviderAdapter
    ) -> None:
        token_id = adapter.generate_token_id()
        assert isinstance(token_id, TokenId)
        assert token_id.value

    def test_FEAT_011_1_access_token_round_trip(
        self, adapter: CoreTokenProviderAdapter
    ) -> None:
        token = adapter.create_access_token(
            "user-1", 900, {"sid": "sess-1", "roles": ["ADMIN"]}
        )
        payload = adapter.verify_access_token(token)
        assert payload["sub"] == "user-1"
        assert payload["sid"] == "sess-1"
        assert payload["roles"] == ["ADMIN"]
        assert isinstance(payload["iat"], int)

    def test_FEAT_011_1_refresh_token_carries_token_id(
        self, adapter: CoreTokenProviderAdapter
    ) -> None:
        token_id = adapter.generate_token_id()
        token = adapter.create_refresh_token("user-1", token_id, 3600, {"sid": "s"})
        payload = adapter.verify_refresh_token(token)
        assert payload["refresh_token_id"] == token_id.value
        assert payload["jti"] == token_id.value

    def test_FEAT_011_1_revoked_token_is_rejected(
        self, adapter: CoreTokenProviderAdapter
    ) -> None:
        token = adapter.create_access_token("user-1", 900)
        adapter.revoke_token(token)
        with pytest.raises(TokenInvalidError):
            adapter.verify_access_token(token)

    def test_FEAT_011_1_invalid_token_raises_core_invalid(
        self, adapter: CoreTokenProviderAdapter
    ) -> None:
        with pytest.raises(TokenInvalidError):
            adapter.verify_access_token("not-a-jwt")

    def test_FEAT_011_1_expired_token_raises_core_expired(
        self,
        now: datetime,
        provider_factory: Callable[[datetime], JwtTokenProvider],
    ) -> None:
        issuer = CoreTokenProviderAdapter(provider_factory(now))
        token = issuer.create_access_token("user-1", 60)
        # Vérification 1 h plus tard.
        later = CoreTokenProviderAdapter(provider_factory(now + timedelta(hours=1)))
        with pytest.raises(TokenExpiredError):
            later.verify_access_token(token)

    def test_FEAT_011_1_revoke_ignores_invalid_token(
        self, adapter: CoreTokenProviderAdapter
    ) -> None:
        # Best-effort : ne lève pas sur token illisible.
        adapter.revoke_token("garbage")

    def test_FEAT_011_1_shared_revocation_state(
        self,
        now: datetime,
        provider_factory: Callable[[datetime], JwtTokenProvider],
    ) -> None:
        revocation = CoreRevocationAdapter()
        adapter = CoreTokenProviderAdapter(provider_factory(now), revocation=revocation)
        token = adapter.create_access_token("u", 900)
        payload = adapter.verify_access_token(token)
        revocation.revoke(TokenId(payload["jti"]))
        with pytest.raises(TokenInvalidError):
            adapter.verify_access_token(token)
