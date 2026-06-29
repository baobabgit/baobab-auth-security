"""Statuts du cycle de vie d'une clé.

:spec: FEAT-010.4
"""

from __future__ import annotations

from enum import StrEnum


class KeyStatus(StrEnum):
    """Cycle de vie d'une paire de clés.

    - ``PENDING`` : générée, pas encore active.
    - ``ACTIVE`` : utilisée pour signer ; publiée au JWKS.
    - ``RETIRED`` : plus utilisée pour signer ; peut rester publiée pour
      vérifier d'anciens tokens.
    """

    PENDING = "pending"
    ACTIVE = "active"
    RETIRED = "retired"
