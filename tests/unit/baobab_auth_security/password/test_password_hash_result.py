"""Tests de :class:`PasswordHashResult`.

:spec: FEAT-010.1, ADR-0006
"""

from __future__ import annotations

import pytest

from baobab_auth_security.exceptions import PasswordHashingError
from baobab_auth_security.password.password_hash_result import PasswordHashResult


class TestPasswordHashResult:
    """Vérifie l'exposition contrôlée et le masquage du hash."""

    def test_FEAT_010_1_value_is_accessible(self) -> None:
        result = PasswordHashResult("$argon2id$abc")
        assert result.value == "$argon2id$abc"

    def test_FEAT_010_1_repr_and_str_are_masked(self) -> None:
        result = PasswordHashResult("$argon2id$secret-digest")
        assert "secret-digest" not in repr(result)
        assert "secret-digest" not in str(result)
        assert str(result) == "***"

    def test_FEAT_010_1_rejects_empty_value(self) -> None:
        with pytest.raises(PasswordHashingError):
            PasswordHashResult("")
