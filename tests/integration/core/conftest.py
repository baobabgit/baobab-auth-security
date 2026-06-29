"""Fixtures pour les tests d'intégration contractuels avec ``baobab-auth-core``.

:spec: FEAT-011.1
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.integration.core_token_provider_adapter import (
    CoreTokenProviderAdapter,
)
from baobab_auth_security.keys.in_memory_key_provider import InMemoryKeyProvider
from baobab_auth_security.keys.key_generator import KeyGenerator
from baobab_auth_security.tokens.jwt_decoder import JwtDecoder
from baobab_auth_security.tokens.jwt_encoder import JwtEncoder
from baobab_auth_security.tokens.jwt_token_provider import JwtTokenProvider
from baobab_auth_security.tokens.jwt_validator import JwtValidator

_NOW = datetime(2026, 6, 29, 12, 0, tzinfo=UTC)


@pytest.fixture
def token_provider_adapter() -> CoreTokenProviderAdapter:
    clock = FixedClock(_NOW)
    key_pair = KeyGenerator(clock).generate(kid="integration-key")
    provider = InMemoryKeyProvider((key_pair,))
    jwt_provider = JwtTokenProvider(
        JwtEncoder(key_pair.private_key, key_pair.kid),
        JwtDecoder(provider.public_key_for_kid),
        JwtValidator(clock, issuer="baobab-auth", audience="api"),
        clock,
        issuer="baobab-auth",
        audience="api",
    )
    return CoreTokenProviderAdapter(jwt_provider)
