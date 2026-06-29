"""Intégration contractuelle : port ``PasswordHasher`` du core.

:spec: FEAT-011.1, ADR-0005
"""

from __future__ import annotations

from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.plain_password import PlainPassword
from baobab_auth_core.ports.password_hasher import PasswordHasher

from baobab_auth_security.integration.core_password_hasher_adapter import (
    CorePasswordHasherAdapter,
)
from baobab_auth_security.password.argon2_password_hasher import Argon2PasswordHasher
from baobab_auth_security.password.password_hash_policy import PasswordHashPolicy

_FAST = PasswordHashPolicy(time_cost=1, memory_cost=8, parallelism=1)


class TestCorePasswordHasherAdapterIntegration:
    """Vérifie la conformité au port réel de ``baobab-auth-core``."""

    def test_FEAT_011_1_satisfies_core_password_hasher_protocol(self) -> None:
        adapter = CorePasswordHasherAdapter(Argon2PasswordHasher(_FAST))
        assert isinstance(adapter, PasswordHasher)

    def test_FEAT_011_1_end_to_end_hash_and_verify(self) -> None:
        adapter = CorePasswordHasherAdapter(Argon2PasswordHasher(_FAST))
        plain = PlainPassword("correct horse battery staple")

        digest: PasswordHash = adapter.hash(plain)

        assert isinstance(digest, PasswordHash)
        assert adapter.verify(plain, digest) is True
        assert adapter.verify(PlainPassword("wrong"), digest) is False
