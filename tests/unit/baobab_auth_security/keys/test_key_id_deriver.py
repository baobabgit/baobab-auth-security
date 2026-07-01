"""Tests de :class:`KeyIdDeriver`.

:spec: FEAT-020.1
"""

from __future__ import annotations

from datetime import UTC, datetime

from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.keys.ec_key_generator import EcKeyGenerator
from baobab_auth_security.keys.key_generator import KeyGenerator
from baobab_auth_security.keys.key_id_deriver import KeyIdDeriver

_NOW = datetime(2026, 6, 28, 12, 0, tzinfo=UTC)


class TestKeyIdDeriver:
    """Vérifie la dérivation stable de ``kid``."""

    def test_FEAT_020_1_derive_is_stable_for_rsa(self) -> None:
        pair = KeyGenerator(FixedClock(_NOW)).generate()
        assert KeyIdDeriver.derive(pair.public_key) == pair.kid

    def test_FEAT_020_1_derive_is_stable_for_ec(self) -> None:
        pair = EcKeyGenerator(FixedClock(_NOW)).generate()
        assert KeyIdDeriver.derive(pair.public_key) == pair.kid
