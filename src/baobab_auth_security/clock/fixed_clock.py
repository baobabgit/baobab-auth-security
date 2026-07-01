"""Horloge déterministe pour les tests.

:spec: FEAT-012.1
"""

from __future__ import annotations

from datetime import datetime

from baobab_auth_security.exceptions import ConfigurationError


class FixedClock:
    """Horloge renvoyant toujours le même instant (tests déterministes).

    Implémente structurellement le port
    :class:`baobab_auth_security.clock.clock.Clock`.

    :param moment: Instant fixe à renvoyer ; doit être **timezone-aware**.
    :raises ConfigurationError: Si ``moment`` est naïf (sans ``tzinfo``).
    """

    def __init__(self, moment: datetime) -> None:
        """Initialise l'horloge avec un instant fixe timezone-aware."""
        if moment.tzinfo is None:
            raise ConfigurationError(
                "FixedClock exige un datetime timezone-aware (UTC)."
            )
        self._moment = moment

    def now(self) -> datetime:
        """Retourne l'instant fixe configuré.

        :returns: Le datetime fixe (timezone-aware).
        """
        return self._moment
