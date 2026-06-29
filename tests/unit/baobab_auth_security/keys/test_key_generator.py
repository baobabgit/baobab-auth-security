"""Tests de :class:`KeyGenerator`.

:spec: FEAT-010.4
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.exceptions import ConfigurationError
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm
from baobab_auth_security.keys.key_generator import KeyGenerator
from baobab_auth_security.keys.key_status import KeyStatus

_NOW = datetime(2026, 6, 29, 12, 0, tzinfo=UTC)


class TestKeyGenerator:
    """Vérifie la génération de clés RSA et leurs métadonnées."""

    def test_FEAT_010_4_generates_rsa_key_pair(self, generator: KeyGenerator) -> None:
        pair = generator.generate()
        assert isinstance(pair.private_key, RSAPrivateKey)
        assert pair.private_key.key_size >= 2048
        assert pair.status is KeyStatus.ACTIVE
        assert pair.algorithm is KeyAlgorithm.RS256
        assert pair.created_at == _NOW

    def test_FEAT_010_4_kid_is_derived_hex_when_absent(self) -> None:
        gen = KeyGenerator(FixedClock(_NOW))
        pair = gen.generate()
        # kid dérivé de la clé publique : 16 caractères hexadécimaux.
        assert len(pair.kid) == 16
        assert all(c in "0123456789abcdef" for c in pair.kid)

    def test_FEAT_010_4_honours_explicit_kid(self, generator: KeyGenerator) -> None:
        assert generator.generate(kid="my-kid").kid == "my-kid"

    def test_FEAT_010_4_rejects_small_key_size(self) -> None:
        with pytest.raises(ConfigurationError):
            KeyGenerator(FixedClock(_NOW), key_size=1024)
