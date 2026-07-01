"""Tests des convertisseurs JWK EC/OKP et composite.

:spec: FEAT-020.1
"""

from __future__ import annotations

from datetime import UTC, datetime

from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.jwks.ec_jwk import EcJwk
from baobab_auth_security.jwks.ec_public_jwk_converter import EcPublicJwkConverter
from baobab_auth_security.jwks.jwks_provider import LocalJwksProvider
from baobab_auth_security.jwks.okp_jwk import OkpJwk
from baobab_auth_security.jwks.okp_public_jwk_converter import OkpPublicJwkConverter
from baobab_auth_security.jwks.public_jwk_converter import PublicJwkConverter
from baobab_auth_security.keys.ec_key_generator import EcKeyGenerator
from baobab_auth_security.keys.ed25519_key_generator import Ed25519KeyGenerator
from baobab_auth_security.keys.in_memory_key_provider import InMemoryKeyProvider

_NOW = datetime(2026, 6, 28, 12, 0, tzinfo=UTC)


class TestEcOkpJwkConverters:
    """Vérifie la conversion et la publication JWKS multi-algorithmes."""

    def test_FEAT_020_1_ec_jwk_has_public_fields_only(self) -> None:
        pair = EcKeyGenerator(FixedClock(_NOW)).generate(kid="ec-1")
        jwk = EcPublicJwkConverter().to_jwk(pair.public_key, pair.kid, pair.algorithm)
        data = jwk.to_dict()
        assert isinstance(jwk, EcJwk)
        assert data["kty"] == "EC"
        assert "d" not in data

    def test_FEAT_020_1_okp_jwk_has_public_fields_only(self) -> None:
        pair = Ed25519KeyGenerator(FixedClock(_NOW)).generate(kid="ed-1")
        jwk = OkpPublicJwkConverter().to_jwk(pair.public_key, pair.kid, pair.algorithm)
        data = jwk.to_dict()
        assert isinstance(jwk, OkpJwk)
        assert data["crv"] == "Ed25519"
        assert "d" not in data

    def test_FEAT_020_1_local_jwks_publishes_mixed_keys(self) -> None:
        ec = EcKeyGenerator(FixedClock(_NOW)).generate(kid="ec-pub")
        ed = Ed25519KeyGenerator(FixedClock(_NOW)).generate(kid="ed-pub")
        provider = InMemoryKeyProvider((ec, ed))
        jwks = LocalJwksProvider(provider, PublicJwkConverter()).jwks()
        kids = jwks.key_ids()
        assert "ec-pub" in kids
        assert "ed-pub" in kids

    def test_FEAT_020_1_public_jwk_converter_rejects_unknown_type(self) -> None:
        from unittest.mock import Mock

        import pytest

        from baobab_auth_security.exceptions import ConfigurationError
        from baobab_auth_security.keys.key_algorithm import KeyAlgorithm

        converter = PublicJwkConverter()
        with pytest.raises(ConfigurationError):
            converter.to_jwk(Mock(), "kid", KeyAlgorithm.ES256)
