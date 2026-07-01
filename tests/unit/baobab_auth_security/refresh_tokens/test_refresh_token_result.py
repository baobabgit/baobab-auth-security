"""Tests de :class:`RefreshTokenResult`.

:spec: FEAT-010.3, ADR-0006
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from baobab_auth_security.exceptions import RefreshTokenError
from baobab_auth_security.refresh_tokens.refresh_token_result import RefreshTokenResult

_NOW = datetime(2026, 6, 29, 12, 0, tzinfo=UTC)


def _result(**overrides: object) -> RefreshTokenResult:
    kwargs: dict[str, object] = {
        "token": "clear-secret-token",
        "token_hash": "deadbeef",
        "token_id": "jti-1",
        "issued_at": _NOW,
        "expires_at": _NOW + timedelta(days=14),
    }
    kwargs.update(overrides)
    return RefreshTokenResult(**kwargs)  # type: ignore[arg-type]


class TestRefreshTokenResult:
    """Vérifie le masquage du clair et la validation des champs."""

    def test_FEAT_010_3_repr_and_str_mask_clear_token(self) -> None:
        result = _result()
        assert "clear-secret-token" not in repr(result)
        assert "clear-secret-token" not in str(result)
        assert str(result) == "***"
        assert "jti-1" in repr(result)

    def test_FEAT_010_3_values_remain_accessible(self) -> None:
        result = _result()
        assert result.token == "clear-secret-token"
        assert result.token_hash == "deadbeef"

    def test_FEAT_010_3_rejects_empty_fields(self) -> None:
        with pytest.raises(RefreshTokenError):
            _result(token="")

    def test_FEAT_010_3_rejects_naive_dates(self) -> None:
        with pytest.raises(RefreshTokenError):
            _result(issued_at=datetime(2026, 1, 1))
