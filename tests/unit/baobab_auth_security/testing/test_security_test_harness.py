"""Tests de :class:`SecurityTestHarness`.

:spec: FEAT-012.2
"""

from __future__ import annotations

from datetime import UTC, datetime

from baobab_auth_core.domain.value_objects.plain_password import PlainPassword

from baobab_auth_security.testing.security_test_harness import SecurityTestHarness


class TestSecurityTestHarness:
    """Vérifie l'assemblage déterministe de la pile de sécurité."""

    def test_FEAT_012_2_token_round_trip(self) -> None:
        harness = SecurityTestHarness()
        adapter = harness.token_provider_adapter
        token = adapter.create_access_token("user-1", 900, {"roles": ["ADMIN"]})
        payload = adapter.verify_access_token(token)
        assert payload["sub"] == "user-1"
        assert payload["roles"] == ["ADMIN"]

    def test_FEAT_012_2_jwks_is_published(self) -> None:
        harness = SecurityTestHarness(kid="harness-key")
        assert harness.jwks_provider.jwks().key_ids() == ("harness-key",)

    def test_FEAT_012_2_password_adapter_works(self) -> None:
        harness = SecurityTestHarness()
        digest = harness.password_hasher_adapter.hash(PlainPassword("pw"))
        assert harness.password_hasher_adapter.verify(PlainPassword("pw"), digest)

    def test_FEAT_012_2_clock_is_fixed(self) -> None:
        moment = datetime(2027, 3, 3, tzinfo=UTC)
        harness = SecurityTestHarness(moment)
        assert harness.clock.now() == moment

    def test_FEAT_012_2_exposes_jwt_token_provider(self) -> None:
        harness = SecurityTestHarness()
        provider = harness.jwt_token_provider
        token = provider.issue_access_token(subject="u", token_id="j", ttl_seconds=60)
        assert provider.verify_access_token(token).sub == "u"
