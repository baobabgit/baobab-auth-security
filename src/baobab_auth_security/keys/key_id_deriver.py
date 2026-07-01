"""Dérivation stable d'un ``kid`` depuis une clé publique.

:spec: FEAT-020.1
"""

from __future__ import annotations

import hashlib

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.types import PublicKeyTypes


class KeyIdDeriver:
    """Dérive un identifiant de clé stable à partir du matériel public."""

    @staticmethod
    def derive(public_key: PublicKeyTypes) -> str:
        """Calcule un ``kid`` hexadécimal (16 caractères) depuis la clé publique.

        :param public_key: Clé publique (RSA, EC ou OKP).
        :returns: ``kid`` dérivé par SHA-256 tronqué.
        """
        der = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return hashlib.sha256(der).hexdigest()[:16]
