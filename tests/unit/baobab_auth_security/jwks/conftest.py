"""Fixtures partagées pour les tests du module ``jwks``.

:spec: FEAT-010.4
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.keys.key_generator import KeyGenerator
from baobab_auth_security.keys.key_pair import KeyPair

_NOW = datetime(2026, 6, 29, 12, 0, tzinfo=UTC)


@pytest.fixture(scope="session")
def generator() -> KeyGenerator:
    return KeyGenerator(FixedClock(_NOW))


@pytest.fixture(scope="session")
def rsa_key(generator: KeyGenerator) -> KeyPair:
    return generator.generate(kid="jwks-key-1")
