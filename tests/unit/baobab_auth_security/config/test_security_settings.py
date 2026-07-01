"""Tests de :class:`SecuritySettings`.

:spec: FEAT-012.2
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from baobab_auth_security.config.security_settings import SecuritySettings
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm
from baobab_auth_security.password.password_hash_policy import PasswordHashPolicy
from baobab_auth_security.tokens.jwt_algorithm import JwtAlgorithm


class TestSecuritySettings:
    """Vérifie le chargement et la dérivation de la configuration."""

    def test_FEAT_012_2_defaults(self) -> None:
        settings = SecuritySettings()
        assert settings.algorithm == "RS256"
        assert settings.access_ttl_seconds == 900
        assert settings.issuer is None

    def test_FEAT_012_2_loads_from_environment(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("BAOBAB_SECURITY_ISSUER", "baobab-auth")
        monkeypatch.setenv("BAOBAB_SECURITY_ACCESS_TTL_SECONDS", "120")
        settings = SecuritySettings()
        assert settings.issuer == "baobab-auth"
        assert settings.access_ttl_seconds == 120

    def test_FEAT_012_2_derives_password_policy(self) -> None:
        settings = SecuritySettings(argon2_time_cost=2, argon2_memory_cost=512)
        policy = settings.password_policy()
        assert isinstance(policy, PasswordHashPolicy)
        assert policy.time_cost == 2
        assert policy.memory_cost == 512

    def test_FEAT_012_2_resolves_algorithms(self) -> None:
        settings = SecuritySettings(algorithm="RS384")
        assert settings.jwt_algorithm() is JwtAlgorithm.RS384
        assert settings.key_algorithm() is KeyAlgorithm.RS384

    def test_FEAT_012_2_rejects_invalid_ttl(self) -> None:
        with pytest.raises(ValidationError):
            SecuritySettings(access_ttl_seconds=0)
