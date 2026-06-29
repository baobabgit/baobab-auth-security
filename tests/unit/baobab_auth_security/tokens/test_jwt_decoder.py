"""Tests de :class:`JwtDecoder` (vérification de signature, durcissement).

:spec: FEAT-010.2, ADR-0003
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from baobab_auth_security.exceptions import (
    InvalidAlgorithmError,
    KeyNotFoundError,
    TokenSignatureError,
    TokenValidationError,
)
from baobab_auth_security.tokens.jwt_algorithm import JwtAlgorithm
from baobab_auth_security.tokens.jwt_decoder import JwtDecoder
from baobab_auth_security.tokens.jwt_encoder import JwtEncoder
from baobab_auth_security.tokens.security_token_claims import SecurityTokenClaims

_NOW = datetime(2026, 6, 29, 12, 0, tzinfo=UTC)


def _claims() -> SecurityTokenClaims:
    return SecurityTokenClaims(
        sub="u", jti="j", issued_at=_NOW, expires_at=_NOW + timedelta(minutes=5)
    )


class TestJwtDecoder:
    """Cas nominaux et négatifs du décodage."""

    def test_FEAT_010_2_decodes_valid_token(
        self, encoder: JwtEncoder, decoder: JwtDecoder
    ) -> None:
        assert decoder.decode(encoder.encode(_claims())).sub == "u"

    def test_FEAT_010_2_rejects_tampered_token(
        self, encoder: JwtEncoder, decoder: JwtDecoder
    ) -> None:
        token = encoder.encode(_claims())
        tampered = token[:-3] + ("aaa" if token[-3:] != "aaa" else "bbb")
        with pytest.raises(TokenValidationError):
            decoder.decode(tampered)

    def test_FEAT_010_2_rejects_wrong_signing_key(
        self, other_private_key: RSAPrivateKey, decoder: JwtDecoder
    ) -> None:
        rogue = JwtEncoder(other_private_key, "test-key-1")
        with pytest.raises(TokenSignatureError):
            decoder.decode(rogue.encode(_claims()))

    def test_FEAT_010_2_rejects_alg_none(self, decoder: JwtDecoder) -> None:
        forged = jwt.encode(
            {"sub": "u", "jti": "j"},
            key="",
            algorithm="none",
            headers={"kid": "test-key-1"},
        )
        with pytest.raises(InvalidAlgorithmError):
            decoder.decode(forged)

    def test_FEAT_010_2_rejects_missing_kid(
        self, private_key: RSAPrivateKey, decoder: JwtDecoder
    ) -> None:
        token = jwt.encode({"sub": "u", "jti": "j"}, private_key, algorithm="RS256")
        with pytest.raises(TokenSignatureError):
            decoder.decode(token)

    def test_FEAT_010_2_unknown_kid_raises_key_not_found(
        self, private_key: RSAPrivateKey, decoder: JwtDecoder
    ) -> None:
        token = jwt.encode(
            {"sub": "u", "jti": "j"},
            private_key,
            algorithm="RS256",
            headers={"kid": "absent"},
        )
        with pytest.raises(KeyNotFoundError):
            decoder.decode(token)

    def test_FEAT_010_2_rejects_unreadable_token(self, decoder: JwtDecoder) -> None:
        with pytest.raises(TokenValidationError):
            decoder.decode("not-a-jwt")

    def test_FEAT_010_2_rejects_algorithm_outside_decoder_whitelist(
        self, private_key: RSAPrivateKey, resolver
    ) -> None:
        # Décodeur restreint à RS256 ; token signé RS384 -> refusé.
        decoder = JwtDecoder(resolver, algorithms=(JwtAlgorithm.RS256,))
        encoder = JwtEncoder(private_key, "test-key-1", JwtAlgorithm.RS384)
        with pytest.raises(InvalidAlgorithmError):
            decoder.decode(encoder.encode(_claims()))

    def test_FEAT_010_2_rejects_valid_signature_with_non_json_payload(
        self, private_key: RSAPrivateKey, decoder: JwtDecoder
    ) -> None:
        # Signature valide mais charge utile non-JSON -> PyJWTError non-signature.
        token = jwt.PyJWS().encode(
            b"not-json-payload",
            private_key,
            algorithm="RS256",
            headers={"kid": "test-key-1"},
        )
        with pytest.raises(TokenValidationError):
            decoder.decode(token)

    def test_FEAT_010_2_rejects_incomplete_claims(
        self, private_key: RSAPrivateKey, decoder: JwtDecoder
    ) -> None:
        # Token signé mais sans 'jti' ni 'iat'/'exp' -> claims incomplets.
        token = jwt.encode(
            {"sub": "u"},
            private_key,
            algorithm="RS256",
            headers={"kid": "test-key-1"},
        )
        with pytest.raises(TokenValidationError):
            decoder.decode(token)
