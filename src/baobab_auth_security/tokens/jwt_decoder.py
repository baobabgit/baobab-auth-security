"""Décodeur JWT — vérifie la signature et reconstruit les claims.

La validation des claims métier (``exp``/``iss``/``aud``) est déléguée à
:class:`JwtValidator` ; ce décodeur ne vérifie que la **signature** et la
structure, et refuse ``alg=none`` ou tout algorithme hors liste blanche.

:spec: FEAT-010.2, ADR-0003
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import jwt
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from baobab_auth_security.exceptions import (
    InvalidAlgorithmError,
    TokenSignatureError,
    TokenValidationError,
)
from baobab_auth_security.tokens.jwt_algorithm import JwtAlgorithm
from baobab_auth_security.tokens.security_token_claims import SecurityTokenClaims

PublicKeyResolver = Callable[[str], RSAPublicKey]
"""Résout une clé publique RSA à partir d'un ``kid``."""


class JwtDecoder:
    """Vérifie la signature d'un JWT et en extrait les claims.

    :param public_key_resolver: Fonction ``kid -> RSAPublicKey``.
    :param algorithms: Algorithmes autorisés ; défaut : tous les ``RS*``.
    """

    def __init__(
        self,
        public_key_resolver: PublicKeyResolver,
        algorithms: tuple[JwtAlgorithm, ...] = tuple(JwtAlgorithm),
    ) -> None:
        """Initialise le décodeur avec un résolveur et une liste blanche."""
        self._resolver = public_key_resolver
        self._algorithms = algorithms

    def decode(self, token: str) -> SecurityTokenClaims:
        """Vérifie la signature et reconstruit les claims.

        :param token: JWT compact à vérifier.
        :returns: Claims décodés.
        :raises InvalidAlgorithmError: Si ``alg=none`` ou hors liste blanche.
        :raises TokenSignatureError: Si la signature est invalide ou le ``kid``
            absent.
        :raises TokenValidationError: Si le token est malformé.
        """
        try:
            header = jwt.get_unverified_header(token)
        except jwt.PyJWTError as exc:
            raise TokenValidationError("En-tête JWT illisible.") from exc

        algorithm = JwtAlgorithm.from_name(str(header.get("alg")))
        if algorithm not in self._algorithms:
            raise InvalidAlgorithmError(
                f"Algorithme {algorithm.value} non autorisé pour ce décodeur."
            )

        kid = header.get("kid")
        if not kid:
            raise TokenSignatureError("Header JWT sans 'kid'.")

        public_key = self._resolver(str(kid))

        try:
            payload: dict[str, Any] = jwt.decode(
                token,
                public_key,
                algorithms=[alg.value for alg in self._algorithms],
                options={"verify_exp": False, "verify_aud": False},
            )
        except jwt.InvalidSignatureError as exc:
            raise TokenSignatureError("Signature JWT invalide.") from exc
        except jwt.PyJWTError as exc:
            raise TokenValidationError("JWT invalide.") from exc

        return self._to_claims(payload)

    @staticmethod
    def _to_claims(payload: dict[str, Any]) -> SecurityTokenClaims:
        """Convertit un payload décodé en :class:`SecurityTokenClaims`.

        :param payload: Dictionnaire de claims décodés.
        :returns: Claims structurés.
        :raises TokenValidationError: Si un claim obligatoire manque.
        """
        try:
            audience = payload.get("aud")
            return SecurityTokenClaims(
                sub=payload["sub"],
                jti=payload["jti"],
                issued_at=datetime.fromtimestamp(payload["iat"], tz=UTC),
                expires_at=datetime.fromtimestamp(payload["exp"], tz=UTC),
                sid=payload.get("sid"),
                roles=tuple(payload.get("roles", ())),
                permissions=tuple(payload.get("permissions", ())),
                issuer=payload.get("iss"),
                audience=tuple(audience) if isinstance(audience, list) else audience,
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise TokenValidationError("Claims JWT incomplets ou invalides.") from exc
