"""Fixtures partagées pour les tests d'intégration core (unitaires).

:spec: FEAT-011.1
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

import pytest

from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.integration.core_token_provider_adapter import (
    CoreTokenProviderAdapter,
)
from baobab_auth_security.keys.in_memory_key_provider import InMemoryKeyProvider
from baobab_auth_security.keys.key_generator import KeyGenerator
from baobab_auth_security.keys.key_pair import KeyPair
from baobab_auth_security.tokens.jwt_decoder import JwtDecoder
from baobab_auth_security.tokens.jwt_encoder import JwtEncoder
from baobab_auth_security.tokens.jwt_token_provider import JwtTokenProvider
from baobab_auth_security.tokens.jwt_validator import JwtValidator

NOW = datetime(2026, 6, 29, 12, 0, tzinfo=UTC)
ISSUER = "baobab-auth"
AUDIENCE = "api"


@pytest.fixture(scope="session")
def signing_key() -> KeyPair:
    return KeyGenerator(FixedClock(NOW)).generate(kid="adapter-key")


def build_jwt_provider(key_pair: KeyPair, moment: datetime) -> JwtTokenProvider:
    """Assemble un :class:`JwtTokenProvider` à un instant donné."""
    provider = InMemoryKeyProvider((key_pair,))
    clock = FixedClock(moment)
    encoder = JwtEncoder(key_pair.private_key, key_pair.kid)
    decoder = JwtDecoder(provider.public_key_for_kid)
    validator = JwtValidator(clock, issuer=ISSUER, audience=AUDIENCE)
    return JwtTokenProvider(
        encoder, decoder, validator, clock, issuer=ISSUER, audience=AUDIENCE
    )


@pytest.fixture
def now() -> datetime:
    return NOW


@pytest.fixture
def provider_factory(
    signing_key: KeyPair,
) -> Callable[[datetime], JwtTokenProvider]:
    def _factory(moment: datetime) -> JwtTokenProvider:
        return build_jwt_provider(signing_key, moment)

    return _factory


@pytest.fixture
def adapter(signing_key: KeyPair) -> CoreTokenProviderAdapter:
    return CoreTokenProviderAdapter(build_jwt_provider(signing_key, NOW))
