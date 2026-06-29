"""Port de vérification de révocation par ``jti``.

:spec: FEAT-011.1
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class RevocationChecker(Protocol):
    """Abstraction de la révocation d'un token par son ``jti``."""

    def revoke(self, jti: str) -> None:
        """Marque un ``jti`` comme révoqué.

        :param jti: Identifiant du token à révoquer.
        """
        ...

    def is_revoked(self, jti: str) -> bool:
        """Indique si un ``jti`` est révoqué.

        :param jti: Identifiant du token à vérifier.
        :returns: ``True`` si révoqué.
        """
        ...
