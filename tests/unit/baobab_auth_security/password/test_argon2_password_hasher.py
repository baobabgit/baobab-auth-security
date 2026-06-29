"""Tests de :class:`Argon2PasswordHasher`.

:spec: FEAT-010.1
"""

from __future__ import annotations

import pytest

from baobab_auth_security.exceptions import PasswordHashingError
from baobab_auth_security.password.argon2_password_hasher import Argon2PasswordHasher
from baobab_auth_security.password.password_hash_policy import PasswordHashPolicy
from baobab_auth_security.password.password_hash_result import PasswordHashResult

# Politique « légère » pour accélérer les tests (toujours valide).
_FAST = PasswordHashPolicy(time_cost=1, memory_cost=8, parallelism=1)


class TestArgon2PasswordHasher:
    """Cas nominaux et négatifs du hachage Argon2id."""

    def test_FEAT_010_1_hash_is_argon2id_and_non_reversible(self) -> None:
        # Arrange
        hasher = Argon2PasswordHasher(_FAST)

        # Act
        result = hasher.hash("s3cret-pass")

        # Assert
        assert isinstance(result, PasswordHashResult)
        assert result.value.startswith("$argon2id$")
        assert "s3cret-pass" not in result.value

    def test_FEAT_010_1_hash_is_salted_unique(self) -> None:
        hasher = Argon2PasswordHasher(_FAST)
        assert hasher.hash("pw").value != hasher.hash("pw").value

    def test_FEAT_010_1_verify_accepts_correct_password(self) -> None:
        hasher = Argon2PasswordHasher(_FAST)
        digest = hasher.hash("good").value

        result = hasher.verify("good", digest)

        assert result.is_valid is True
        assert bool(result) is True

    def test_FEAT_010_1_verify_rejects_wrong_password_without_raising(self) -> None:
        hasher = Argon2PasswordHasher(_FAST)
        digest = hasher.hash("good").value

        result = hasher.verify("wrong", digest)

        assert result.is_valid is False
        assert result.needs_rehash is False

    def test_FEAT_010_1_verify_raises_on_malformed_hash(self) -> None:
        hasher = Argon2PasswordHasher(_FAST)
        with pytest.raises(PasswordHashingError):
            hasher.verify("good", "not-a-valid-hash")

    def test_FEAT_010_1_hash_rejects_empty_password(self) -> None:
        hasher = Argon2PasswordHasher(_FAST)
        with pytest.raises(PasswordHashingError):
            hasher.hash("")

    def test_FEAT_010_1_needs_rehash_detects_param_change(self) -> None:
        # Arrange : hash produit avec une politique faible
        weak = Argon2PasswordHasher(
            PasswordHashPolicy(time_cost=1, memory_cost=8, parallelism=1)
        )
        digest = weak.hash("pw").value

        # Act : vérifié par un hasher à coût plus élevé
        strong = Argon2PasswordHasher(
            PasswordHashPolicy(time_cost=3, memory_cost=64, parallelism=1)
        )

        # Assert
        assert strong.needs_rehash(digest) is True
        assert strong.verify("pw", digest).needs_rehash is True

    def test_FEAT_010_1_needs_rehash_false_for_current_params(self) -> None:
        hasher = Argon2PasswordHasher(_FAST)
        digest = hasher.hash("pw").value
        assert hasher.needs_rehash(digest) is False

    def test_FEAT_010_1_default_policy_used_when_none(self) -> None:
        hasher = Argon2PasswordHasher()
        assert hasher.policy == PasswordHashPolicy()
