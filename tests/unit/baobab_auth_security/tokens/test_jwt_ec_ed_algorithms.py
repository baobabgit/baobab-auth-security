"""Tests JWT ES256 et EdDSA (round-trip).

:spec: FEAT-020.1
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.keys.ec_key_generator import EcKeyGenerator
from baobab_auth_security.keys.ed25519_key_generator import Ed25519KeyGenerator
from baobab_auth_security.keys.in_memory_key_provider import InMemoryKeyProvider
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm
from baobab_auth_security.tokens.jwt_algorithm import JwtAlgorithm
from baobab_auth_security.tokens.jwt_decoder import JwtDecoder
from baobab_auth_security.tokens.jwt_encoder import JwtEncoder
from baobab_auth_security.tokens.jwt_validator import JwtValidator
from baobab_auth_security.tokens.security_token_claims import SecurityTokenClaims

_NOW = datetime(2026, 6, 28, 12, 0, tzinfo=UTC)


class TestJwtEcEdAlgorithms:
    """Vérifie l'encodage et le décodage EC/EdDSA."""

    def test_FEAT_020_1_es256_round_trip(self) -> None:
        pair = EcKeyGenerator(FixedClock(_NOW)).generate(
            algorithm=KeyAlgorithm.ES256, kid="ec-kid"
        )
        provider = InMemoryKeyProvider((pair,))
        encoder = JwtEncoder(pair.private_key, pair.kid, algorithm=JwtAlgorithm.ES256)
        decoder = JwtDecoder(
            provider.public_key_for_kid,
            algorithms=(JwtAlgorithm.ES256,),
        )
        claims = SecurityTokenClaims(
            sub="user",
            jti="jti-1",
            issued_at=_NOW,
            expires_at=_NOW + timedelta(minutes=5),
        )
        token = encoder.encode(claims)
        decoded = decoder.decode(token)
        assert decoded.sub == "user"
        JwtValidator(FixedClock(_NOW)).validate(decoded)

    def test_FEAT_020_1_eddsa_round_trip(self) -> None:
        pair = Ed25519KeyGenerator(FixedClock(_NOW)).generate(kid="ed-kid")
        provider = InMemoryKeyProvider((pair,))
        encoder = JwtEncoder(pair.private_key, pair.kid, algorithm=JwtAlgorithm.EdDSA)
        decoder = JwtDecoder(
            provider.public_key_for_kid,
            algorithms=(JwtAlgorithm.EdDSA,),
        )
        claims = SecurityTokenClaims(
            sub="user",
            jti="jti-2",
            issued_at=_NOW,
            expires_at=_NOW + timedelta(minutes=5),
        )
        token = encoder.encode(claims)
        decoded = decoder.decode(token)
        assert decoded.jti == "jti-2"
