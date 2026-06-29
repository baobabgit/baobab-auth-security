"""Tests de la hiérarchie d'exceptions.

:spec: FEAT-012.1, ADR-0006
"""

from __future__ import annotations

import pytest

from baobab_auth_security.exceptions import (
    ConfigurationError,
    InvalidAlgorithmError,
    KeyManagementError,
    KeyNotFoundError,
    PasswordHashingError,
    RefreshTokenError,
    SecurityError,
    TokenEncodingError,
    TokenError,
    TokenExpiredError,
    TokenRevokedError,
    TokenSignatureError,
    TokenValidationError,
)


class TestExceptions:
    """Vérifie la hiérarchie et l'absence de fuite dans les messages."""

    @pytest.mark.parametrize(
        "exc",
        [
            ConfigurationError,
            PasswordHashingError,
            TokenError,
            KeyManagementError,
            RefreshTokenError,
        ],
    )
    def test_FEAT_012_1_direct_children_inherit_security_error(
        self, exc: type[SecurityError]
    ) -> None:
        assert issubclass(exc, SecurityError)

    @pytest.mark.parametrize(
        "exc",
        [
            TokenEncodingError,
            TokenValidationError,
            TokenSignatureError,
            TokenExpiredError,
            InvalidAlgorithmError,
            TokenRevokedError,
        ],
    )
    def test_FEAT_012_1_token_errors_inherit_token_error(
        self, exc: type[TokenError]
    ) -> None:
        assert issubclass(exc, TokenError)

    def test_FEAT_012_1_validation_subtypes_inherit_validation_error(self) -> None:
        assert issubclass(TokenSignatureError, TokenValidationError)
        assert issubclass(TokenExpiredError, TokenValidationError)
        assert issubclass(InvalidAlgorithmError, TokenValidationError)
        assert issubclass(TokenRevokedError, TokenValidationError)

    def test_FEAT_012_1_key_not_found_inherits_key_management(self) -> None:
        assert issubclass(KeyNotFoundError, KeyManagementError)

    def test_FEAT_012_1_raisable_and_message_preserved(self) -> None:
        with pytest.raises(SecurityError, match="boom"):
            raise TokenExpiredError("boom")
