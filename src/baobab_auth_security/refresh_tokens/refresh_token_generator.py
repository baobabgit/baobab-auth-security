"""Générateur de refresh tokens opaques.

:spec: FEAT-010.3, ADR-0004
"""

from __future__ import annotations

import secrets
from datetime import timedelta

from baobab_auth_security.clock.clock import Clock
from baobab_auth_security.exceptions import ConfigurationError
from baobab_auth_security.refresh_tokens.refresh_token_hasher import RefreshTokenHasher
from baobab_auth_security.refresh_tokens.refresh_token_result import RefreshTokenResult

_DEFAULT_TTL_SECONDS = 1_209_600  # 14 jours


class RefreshTokenGenerator:
    """Génère des refresh tokens opaques à forte entropie.

    :param clock: Horloge UTC injectée.
    :param hasher: Hasheur de tokens ; défaut :class:`RefreshTokenHasher`.
    :param token_nbytes: Entropie du token, en octets (>= 32).
    :param default_ttl_seconds: Durée de vie par défaut, en secondes.
    :raises ConfigurationError: Si ``token_nbytes`` < 32.
    """

    def __init__(
        self,
        clock: Clock,
        hasher: RefreshTokenHasher | None = None,
        *,
        token_nbytes: int = 32,
        default_ttl_seconds: int = _DEFAULT_TTL_SECONDS,
    ) -> None:
        """Initialise le générateur."""
        if token_nbytes < 32:
            raise ConfigurationError("token_nbytes doit être >= 32 octets.")
        self._clock = clock
        self._hasher = hasher or RefreshTokenHasher()
        self._token_nbytes = token_nbytes
        self._default_ttl = default_ttl_seconds

    def generate(
        self,
        *,
        token_id: str | None = None,
        ttl_seconds: int | None = None,
    ) -> RefreshTokenResult:
        """Génère un refresh token opaque, son hash et ses métadonnées.

        :param token_id: Identifiant (``jti``) ; généré si ``None``.
        :param ttl_seconds: Durée de vie ; défaut configuré si ``None``.
        :returns: Résultat avec token en clair (éphémère), hash et dates UTC.
        """
        token = secrets.token_urlsafe(self._token_nbytes)
        tid = token_id or secrets.token_urlsafe(16)
        ttl = self._default_ttl if ttl_seconds is None else ttl_seconds
        now = self._clock.now()
        return RefreshTokenResult(
            token=token,
            token_hash=self._hasher.hash(token),
            token_id=tid,
            issued_at=now,
            expires_at=now + timedelta(seconds=ttl),
        )
