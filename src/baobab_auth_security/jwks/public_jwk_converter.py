"""Conversion polymorphe d'une clé publique en JWK.

:spec: FEAT-020.1, ADR-0006
"""

from __future__ import annotations

from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.types import PublicKeyTypes

from baobab_auth_security.exceptions import ConfigurationError
from baobab_auth_security.jwks.ec_public_jwk_converter import EcPublicJwkConverter
from baobab_auth_security.jwks.okp_public_jwk_converter import OkpPublicJwkConverter
from baobab_auth_security.jwks.public_jwk import PublicJwk
from baobab_auth_security.jwks.rsa_public_jwk_converter import RsaPublicJwkConverter
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm


class PublicJwkConverter:
    """Délègue la conversion JWK selon le type de clé publique."""

    def __init__(
        self,
        rsa_converter: RsaPublicJwkConverter | None = None,
        ec_converter: EcPublicJwkConverter | None = None,
        okp_converter: OkpPublicJwkConverter | None = None,
    ) -> None:
        """Initialise les convertisseurs spécialisés."""
        self._rsa = rsa_converter or RsaPublicJwkConverter()
        self._ec = ec_converter or EcPublicJwkConverter()
        self._okp = okp_converter or OkpPublicJwkConverter()

    def to_jwk(
        self,
        public_key: PublicKeyTypes,
        kid: str,
        algorithm: KeyAlgorithm,
    ) -> PublicJwk:
        """Construit une JWK publique depuis une clé asymétrique.

        :param public_key: Clé publique RSA, EC ou OKP.
        :param kid: Identifiant de clé.
        :param algorithm: Algorithme de signature associé.
        :returns: JWK publique typée.
        :raises ConfigurationError: Si le type de clé est inconnu.
        """
        if isinstance(public_key, RSAPublicKey):
            return self._rsa.to_jwk(public_key, kid, algorithm)
        if isinstance(public_key, EllipticCurvePublicKey):
            return self._ec.to_jwk(public_key, kid, algorithm)
        if isinstance(public_key, Ed25519PublicKey):
            return self._okp.to_jwk(public_key, kid, algorithm)
        raise ConfigurationError(
            f"Type de clé publique non supporté pour JWK : {type(public_key)!r}."
        )
