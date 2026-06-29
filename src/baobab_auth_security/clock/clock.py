"""Port ``Clock`` — horloge injectable, alignée sur ``baobab-auth-core``.

Plutôt que de redéfinir un port, ``baobab-auth-security`` réutilise le ``Protocol``
réel de ``baobab-auth-core`` (:class:`baobab_auth_core.ports.clock.Clock`). Les
implémentations concrètes :class:`SystemClock` et :class:`FixedClock` retournent
des datetimes **timezone-aware en UTC**.

:spec: FEAT-012.1, ADR-0005
"""

from __future__ import annotations

from baobab_auth_core.ports.clock import Clock

__all__ = ["Clock"]
