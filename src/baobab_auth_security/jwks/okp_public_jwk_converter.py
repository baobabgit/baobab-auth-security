"""Conversion d'une clé publique Ed25519 en JWK.

:spec: FEAT-020.1, ADR-0006
"""

from __future__ import annotations

import base64

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from baobab_auth_security.jwks.okp_jwk import OkpJwk
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm


class OkpPublicJwkConverter:
    """Convertit une clé publique Ed25519 en :class:`OkpJwk`."""

    def to_jwk(
        self,
        public_key: Ed25519PublicKey,
        kid: str,
        algorithm: KeyAlgorithm = KeyAlgorithm.EdDSA,
    ) -> OkpJwk:
        """Construit une JWK publique depuis une clé Ed25519.

        :param public_key: Clé publique OKP.
        :param kid: Identifiant de clé.
        :param algorithm: Algorithme associé (``EdDSA``).
        :returns: JWK publique (``crv``, ``x`` en base64url).
        """
        raw = public_key.public_bytes_raw()
        return OkpJwk(
            kid=kid,
            alg=algorithm.value,
            crv="Ed25519",
            x=base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii"),
        )
