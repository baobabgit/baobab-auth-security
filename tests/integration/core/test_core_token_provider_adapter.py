"""Intégration contractuelle : port ``TokenProvider`` du core.

:spec: FEAT-011.1, ADR-0005
"""

from __future__ import annotations

from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.ports.token_provider import TokenProvider

from baobab_auth_security.integration.core_token_provider_adapter import (
    CoreTokenProviderAdapter,
)


class TestCoreTokenProviderAdapterIntegration:
    """Vérifie la conformité au port réel de ``baobab-auth-core``."""

    def test_FEAT_011_1_satisfies_core_token_provider_protocol(
        self, token_provider_adapter: CoreTokenProviderAdapter
    ) -> None:
        assert isinstance(token_provider_adapter, TokenProvider)

    def test_FEAT_011_1_access_token_end_to_end(
        self, token_provider_adapter: CoreTokenProviderAdapter
    ) -> None:
        token = token_provider_adapter.create_access_token(
            subject="user-1",
            ttl_seconds=900,
            claims={"sid": "sess-1", "roles": ["ADMIN"]},
        )
        payload = token_provider_adapter.verify_access_token(token)
        assert payload["sub"] == "user-1"
        assert payload["sid"] == "sess-1"
        assert payload["roles"] == ["ADMIN"]

    def test_FEAT_011_1_refresh_token_round_trip(
        self, token_provider_adapter: CoreTokenProviderAdapter
    ) -> None:
        token_id: TokenId = token_provider_adapter.generate_token_id()
        token = token_provider_adapter.create_refresh_token(
            subject="user-1", token_id=token_id, ttl_seconds=3600
        )
        payload = token_provider_adapter.verify_refresh_token(token)
        assert payload["refresh_token_id"] == token_id.value

    def test_FEAT_011_1_revoke_then_reject(
        self, token_provider_adapter: CoreTokenProviderAdapter
    ) -> None:
        from baobab_auth_core.exceptions.auth import TokenInvalidError

        token = token_provider_adapter.create_access_token("user-1", 900)
        token_provider_adapter.revoke_token(token)
        try:
            token_provider_adapter.verify_access_token(token)
        except TokenInvalidError:
            return
        raise AssertionError("Le token révoqué aurait dû être rejeté.")
