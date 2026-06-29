"""Tests de :class:`InMemoryRevocationChecker`.

:spec: FEAT-011.1
"""

from __future__ import annotations

from baobab_auth_security.revocation.in_memory_revocation_checker import (
    InMemoryRevocationChecker,
)


class TestInMemoryRevocationChecker:
    """Vérifie la révocation par ``jti`` en mémoire."""

    def test_FEAT_011_1_unknown_jti_is_not_revoked(self) -> None:
        assert InMemoryRevocationChecker().is_revoked("absent") is False

    def test_FEAT_011_1_revoke_marks_jti(self) -> None:
        checker = InMemoryRevocationChecker()
        checker.revoke("jti-1")
        assert checker.is_revoked("jti-1") is True
