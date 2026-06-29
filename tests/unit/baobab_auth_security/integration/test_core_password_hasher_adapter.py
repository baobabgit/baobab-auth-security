"""Tests unitaires de :class:`CorePasswordHasherAdapter`.

:spec: FEAT-011.1
"""

from __future__ import annotations

from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.plain_password import PlainPassword

from baobab_auth_security.integration.core_password_hasher_adapter import (
    CorePasswordHasherAdapter,
)
from baobab_auth_security.password.argon2_password_hasher import Argon2PasswordHasher
from baobab_auth_security.password.password_hash_policy import PasswordHashPolicy

_FAST = PasswordHashPolicy(time_cost=1, memory_cost=8, parallelism=1)


class TestCorePasswordHasherAdapter:
    """Vérifie le mapping vers les value objects du core."""

    def test_FEAT_011_1_hash_returns_core_password_hash(self) -> None:
        adapter = CorePasswordHasherAdapter(Argon2PasswordHasher(_FAST))
        result = adapter.hash(PlainPassword("s3cret"))
        assert isinstance(result, PasswordHash)
        assert result.value.startswith("$argon2id$")

    def test_FEAT_011_1_verify_true_then_false(self) -> None:
        adapter = CorePasswordHasherAdapter(Argon2PasswordHasher(_FAST))
        digest = adapter.hash(PlainPassword("good"))
        assert adapter.verify(PlainPassword("good"), digest) is True
        assert adapter.verify(PlainPassword("bad"), digest) is False

    def test_FEAT_011_1_default_hasher_used(self) -> None:
        adapter = CorePasswordHasherAdapter()
        digest = adapter.hash(PlainPassword("x"))
        assert adapter.verify(PlainPassword("x"), digest) is True
