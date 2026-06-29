"""Chargement de clés RSA depuis du PEM.

:spec: FEAT-010.4
"""

from __future__ import annotations

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from baobab_auth_security.exceptions import KeyManagementError


class PemKeyLoader:
    """Charge des clés RSA privées/publiques au format PEM."""

    def load_private_key(
        self, pem: str | bytes, password: bytes | None = None
    ) -> RSAPrivateKey:
        """Charge une clé privée RSA depuis du PEM.

        :param pem: Contenu PEM (str ou bytes).
        :param password: Mot de passe de déchiffrement, ou ``None``.
        :returns: Clé privée RSA.
        :raises KeyManagementError: Si le PEM est invalide ou non-RSA.
        """
        data = pem.encode("utf-8") if isinstance(pem, str) else pem
        try:
            key = serialization.load_pem_private_key(data, password=password)
        except (ValueError, TypeError) as exc:
            raise KeyManagementError("Clé privée PEM invalide.") from exc
        if not isinstance(key, RSAPrivateKey):
            raise KeyManagementError("La clé privée n'est pas une clé RSA.")
        return key

    def load_public_key(self, pem: str | bytes) -> RSAPublicKey:
        """Charge une clé publique RSA depuis du PEM.

        :param pem: Contenu PEM (str ou bytes).
        :returns: Clé publique RSA.
        :raises KeyManagementError: Si le PEM est invalide ou non-RSA.
        """
        data = pem.encode("utf-8") if isinstance(pem, str) else pem
        try:
            key = serialization.load_pem_public_key(data)
        except (ValueError, TypeError) as exc:
            raise KeyManagementError("Clé publique PEM invalide.") from exc
        if not isinstance(key, RSAPublicKey):
            raise KeyManagementError("La clé publique n'est pas une clé RSA.")
        return key
