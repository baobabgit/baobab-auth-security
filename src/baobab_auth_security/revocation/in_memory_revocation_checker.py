"""Vérificateur de révocation en mémoire (par ``jti``).

:spec: FEAT-011.1
"""

from __future__ import annotations


class InMemoryRevocationChecker:
    """Révocation minimale par ``jti``, conservée en mémoire.

    Implémente structurellement le port
    :class:`baobab_auth_security.revocation.revocation_checker.RevocationChecker`.
    """

    def __init__(self) -> None:
        """Initialise un ensemble vide de ``jti`` révoqués."""
        self._revoked: set[str] = set()

    def revoke(self, jti: str) -> None:
        """Marque un ``jti`` comme révoqué.

        :param jti: Identifiant du token à révoquer.
        """
        self._revoked.add(jti)

    def is_revoked(self, jti: str) -> bool:
        """Indique si un ``jti`` est révoqué.

        :param jti: Identifiant à vérifier.
        :returns: ``True`` si révoqué.
        """
        return jti in self._revoked
