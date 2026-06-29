"""Validateur de claims JWT (expiration, émetteur, audience, algorithme).

:spec: FEAT-010.2, ADR-0003
"""

from __future__ import annotations

from datetime import timedelta

from baobab_auth_security.clock.clock import Clock
from baobab_auth_security.exceptions import (
    InvalidAlgorithmError,
    TokenExpiredError,
    TokenValidationError,
)
from baobab_auth_security.tokens.jwt_algorithm import JwtAlgorithm
from baobab_auth_security.tokens.security_token_claims import SecurityTokenClaims


class JwtValidator:
    """Valide les claims métier d'un token déjà vérifié en signature.

    :param clock: Horloge UTC injectée (déterministe en test).
    :param issuer: Émetteur attendu (``iss``) ou ``None`` (non vérifié).
    :param audience: Audience attendue (``aud``) ou ``None`` (non vérifié).
    :param allowed_algorithms: Algorithmes autorisés ; défaut : tous les ``RS*``.
    :param leeway_seconds: Tolérance d'horloge pour l'expiration.
    """

    def __init__(
        self,
        clock: Clock,
        issuer: str | None = None,
        audience: str | tuple[str, ...] | None = None,
        allowed_algorithms: tuple[JwtAlgorithm, ...] = tuple(JwtAlgorithm),
        leeway_seconds: int = 0,
    ) -> None:
        """Initialise le validateur."""
        self._clock = clock
        self._issuer = issuer
        self._audience = audience
        self._allowed = allowed_algorithms
        self._leeway = timedelta(seconds=leeway_seconds)

    def validate_algorithm(self, name: str) -> JwtAlgorithm:
        """Vérifie qu'un algorithme est autorisé (refuse ``none``/inconnu).

        :param name: Nom d'algorithme du header.
        :returns: L'algorithme résolu.
        :raises InvalidAlgorithmError: Si refusé ou hors liste blanche.
        """
        algorithm = JwtAlgorithm.from_name(name)
        if algorithm not in self._allowed:
            raise InvalidAlgorithmError(f"Algorithme {name!r} hors liste blanche.")
        return algorithm

    def validate(self, claims: SecurityTokenClaims) -> None:
        """Valide expiration, émetteur et audience.

        :param claims: Claims à valider.
        :raises TokenExpiredError: Si le token est expiré.
        :raises TokenValidationError: Si ``iss`` ou ``aud`` ne correspond pas.
        """
        now = self._clock.now()
        if claims.expires_at <= now - self._leeway:
            raise TokenExpiredError("Token expiré.")

        if self._issuer is not None and claims.issuer != self._issuer:
            raise TokenValidationError("Émetteur (iss) inattendu.")

        if self._audience is not None and not self._audience_matches(claims.audience):
            raise TokenValidationError("Audience (aud) inattendue.")

    def _audience_matches(self, actual: str | tuple[str, ...] | None) -> bool:
        """Indique si l'audience du token recoupe l'audience attendue.

        :param actual: Audience portée par le token.
        :returns: ``True`` si au moins une audience attendue est présente.
        """
        if actual is None:
            return False
        expected = (
            {self._audience}
            if isinstance(self._audience, str)
            else set(self._audience or ())
        )
        present = {actual} if isinstance(actual, str) else set(actual)
        return bool(expected & present)
