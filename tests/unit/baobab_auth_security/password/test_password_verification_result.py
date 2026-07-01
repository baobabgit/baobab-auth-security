"""Tests de :class:`PasswordVerificationResult`.

:spec: FEAT-010.1
"""

from __future__ import annotations

from baobab_auth_security.password.password_verification_result import (
    PasswordVerificationResult,
)


class TestPasswordVerificationResult:
    """Vérifie la sémantique du résultat de vérification."""

    def test_FEAT_010_1_truthiness_follows_is_valid(self) -> None:
        assert bool(PasswordVerificationResult(is_valid=True)) is True
        assert bool(PasswordVerificationResult(is_valid=False)) is False

    def test_FEAT_010_1_needs_rehash_defaults_false(self) -> None:
        assert PasswordVerificationResult(is_valid=True).needs_rehash is False
