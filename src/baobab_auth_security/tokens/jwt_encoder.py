"""Encodeur JWT — signe des claims avec une clé privée RSA.

:spec: FEAT-010.2, ADR-0003
"""

from __future__ import annotations

from typing import Any, cast

import jwt

from baobab_auth_security.exceptions import TokenEncodingError
from baobab_auth_security.tokens.jwt_algorithm import JwtAlgorithm
from baobab_auth_security.tokens.security_token_claims import SecurityTokenClaims
from baobab_auth_security.tokens.signing_key_types import SigningPrivateKey


class JwtEncoder:
    """Signe des :class:`SecurityTokenClaims` en JWT compact.

    Le header porte ``kid`` et ``alg``. L'algorithme est restreint à la liste
    blanche :class:`JwtAlgorithm` (RS256 par défaut).

    :param private_key: Clé privée de signature (RSA, EC ou OKP).
    :param kid: Identifiant de clé publié dans le header (``kid``).
    :param algorithm: Algorithme de signature ; défaut ``RS256``.
    """

    def __init__(
        self,
        private_key: SigningPrivateKey,
        kid: str,
        algorithm: JwtAlgorithm = JwtAlgorithm.RS256,
    ) -> None:
        """Initialise l'encodeur avec une clé et un algorithme autorisés."""
        self._private_key = private_key
        self._kid = kid
        self._algorithm = algorithm

    @property
    def kid(self) -> str:
        """Identifiant de la clé de signature.

        :returns: Le ``kid`` publié dans le header.
        """
        return self._kid

    def encode(self, claims: SecurityTokenClaims) -> str:
        """Sérialise et signe les claims en JWT.

        :param claims: Claims à encoder.
        :returns: JWT compact signé.
        :raises TokenEncodingError: Si l'encodage échoue.
        """
        payload: dict[str, Any] = {
            "sub": claims.sub,
            "jti": claims.jti,
            "iat": claims.issued_at,
            "exp": claims.expires_at,
            "roles": list(claims.roles),
            "permissions": list(claims.permissions),
        }
        if claims.sid is not None:
            payload["sid"] = claims.sid
        if claims.issuer is not None:
            payload["iss"] = claims.issuer
        if claims.audience is not None:
            payload["aud"] = (
                list(claims.audience)
                if isinstance(claims.audience, tuple)
                else claims.audience
            )
        try:
            return jwt.encode(
                payload,
                cast(Any, self._private_key),
                algorithm=self._algorithm.value,
                headers={"kid": self._kid},
            )
        except (TypeError, ValueError) as exc:  # pragma: no cover - garde-fou
            raise TokenEncodingError("Échec de l'encodage du JWT.") from exc
