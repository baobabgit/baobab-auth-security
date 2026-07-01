"""Tests de :class:`RsaPublicJwkConverter`.

:spec: FEAT-010.4
"""

from __future__ import annotations

import base64

from baobab_auth_security.jwks.rsa_public_jwk_converter import RsaPublicJwkConverter
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm
from baobab_auth_security.keys.key_pair import KeyPair


def _b64url_to_int(value: str) -> int:
    padding = "=" * (-len(value) % 4)
    return int.from_bytes(base64.urlsafe_b64decode(value + padding), "big")


class TestRsaPublicJwkConverter:
    """Vérifie l'encodage RFC 7518 des composants publics RSA."""

    def test_FEAT_010_4_encodes_modulus_and_exponent(self, rsa_key: KeyPair) -> None:
        converter = RsaPublicJwkConverter()
        jwk = converter.to_jwk(rsa_key.public_key, rsa_key.kid, KeyAlgorithm.RS256)

        numbers = rsa_key.public_key.public_numbers()
        assert jwk.kid == rsa_key.kid
        assert jwk.alg == "RS256"
        assert _b64url_to_int(jwk.n) == numbers.n
        assert _b64url_to_int(jwk.e) == numbers.e

    def test_FEAT_010_4_no_base64_padding(self, rsa_key: KeyPair) -> None:
        jwk = RsaPublicJwkConverter().to_jwk(rsa_key.public_key, rsa_key.kid)
        assert "=" not in jwk.n
        assert "=" not in jwk.e
