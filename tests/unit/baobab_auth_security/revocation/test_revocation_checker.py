"""Tests du port :class:`RevocationChecker`.

:spec: FEAT-011.1
"""

from __future__ import annotations

from baobab_auth_security.revocation.in_memory_revocation_checker import (
    InMemoryRevocationChecker,
)
from baobab_auth_security.revocation.revocation_checker import RevocationChecker


class TestRevocationChecker:
    """Vérifie la conformité structurelle au port."""

    def test_FEAT_011_1_in_memory_satisfies_protocol(self) -> None:
        assert isinstance(InMemoryRevocationChecker(), RevocationChecker)
