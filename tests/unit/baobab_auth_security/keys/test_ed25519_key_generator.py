"""Tests de :class:`Ed25519KeyGenerator`.

:spec: FEAT-020.1
"""

from __future__ import annotations

from datetime import UTC, datetime

from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.keys.ed25519_key_generator import Ed25519KeyGenerator
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm
from baobab_auth_security.keys.key_status import KeyStatus

_NOW = datetime(2026, 6, 28, 12, 0, tzinfo=UTC)


class TestEd25519KeyGenerator:
    """Vérifie la génération de paires Ed25519."""

    def test_FEAT_020_1_generates_eddsa_key_pair(self) -> None:
        pair = Ed25519KeyGenerator(FixedClock(_NOW)).generate()
        assert pair.algorithm is KeyAlgorithm.EdDSA
        assert pair.status is KeyStatus.ACTIVE
        assert pair.kid
