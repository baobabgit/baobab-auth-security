"""Décodage base64url pour les champs JWK (RFC 7518).

:spec: FEAT-020.2
"""

from __future__ import annotations

import base64


class Base64UrlDecoder:
    """Décode des entiers et octets depuis le format base64url."""

    @staticmethod
    def decode_bytes(value: str) -> bytes:
        """Décode une chaîne base64url en octets.

        :param value: Valeur encodée sans padding.
        :returns: Octets décodés.
        """
        padding = "=" * (-len(value) % 4)
        return base64.urlsafe_b64decode(value + padding)

    @classmethod
    def decode_uint(cls, value: str) -> int:
        """Décode un entier non signé big-endian depuis base64url.

        :param value: Valeur encodée.
        :returns: Entier positif.
        """
        return int.from_bytes(cls.decode_bytes(value), "big")
