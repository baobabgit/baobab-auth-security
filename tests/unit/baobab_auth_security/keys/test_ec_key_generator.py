"""Tests de :class:`EcKeyGenerator`.

:spec: FEAT-020.1
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.exceptions import ConfigurationError
from baobab_auth_security.keys.ec_key_generator import EcKeyGenerator
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm
from baobab_auth_security.keys.key_status import KeyStatus

_NOW = datetime(2026, 6, 28, 12, 0, tzinfo=UTC)


class TestEcKeyGenerator:
    """Vérifie la génération de paires EC."""

    def test_FEAT_020_1_generates_es256_key_pair(self) -> None:
        pair = EcKeyGenerator(FixedClock(_NOW)).generate()
        assert pair.algorithm is KeyAlgorithm.ES256
        assert pair.status is KeyStatus.ACTIVE
        assert pair.kid
        assert pair.created_at == _NOW

    def test_FEAT_020_1_honours_explicit_kid(self) -> None:
        pair = EcKeyGenerator(FixedClock(_NOW)).generate(kid="ec-test")
        assert pair.kid == "ec-test"

    def test_FEAT_020_1_rejects_non_ec_algorithm(self) -> None:
        with pytest.raises(ConfigurationError):
            EcKeyGenerator(FixedClock(_NOW)).generate(algorithm=KeyAlgorithm.RS256)
