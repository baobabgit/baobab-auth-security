"""Claims structurés d'un token de sécurité.

:spec: FEAT-010.2
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from baobab_auth_security.exceptions import ConfigurationError


@dataclass(frozen=True)
class SecurityTokenClaims:
    """Claims portés par un access token (avant encodage / après décodage).

    Les dates doivent être **timezone-aware (UTC)**.

    :param sub: Sujet (``sub``).
    :param jti: Identifiant unique du token (``jti``).
    :param issued_at: Date d'émission (``iat``), UTC aware.
    :param expires_at: Date d'expiration (``exp``), UTC aware.
    :param sid: Identifiant de session (``sid``) ou ``None``.
    :param roles: Rôles du sujet.
    :param permissions: Permissions agrégées.
    :param issuer: Émetteur (``iss``) ou ``None``.
    :param audience: Audience(s) (``aud``) ou ``None``.
    :raises ConfigurationError: Si une date est naïve (sans tzinfo).
    """

    sub: str
    jti: str
    issued_at: datetime
    expires_at: datetime
    sid: str | None = None
    roles: tuple[str, ...] = field(default_factory=tuple)
    permissions: tuple[str, ...] = field(default_factory=tuple)
    issuer: str | None = None
    audience: str | tuple[str, ...] | None = None

    def __post_init__(self) -> None:
        """Valide que les dates sont timezone-aware.

        :raises ConfigurationError: Si ``issued_at`` ou ``expires_at`` est naïf.
        """
        if self.issued_at.tzinfo is None or self.expires_at.tzinfo is None:
            raise ConfigurationError(
                "Les claims exigent des datetimes timezone-aware (UTC)."
            )
