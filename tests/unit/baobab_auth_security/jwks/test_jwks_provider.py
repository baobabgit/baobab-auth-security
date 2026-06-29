"""Tests de :class:`LocalJwksProvider`.

:spec: FEAT-010.4, ADR-0006
"""

from __future__ import annotations

import dataclasses

from baobab_auth_security.jwks.jwks_provider import LocalJwksProvider
from baobab_auth_security.keys.in_memory_key_provider import InMemoryKeyProvider
from baobab_auth_security.keys.key_pair import KeyPair
from baobab_auth_security.keys.key_status import KeyStatus


class TestLocalJwksProvider:
    """Vérifie la construction du JWKS public (sans clé privée)."""

    def test_FEAT_010_4_publishes_active_key(self, rsa_key: KeyPair) -> None:
        provider = LocalJwksProvider(InMemoryKeyProvider((rsa_key,)))
        jwks = provider.jwks()
        assert jwks.key_ids() == (rsa_key.kid,)

    def test_FEAT_010_4_jwks_dict_has_no_private_material(
        self, rsa_key: KeyPair
    ) -> None:
        provider = LocalJwksProvider(InMemoryKeyProvider((rsa_key,)))
        data = provider.jwks().to_dict()
        for entry in data["keys"]:
            assert {"d", "p", "q", "dp", "dq", "qi"}.isdisjoint(entry)
            assert set(entry) == {"kty", "use", "alg", "kid", "n", "e"}

    def test_FEAT_010_4_omits_pending_keys(self, rsa_key: KeyPair) -> None:
        pending = dataclasses.replace(
            rsa_key, kid="pending-1", status=KeyStatus.PENDING
        )
        retired = dataclasses.replace(
            rsa_key, kid="retired-1", status=KeyStatus.RETIRED
        )
        provider = LocalJwksProvider(InMemoryKeyProvider((rsa_key, pending, retired)))
        published = set(provider.jwks().key_ids())
        assert rsa_key.kid in published
        assert "retired-1" in published
        assert "pending-1" not in published
