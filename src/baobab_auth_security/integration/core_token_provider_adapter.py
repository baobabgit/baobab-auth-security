"""Adaptateur du provider JWT vers le port ``TokenProvider`` du core.

:spec: FEAT-011.1, ADR-0005
"""

from __future__ import annotations

import secrets
from collections.abc import Callable
from typing import Any

from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.exceptions.auth import (
    TokenExpiredError as CoreTokenExpiredError,
)
from baobab_auth_core.exceptions.auth import (
    TokenInvalidError as CoreTokenInvalidError,
)

from baobab_auth_security.exceptions import SecurityError
from baobab_auth_security.exceptions import TokenExpiredError as SecTokenExpiredError
from baobab_auth_security.integration.core_revocation_adapter import (
    CoreRevocationAdapter,
)
from baobab_auth_security.tokens.jwt_token_provider import JwtTokenProvider
from baobab_auth_security.tokens.security_token_claims import SecurityTokenClaims

_DEFAULT_ID_NBYTES = 16


class CoreTokenProviderAdapter:
    """Expose :class:`JwtTokenProvider` derrière le port réel ``TokenProvider``.

    Satisfait ``baobab_auth_core.ports.token_provider.TokenProvider`` (synchrone,
    six méthodes). Les access **et** refresh tokens sont des JWT signés
    (auto-portants, vérifiables via JWKS), conformément au modèle du port. Les
    refresh tokens *opaques* (:mod:`baobab_auth_security.refresh_tokens`) restent
    disponibles pour les flux gérés par l'API/database.

    :param jwt_provider: Provider JWT sous-jacent.
    :param access_ttl_seconds: TTL par défaut des access tokens.
    :param refresh_ttl_seconds: TTL par défaut des refresh tokens.
    :param revocation: Adaptateur de révocation ; défaut
        :class:`CoreRevocationAdapter`.
    :param token_id_factory: Fabrique de ``jti`` ; défaut ``secrets``.
    """

    def __init__(
        self,
        jwt_provider: JwtTokenProvider,
        *,
        access_ttl_seconds: int = 900,
        refresh_ttl_seconds: int = 1_209_600,
        revocation: CoreRevocationAdapter | None = None,
        token_id_factory: Callable[[], str] | None = None,
    ) -> None:
        """Initialise l'adaptateur."""
        self._jwt = jwt_provider
        self._access_ttl = access_ttl_seconds
        self._refresh_ttl = refresh_ttl_seconds
        self._revocation = revocation or CoreRevocationAdapter()
        self._new_id = token_id_factory or self._default_id

    @staticmethod
    def _default_id() -> str:
        """Génère un ``jti`` aléatoire.

        :returns: Identifiant URL-safe.
        """
        return secrets.token_urlsafe(_DEFAULT_ID_NBYTES)

    def generate_token_id(self) -> TokenId:
        """Génère un identifiant de token unique.

        :returns: ``TokenId`` du core.
        """
        return TokenId(self._new_id())

    def create_access_token(
        self,
        subject: str,
        ttl_seconds: int,
        claims: dict[str, Any] | None = None,
    ) -> str:
        """Crée un access token JWT signé.

        :param subject: Sujet (``sub``).
        :param ttl_seconds: Durée de vie en secondes.
        :param claims: Claims additionnels (``sid``, ``roles``, ``permissions``).
        :returns: JWT compact.
        """
        extra = claims or {}
        return self._jwt.issue_access_token(
            subject=subject,
            token_id=self._new_id(),
            ttl_seconds=ttl_seconds,
            session_id=extra.get("sid"),
            roles=extra.get("roles", ()),
            permissions=extra.get("permissions", ()),
        )

    def verify_access_token(self, token: str) -> dict[str, Any]:
        """Vérifie un access token et retourne son payload décodé.

        :param token: JWT à vérifier.
        :returns: Payload décodé (``sub``, ``jti``, ``sid``, ``roles``, ...).
        :raises baobab_auth_core.exceptions.auth.TokenExpiredError: Si expiré.
        :raises baobab_auth_core.exceptions.auth.TokenInvalidError: Si invalide
            ou révoqué.
        """
        return self._to_payload(self._verify(token))

    def create_refresh_token(
        self,
        subject: str,
        token_id: TokenId,
        ttl_seconds: int,
        claims: dict[str, Any] | None = None,
    ) -> str:
        """Crée un refresh token JWT portant ``token_id`` (``jti``).

        :param subject: Sujet (``sub``).
        :param token_id: Identifiant du refresh token (``refresh_token_id``).
        :param ttl_seconds: Durée de vie en secondes.
        :param claims: Claims additionnels (``sid``).
        :returns: JWT compact.
        """
        extra = claims or {}
        return self._jwt.issue_access_token(
            subject=subject,
            token_id=token_id.value,
            ttl_seconds=ttl_seconds,
            session_id=extra.get("sid"),
        )

    def verify_refresh_token(self, token: str) -> dict[str, Any]:
        """Vérifie un refresh token et retourne son payload.

        :param token: JWT de rafraîchissement à vérifier.
        :returns: Payload décodé, enrichi de ``refresh_token_id``.
        :raises baobab_auth_core.exceptions.auth.TokenExpiredError: Si expiré.
        :raises baobab_auth_core.exceptions.auth.TokenInvalidError: Si invalide
            ou révoqué.
        """
        claims = self._verify(token)
        payload = self._to_payload(claims)
        payload["refresh_token_id"] = claims.jti
        return payload

    def revoke_token(self, token: str) -> None:
        """Révoque un token (best-effort) par son ``jti``.

        :param token: Token à révoquer ; ignoré silencieusement s'il est
            invalide ou déjà expiré.
        """
        try:
            claims = self._jwt.verify_access_token(token)
        except SecurityError:
            return
        self._revocation.revoke(TokenId(claims.jti))

    def _verify(self, token: str) -> SecurityTokenClaims:
        """Vérifie signature + claims et refuse les ``jti`` révoqués.

        :param token: JWT à vérifier.
        :returns: Claims de sécurité validés.
        :raises CoreTokenExpiredError: Si expiré.
        :raises CoreTokenInvalidError: Si invalide ou révoqué.
        """
        try:
            claims = self._jwt.verify_access_token(token)
        except SecTokenExpiredError as exc:
            raise CoreTokenExpiredError() from exc
        except SecurityError as exc:
            raise CoreTokenInvalidError() from exc
        if self._revocation.is_revoked(TokenId(claims.jti)):
            raise CoreTokenInvalidError()
        return claims

    @staticmethod
    def _to_payload(claims: SecurityTokenClaims) -> dict[str, Any]:
        """Sérialise des claims de sécurité en payload dict.

        :param claims: Claims de sécurité.
        :returns: Dictionnaire de claims (timestamps entiers).
        """
        return {
            "sub": claims.sub,
            "jti": claims.jti,
            "sid": claims.sid,
            "roles": list(claims.roles),
            "permissions": list(claims.permissions),
            "iat": int(claims.issued_at.timestamp()),
            "exp": int(claims.expires_at.timestamp()),
            "iss": claims.issuer,
            "aud": claims.audience,
        }
