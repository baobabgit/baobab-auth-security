"""Paire de tokens (access + refresh) émise par la brique security.

:spec: FEAT-010.2, ADR-0006
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityTokenPair:
    """Paire de tokens retournée lors d'une émission.

    Les valeurs des tokens sont masquées dans :meth:`__repr__` pour éviter toute
    fuite dans les logs.

    :param access_token: Access token JWT sérialisé.
    :param refresh_token: Refresh token opaque (rendu une seule fois en clair).
    :param token_type: Type de token (``"Bearer"``).
    :param expires_in: Durée de vie de l'access token, en secondes.
    :param refresh_expires_in: Durée de vie du refresh token, en secondes.
    """

    access_token: str
    refresh_token: str
    expires_in: int
    refresh_expires_in: int
    token_type: str = "Bearer"

    def __repr__(self) -> str:
        """Représentation masquant les valeurs de tokens.

        :returns: Représentation sans valeur de token.
        """
        return (
            "SecurityTokenPair(access_token='***', refresh_token='***', "
            f"token_type={self.token_type!r}, expires_in={self.expires_in}, "
            f"refresh_expires_in={self.refresh_expires_in})"
        )
