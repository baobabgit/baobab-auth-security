"""Tests de :class:`InMemoryKeyProvider`.

:spec: FEAT-010.4
"""

from __future__ import annotations

import dataclasses

import pytest

from baobab_auth_security.exceptions import KeyManagementError, KeyNotFoundError
from baobab_auth_security.keys.in_memory_key_provider import InMemoryKeyProvider
from baobab_auth_security.keys.key_pair import KeyPair
from baobab_auth_security.keys.key_status import KeyStatus


class TestInMemoryKeyProvider:
    """Vérifie la gestion des clés et la résolution par ``kid``."""

    def test_FEAT_010_4_first_active_key_becomes_signer(
        self, active_key: KeyPair
    ) -> None:
        provider = InMemoryKeyProvider((active_key,))
        assert provider.active().kid == active_key.kid

    def test_FEAT_010_4_resolves_public_key_by_kid(self, active_key: KeyPair) -> None:
        provider = InMemoryKeyProvider((active_key,))
        assert provider.public_key_for_kid(active_key.kid) is active_key.public_key

    def test_FEAT_010_4_unknown_kid_raises(self, active_key: KeyPair) -> None:
        provider = InMemoryKeyProvider((active_key,))
        with pytest.raises(KeyNotFoundError):
            provider.public_key_for_kid("absent")

    def test_FEAT_010_4_duplicate_kid_raises(self, active_key: KeyPair) -> None:
        provider = InMemoryKeyProvider((active_key,))
        with pytest.raises(KeyManagementError):
            provider.add(active_key)

    def test_FEAT_010_4_no_active_key_raises(self, active_key: KeyPair) -> None:
        pending = dataclasses.replace(active_key, status=KeyStatus.PENDING)
        provider = InMemoryKeyProvider((pending,))
        with pytest.raises(KeyManagementError):
            provider.active()

    def test_FEAT_010_4_set_active_switches_signer(
        self, active_key: KeyPair, second_key: KeyPair
    ) -> None:
        provider = InMemoryKeyProvider((active_key, second_key))
        provider.set_active(second_key.kid)
        assert provider.active().kid == second_key.kid

    def test_FEAT_010_4_set_active_unknown_raises(self, active_key: KeyPair) -> None:
        provider = InMemoryKeyProvider((active_key,))
        with pytest.raises(KeyNotFoundError):
            provider.set_active("absent")

    def test_FEAT_010_4_all_keys_returns_every_pair(
        self, active_key: KeyPair, second_key: KeyPair
    ) -> None:
        provider = InMemoryKeyProvider((active_key, second_key))
        assert {k.kid for k in provider.all_keys()} == {
            active_key.kid,
            second_key.kid,
        }
