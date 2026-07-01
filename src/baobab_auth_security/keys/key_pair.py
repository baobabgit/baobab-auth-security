"""Paire de clés RSA et ses métadonnées.

:spec: FEAT-010.4, ADR-0006
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from baobab_auth_security.exceptions import KeyManagementError
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm
from baobab_auth_security.keys.key_status import KeyStatus


@dataclass(frozen=True)
class KeyPair:
    """Paire de clés RSA active/retirée, avec ``kid`` et statut.

    La clé privée n'apparaît **jamais** dans :meth:`__repr__` (ADR-0006).

    :param kid: Identifiant de clé (publié dans le header JWT et le JWKS).
    :param algorithm: Algorithme de signature associé.
    :param private_key: Clé privée RSA (jamais exposée hors signature).
    :param public_key: Clé publique RSA (exposée au JWKS).
    :param status: Statut de cycle de vie.
    :param created_at: Date de création (UTC aware).
    :raises KeyManagementError: Si ``kid`` est vide ou ``created_at`` naïf.
    """

    kid: str
    algorithm: KeyAlgorithm
    private_key: RSAPrivateKey
    public_key: RSAPublicKey
    status: KeyStatus
    created_at: datetime

    def __post_init__(self) -> None:
        """Valide le ``kid`` et l'aware-ness de la date.

        :raises KeyManagementError: Si invalide.
        """
        if not self.kid:
            raise KeyManagementError("kid de clé vide.")
        if self.created_at.tzinfo is None:
            raise KeyManagementError("created_at doit être timezone-aware (UTC).")

    def __repr__(self) -> str:
        """Représentation masquant la clé privée.

        :returns: Représentation sans matériel de clé privée.
        """
        return (
            f"KeyPair(kid={self.kid!r}, algorithm={self.algorithm.value!r}, "
            f"status={self.status.value!r}, private_key='***')"
        )
