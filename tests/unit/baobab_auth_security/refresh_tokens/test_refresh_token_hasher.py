"""Tests de :class:`RefreshTokenHasher`.

:spec: FEAT-010.3
"""

from __future__ import annotations

import pytest

from baobab_auth_security.exceptions import RefreshTokenError
from baobab_auth_security.refresh_tokens.refresh_token_hasher import RefreshTokenHasher


class TestRefreshTokenHasher:
    """Vérifie le hachage SHA-256 et la comparaison temps constant."""

    def test_FEAT_010_3_hash_is_deterministic_hex(self) -> None:
        hasher = RefreshTokenHasher()
        digest = hasher.hash("opaque-token")
        assert digest == hasher.hash("opaque-token")
        assert len(digest) == 64
        assert "opaque-token" not in digest

    def test_FEAT_010_3_verify_matches_and_rejects(self) -> None:
        hasher = RefreshTokenHasher()
        digest = hasher.hash("token-a")
        assert hasher.verify("token-a", digest) is True
        assert hasher.verify("token-b", digest) is False

    def test_FEAT_010_3_rejects_empty_token(self) -> None:
        hasher = RefreshTokenHasher()
        with pytest.raises(RefreshTokenError):
            hasher.hash("")
