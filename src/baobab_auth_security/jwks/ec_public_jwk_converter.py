"""Conversion d'une clé publique EC en JWK.

:spec: FEAT-020.1, ADR-0006
"""

from __future__ import annotations

import base64

from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey

from baobab_auth_security.jwks.ec_jwk import EcJwk
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm

_CURVE_NAME_BY_ALGORITHM: dict[KeyAlgorithm, str] = {
    KeyAlgorithm.ES256: "P-256",
    KeyAlgorithm.ES384: "P-384",
    KeyAlgorithm.ES512: "P-521",
}


class EcPublicJwkConverter:
    """Convertit une clé publique EC en :class:`EcJwk`."""

    def to_jwk(
        self,
        public_key: EllipticCurvePublicKey,
        kid: str,
        algorithm: KeyAlgorithm = KeyAlgorithm.ES256,
    ) -> EcJwk:
        """Construit une JWK publique depuis une clé EC.

        :param public_key: Clé publique EC.
        :param kid: Identifiant de clé.
        :param algorithm: Algorithme ES* associé.
        :returns: JWK publique (``crv``, ``x``, ``y`` en base64url).
        """
        numbers = public_key.public_numbers()
        curve_name = _CURVE_NAME_BY_ALGORITHM.get(algorithm, public_key.curve.name)
        return EcJwk(
            kid=kid,
            alg=algorithm.value,
            crv=curve_name,
            x=self._b64url_uint(numbers.x),
            y=self._b64url_uint(numbers.y),
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
