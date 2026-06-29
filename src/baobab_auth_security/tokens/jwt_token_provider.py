"""Service haut niveau d'émission et de vérification d'access tokens JWT.

:spec: FEAT-010.2, ADR-0003
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import timedelta

from baobab_auth_security.clock.clock import Clock
from baobab_auth_security.tokens.jwt_decoder import JwtDecoder
from baobab_auth_security.tokens.jwt_encoder import JwtEncoder
from baobab_auth_security.tokens.jwt_validator import JwtValidator
from baobab_auth_security.tokens.security_token_claims import SecurityTokenClaims


class JwtTokenProvider:
    """Orchestre l'émission et la vérification des access tokens.

    :param encoder: Encodeur (signe les claims).
    :param decoder: Décodeur (vérifie la signature).
    :param validator: Validateur (claims métier).
    :param clock: Horloge UTC injectée.
    :param issuer: Émetteur (``iss``) inscrit dans les tokens émis.
    :param audience: Audience (``aud``) inscrite dans les tokens émis.
    """

    def __init__(
        self,
        encoder: JwtEncoder,
        decoder: JwtDecoder,
        validator: JwtValidator,
        clock: Clock,
        issuer: str | None = None,
        audience: str | tuple[str, ...] | None = None,
    ) -> None:
        """Initialise le provider."""
        self._encoder = encoder
        self._decoder = decoder
        self._validator = validator
        self._clock = clock
        self._issuer = issuer
        self._audience = audience

    def issue_access_token(
        self,
        *,
        subject: str,
        token_id: str,
        ttl_seconds: int,
        session_id: str | None = None,
        roles: Iterable[str] = (),
        permissions: Iterable[str] = (),
    ) -> str:
        """Émet un access token signé pour le sujet donné.

        :param subject: Sujet (``sub``).
        :param token_id: Identifiant du token (``jti``).
        :param ttl_seconds: Durée de vie en secondes.
        :param session_id: Identifiant de session (``sid``) ou ``None``.
        :param roles: Rôles à inscrire dans les claims.
        :param permissions: Permissions à inscrire dans les claims.
        :returns: Access token JWT compact.
        """
        now = self._clock.now()
        claims = SecurityTokenClaims(
            sub=subject,
            jti=token_id,
            issued_at=now,
            expires_at=now + timedelta(seconds=ttl_seconds),
            sid=session_id,
            roles=tuple(roles),
            permissions=tuple(permissions),
            issuer=self._issuer,
            audience=self._audience,
        )
        return self._encoder.encode(claims)

    def verify_access_token(self, token: str) -> SecurityTokenClaims:
        """Vérifie la signature puis les claims d'un access token.

        :param token: JWT compact à vérifier.
        :returns: Claims validés.
        :raises InvalidAlgorithmError: Si ``alg=none`` ou hors liste blanche.
        :raises TokenSignatureError: Si la signature est invalide.
        :raises TokenExpiredError: Si le token est expiré.
        :raises TokenValidationError: Si un claim métier est incohérent.
        """
        claims = self._decoder.decode(token)
        self._validator.validate(claims)
        return claims
