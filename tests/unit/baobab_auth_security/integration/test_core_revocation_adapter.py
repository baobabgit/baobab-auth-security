"""Tests unitaires de :class:`CoreRevocationAdapter`.

:spec: FEAT-011.1, ADR-0005
"""

from __future__ import annotations

from baobab_auth_core.domain.value_objects.token_id import TokenId

from baobab_auth_security.integration.core_revocation_adapter import (
    CoreRevocationAdapter,
)
from baobab_auth_security.revocation.in_memory_revocation_checker import (
    InMemoryRevocationChecker,
)


class TestCoreRevocationAdapter:
    """Vérifie la traduction ``TokenId`` ⇄ ``jti``."""

    def test_FEAT_011_1_revoke_then_is_revoked(self) -> None:
        adapter = CoreRevocationAdapter()
        token_id = TokenId("jti-1")
        assert adapter.is_revoked(token_id) is False
        adapter.revoke(token_id)
        assert adapter.is_revoked(token_id) is True

    def test_FEAT_011_1_uses_injected_checker(self) -> None:
        checker = InMemoryRevocationChecker()
        adapter = CoreRevocationAdapter(checker)
        adapter.revoke(TokenId("jti-2"))
        assert checker.is_revoked("jti-2") is True
