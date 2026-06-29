"""Résultat typé de génération d'un refresh token opaque.

:spec: FEAT-010.3, ADR-0004, ADR-0006
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from baobab_auth_security.exceptions import RefreshTokenError


@dataclass(frozen=True)
class RefreshTokenResult:
    """Refresh token généré : clair (éphémère), hash et métadonnées.

    Le token en clair (:attr:`token`) n'est exposé **qu'une seule fois** à
    l'appelant et masqué dans :meth:`__repr__` / :meth:`__str__`. Seul
    :attr:`token_hash` est destiné à la persistance externe.

    :param token: Refresh token opaque en clair (à transmettre une seule fois).
    :param token_hash: Hash SHA-256 du token (stockable).
    :param token_id: Identifiant du token (``jti``).
    :param issued_at: Date d'émission (UTC aware).
    :param expires_at: Date d'expiration (UTC aware).
    :raises RefreshTokenError: Si un champ obligatoire est vide ou une date naïve.
    """

    token: str
    token_hash: str
    token_id: str
    issued_at: datetime
    expires_at: datetime

    def __post_init__(self) -> None:
        """Valide les champs et l'aware-ness des dates.

        :raises RefreshTokenError: Si invalide.
        """
        if not self.token or not self.token_hash or not self.token_id:
            raise RefreshTokenError("Champs de refresh token incomplets.")
        if self.issued_at.tzinfo is None or self.expires_at.tzinfo is None:
            raise RefreshTokenError("Les dates doivent être timezone-aware (UTC).")

    def __str__(self) -> str:
        """Retourne une représentation masquant le token en clair.

        :returns: ``'***'``.
        """
        return "***"

    def __repr__(self) -> str:
        """Retourne une représentation masquant le token en clair.

        :returns: Représentation sans valeur de token en clair.
        """
        return (
            f"RefreshTokenResult(token='***', token_hash='***', "
            f"token_id={self.token_id!r}, issued_at={self.issued_at!r}, "
            f"expires_at={self.expires_at!r})"
        )
