"""Horloge système renvoyant l'heure courante en UTC.

:spec: FEAT-012.1
"""

from __future__ import annotations

from datetime import UTC, datetime


class SystemClock:
    """Horloge fondée sur l'heure système, toujours en UTC.

    Implémente structurellement le port
    :class:`baobab_auth_security.clock.clock.Clock`.
    """

    def now(self) -> datetime:
        """Retourne l'instant courant en UTC (timezone-aware).

        :returns: Datetime courant, ``tzinfo`` = UTC.
        """
        return datetime.now(UTC)
