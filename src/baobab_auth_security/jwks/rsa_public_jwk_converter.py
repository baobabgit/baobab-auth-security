"""Conversion d'une clé publique RSA en JWK.

:spec: FEAT-010.4, ADR-0006
"""

from __future__ import annotations

import base64

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from baobab_auth_security.jwks.jwk import JWK
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm


class RsaPublicJwkConverter:
    """Convertit une clé publique RSA en :class:`JWK` (champs publics seuls)."""

    def to_jwk(
        self,
        public_key: RSAPublicKey,
        kid: str,
        algorithm: KeyAlgorithm = KeyAlgorithm.RS256,
    ) -> JWK:
        """Construit une JWK publique depuis une clé RSA.

        :param public_key: Clé publique RSA.
        :param kid: Identifiant de clé.
        :param algorithm: Algorithme associé.
        :returns: JWK publique (``n``, ``e`` en base64url).
        """
        numbers = public_key.public_numbers()
        return JWK(
            kid=kid,
            alg=algorithm.value,
            n=self._b64url_uint(numbers.n),
            e=self._b64url_uint(numbers.e),
        )

    @staticmethod
    def _b64url_uint(value: int) -> str:
        """Encode un entier non signé en base64url sans padding (RFC 7518).

        :param value: Entier positif.
        :returns: Chaîne base64url.
        """
        length = max(1, (value.bit_length() + 7) // 8)
        data = value.to_bytes(length, "big")
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")
