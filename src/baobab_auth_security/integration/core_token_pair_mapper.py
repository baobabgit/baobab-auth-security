"""Mapping d'une paire de tokens de sécurité vers le ``TokenPair`` du core.

:spec: FEAT-011.1, ADR-0005
"""

from __future__ import annotations

from baobab_auth_core.application.results.token_pair import TokenPair

from baobab_auth_security.tokens.security_token_pair import SecurityTokenPair


class CoreTokenPairMapper:
    """Convertit une :class:`SecurityTokenPair` en ``TokenPair`` du core."""

    def to_core(self, pair: SecurityTokenPair) -> TokenPair:
        """Mappe la paire de tokens vers le DTO du core.

        :param pair: Paire de tokens de sécurité.
        :returns: ``TokenPair`` du core équivalent.
        """
        return TokenPair(
            access_token=pair.access_token,
            refresh_token=pair.refresh_token,
            token_type=pair.token_type,
            expires_in=pair.expires_in,
            refresh_expires_in=pair.refresh_expires_in,
        )
