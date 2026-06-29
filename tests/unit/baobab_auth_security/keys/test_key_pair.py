"""Tests de :class:`KeyPair`.

:spec: FEAT-010.4, ADR-0006
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from baobab_auth_security.exceptions import KeyManagementError
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm
from baobab_auth_security.keys.key_pair import KeyPair
from baobab_auth_security.keys.key_status import KeyStatus


class TestKeyPair:
    """Vérifie la validation et le masquage de la clé privée."""

    def test_FEAT_010_4_repr_masks_private_key(self, active_key: KeyPair) -> None:
        text = repr(active_key)
        assert "private_key='***'" in text
        assert "key-active" in text
        # Aucun matériel de clé privée ne doit transparaître.
        assert "BEGIN" not in text

    def test_FEAT_010_4_rejects_empty_kid(self, active_key: KeyPair) -> None:
        with pytest.raises(KeyManagementError):
            KeyPair(
                kid="",
                algorithm=KeyAlgorithm.RS256,
                private_key=active_key.private_key,
                public_key=active_key.public_key,
                status=KeyStatus.ACTIVE,
                created_at=active_key.created_at,
            )

    def test_FEAT_010_4_rejects_naive_created_at(self, active_key: KeyPair) -> None:
        with pytest.raises(KeyManagementError):
            KeyPair(
                kid="k",
                algorithm=KeyAlgorithm.RS256,
                private_key=active_key.private_key,
                public_key=active_key.public_key,
                status=KeyStatus.ACTIVE,
                created_at=datetime(2026, 1, 1),
            )

    def test_FEAT_010_4_created_at_is_utc(self, active_key: KeyPair) -> None:
        assert active_key.created_at.tzinfo == UTC
