"""Banc de test déterministe assemblant la pile de sécurité.

Destiné aux **consommateurs** (API, client) qui veulent tester sans réassembler
toute la chaîne : horloge fixe, clé RSA en mémoire, provider JWT et adaptateurs
core prêts à l'emploi.

:spec: FEAT-012.2
"""

from __future__ import annotations

from datetime import UTC, datetime

from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.integration.core_password_hasher_adapter import (
    CorePasswordHasherAdapter,
)
from baobab_auth_security.integration.core_token_provider_adapter import (
    CoreTokenProviderAdapter,
)
from baobab_auth_security.jwks.jwks_provider import LocalJwksProvider
from baobab_auth_security.keys.in_memory_key_provider import InMemoryKeyProvider
from baobab_auth_security.keys.key_generator import KeyGenerator
from baobab_auth_security.password.argon2_password_hasher import Argon2PasswordHasher
from baobab_auth_security.password.password_hash_policy import PasswordHashPolicy
from baobab_auth_security.tokens.jwt_decoder import JwtDecoder
from baobab_auth_security.tokens.jwt_encoder import JwtEncoder
from baobab_auth_security.tokens.jwt_token_provider import JwtTokenProvider
from baobab_auth_security.tokens.jwt_validator import JwtValidator

_DEFAULT_MOMENT = datetime(2026, 1, 1, tzinfo=UTC)
# Politique Argon2 volontairement faible : tests rapides et déterministes.
_FAST_POLICY = PasswordHashPolicy(time_cost=1, memory_cost=8, parallelism=1)


class SecurityTestHarness:
    """Assemble une pile de sécurité déterministe pour les tests.

    :param moment: Instant fixe de l'horloge ; défaut ``2026-01-01T00:00:00Z``.
    :param issuer: Émetteur (``iss``) appliqué aux tokens.
    :param audience: Audience (``aud``) appliquée aux tokens.
    :param kid: Identifiant de la clé de signature.
    """

    def __init__(
        self,
        moment: datetime | None = None,
        *,
        issuer: str = "baobab-auth",
        audience: str = "api",
        kid: str = "test-key",
    ) -> None:
        """Construit la pile complète à un instant donné."""
        self._clock = FixedClock(moment or _DEFAULT_MOMENT)
        key_pair = KeyGenerator(self._clock).generate(kid=kid)
        self._key_provider = InMemoryKeyProvider((key_pair,))
        self._jwks_provider = LocalJwksProvider(self._key_provider)
        self._jwt_provider = JwtTokenProvider(
            JwtEncoder(key_pair.private_key, key_pair.kid),
            JwtDecoder(self._key_provider.public_key_for_kid),
            JwtValidator(self._clock, issuer=issuer, audience=audience),
            self._clock,
            issuer=issuer,
            audience=audience,
        )
        self._password_adapter = CorePasswordHasherAdapter(
            Argon2PasswordHasher(_FAST_POLICY)
        )
        self._token_adapter = CoreTokenProviderAdapter(self._jwt_provider)

    @property
    def clock(self) -> FixedClock:
        """Horloge fixe partagée.

        :returns: L'horloge déterministe.
        """
        return self._clock

    @property
    def key_provider(self) -> InMemoryKeyProvider:
        """Fournisseur de clés en mémoire.

        :returns: Le fournisseur de clés.
        """
        return self._key_provider

    @property
    def jwks_provider(self) -> LocalJwksProvider:
        """Fournisseur de JWKS public.

        :returns: Le fournisseur de JWKS.
        """
        return self._jwks_provider

    @property
    def jwt_token_provider(self) -> JwtTokenProvider:
        """Provider JWT (émission/vérification).

        :returns: Le provider JWT.
        """
        return self._jwt_provider

    @property
    def password_hasher_adapter(self) -> CorePasswordHasherAdapter:
        """Adaptateur de hachage compatible core.

        :returns: L'adaptateur de mot de passe.
        """
        return self._password_adapter

    @property
    def token_provider_adapter(self) -> CoreTokenProviderAdapter:
        """Adaptateur de provider de tokens compatible core.

        :returns: L'adaptateur de tokens.
        """
        return self._token_adapter
