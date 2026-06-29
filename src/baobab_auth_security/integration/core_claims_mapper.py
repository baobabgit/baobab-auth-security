"""Mapping des claims de sécurité vers le VO ``TokenClaims`` du core.

:spec: FEAT-011.1, ADR-0005
"""

from __future__ import annotations

from baobab_auth_core.application.results.token_claims import TokenClaims
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId

from baobab_auth_security.tokens.security_token_claims import SecurityTokenClaims


class CoreClaimsMapper:
    """Convertit des :class:`SecurityTokenClaims` en ``TokenClaims`` du core.

    Les rôles et permissions sont **transportés tels quels** (aucun recalcul du
    mapping rôle → permissions).
    """

    def to_core(self, claims: SecurityTokenClaims) -> TokenClaims:
        """Mappe des claims de sécurité vers le VO du core.

        :param claims: Claims de sécurité (déjà vérifiés).
        :returns: ``TokenClaims`` du core équivalent.
        """
        return TokenClaims(
            subject=AuthSubject(claims.sub),
            session_id=SessionId(claims.sid) if claims.sid else None,
            token_id=TokenId(claims.jti),
            roles=tuple(RoleName(role) for role in claims.roles),
            permissions=tuple(
                PermissionName(permission) for permission in claims.permissions
            ),
            issued_at=claims.issued_at,
            expires_at=claims.expires_at,
            issuer=claims.issuer,
            audience=claims.audience,
        )
