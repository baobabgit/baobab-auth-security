"""Tests de non-fuite des secrets (règles transverses de sécurité).

Vérifie qu'aucun mot de passe brut, refresh token brut, access token complet ou
clé privée n'apparaît dans une représentation, un log ou une exception.

:spec: FEAT-012.2, ADR-0006
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from baobab_auth_security.exceptions import PasswordHashingError
from baobab_auth_security.password.argon2_password_hasher import Argon2PasswordHasher
from baobab_auth_security.password.password_hash_policy import PasswordHashPolicy
from baobab_auth_security.refresh_tokens.refresh_token_generator import (
    RefreshTokenGenerator,
)
from baobab_auth_security.testing.security_test_harness import SecurityTestHarness
from baobab_auth_security.tokens.security_token_pair import SecurityTokenPair

_FAST = PasswordHashPolicy(time_cost=1, memory_cost=8, parallelism=1)
_NOW = datetime(2026, 6, 29, 12, 0, tzinfo=UTC)
_SECRET_PASSWORD = "Sup3r-S3cret-Passw0rd!"


class TestNoSecretLeakage:
    """Garanties mécaniques d'absence de fuite de secrets."""

    def test_FEAT_012_2_password_hash_result_masks_secret(self) -> None:
        result = Argon2PasswordHasher(_FAST).hash(_SECRET_PASSWORD)
        assert _SECRET_PASSWORD not in repr(result)
        assert _SECRET_PASSWORD not in str(result)
        assert _SECRET_PASSWORD not in result.value  # hash non réversible

    def test_FEAT_012_2_password_verify_failure_does_not_leak(self) -> None:
        hasher = Argon2PasswordHasher(_FAST)
        with pytest.raises(PasswordHashingError) as excinfo:
            hasher.verify(_SECRET_PASSWORD, "malformed-hash")
        assert _SECRET_PASSWORD not in str(excinfo.value)

    def test_FEAT_012_2_refresh_token_clear_value_is_masked(self) -> None:
        result = RefreshTokenGenerator(SecurityTestHarness(_NOW).clock).generate()
        clear = result.token
        assert clear not in repr(result)
        assert clear not in str(result)
        assert result.token_hash not in repr(result)

    def test_FEAT_012_2_token_pair_masks_access_and_refresh(self) -> None:
        pair = SecurityTokenPair(
            access_token="header.payload.signature",
            refresh_token="opaque-refresh-secret",
            expires_in=900,
            refresh_expires_in=86400,
        )
        text = repr(pair)
        assert "header.payload.signature" not in text
        assert "opaque-refresh-secret" not in text

    def test_FEAT_012_2_key_pair_repr_hides_private_key(self) -> None:
        harness = SecurityTestHarness(_NOW)
        key_pair = harness.key_provider.active()
        text = repr(key_pair)
        assert "private_key='***'" in text
        assert "BEGIN" not in text
        # Le module privé RSA ne doit pas transparaître.
        private_numbers = key_pair.private_key.private_numbers()
        assert str(private_numbers.d) not in text

    def test_FEAT_012_2_jwks_contains_no_private_components(self) -> None:
        harness = SecurityTestHarness(_NOW)
        for entry in harness.jwks_provider.jwks().to_dict()["keys"]:
            assert {"d", "p", "q", "dp", "dq", "qi"}.isdisjoint(entry)

    def test_FEAT_012_2_issued_access_token_claims_are_utc(self) -> None:
        harness = SecurityTestHarness(_NOW)
        token = harness.token_provider_adapter.create_access_token("u", 900)
        payload = harness.token_provider_adapter.verify_access_token(token)
        # Timestamps entiers cohérents avec une émission UTC.
        assert payload["exp"] - payload["iat"] == 900
        assert payload["iat"] == int(_NOW.timestamp())
        # Marge : l'horloge fixe garantit le déterminisme.
        assert _NOW + timedelta(seconds=900) == datetime.fromtimestamp(
            payload["exp"], tz=UTC
        )
