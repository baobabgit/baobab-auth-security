"""Fixtures partagées pour les tests du module ``tokens``.

:spec: FEAT-010.2
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.exceptions import KeyNotFoundError
from baobab_auth_security.tokens.jwt_decoder import JwtDecoder
from baobab_auth_security.tokens.jwt_encoder import JwtEncoder

_KID = "test-key-1"


@pytest.fixture(scope="session")
def private_key() -> RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.fixture(scope="session")
def other_private_key() -> RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.fixture
def kid() -> str:
    return _KID


@pytest.fixture
def resolver(private_key: RSAPrivateKey):
    public = private_key.public_key()

    def _resolve(requested_kid: str) -> RSAPublicKey:
        if requested_kid != _KID:
            raise KeyNotFoundError(f"kid inconnu : {requested_kid}")
        return public

    return _resolve


@pytest.fixture
def encoder(private_key: RSAPrivateKey) -> JwtEncoder:
    return JwtEncoder(private_key, _KID)


@pytest.fixture
def decoder(resolver) -> JwtDecoder:
    return JwtDecoder(resolver)


@pytest.fixture
def now() -> datetime:
    return datetime(2026, 6, 29, 12, 0, tzinfo=UTC)


@pytest.fixture
def clock(now: datetime) -> FixedClock:
    return FixedClock(now)
