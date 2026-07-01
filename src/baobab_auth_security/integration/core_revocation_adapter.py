"""Adaptateur de révocation utilisant le VO ``TokenId`` du core.

:spec: FEAT-011.1, ADR-0005
"""

from __future__ import annotations

from baobab_auth_core.domain.value_objects.token_id import TokenId

from baobab_auth_security.revocation.in_memory_revocation_checker import (
    InMemoryRevocationChecker,
)
from baobab_auth_security.revocation.revocation_checker import RevocationChecker


class CoreRevocationAdapter:
    """Adapte un :class:`RevocationChecker` aux ``TokenId`` du core.

    Traduit le value object ``TokenId`` du core vers le ``jti`` (chaîne) attendu
    par le vérificateur de révocation.

    :param checker: Vérificateur sous-jacent ; défaut
        :class:`InMemoryRevocationChecker`.
    """

    def __init__(self, checker: RevocationChecker | None = None) -> None:
        """Initialise l'adaptateur."""
        self._checker: RevocationChecker = checker or InMemoryRevocationChecker()

    def revoke(self, token_id: TokenId) -> None:
        """Révoque un token par son identifiant core.

        :param token_id: Identifiant du token (``TokenId`` du core).
        """
        self._checker.revoke(token_id.value)

    def is_revoked(self, token_id: TokenId) -> bool:
        """Indique si un token est révoqué.

        :param token_id: Identifiant du token (``TokenId`` du core).
        :returns: ``True`` si révoqué.
        """
        return self._checker.is_revoked(token_id.value)
