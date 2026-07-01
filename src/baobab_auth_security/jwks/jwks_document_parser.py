"""Parsing d'un document JWKS JSON.

:spec: FEAT-020.2
"""

from __future__ import annotations

from typing import Any

from baobab_auth_security.exceptions import JwksFetchError
from baobab_auth_security.jwks.jwk_public_key_loader import JwkPublicKeyLoader
from baobab_auth_security.jwks.jwks import JWKS
from baobab_auth_security.jwks.public_jwk import PublicJwk
from baobab_auth_security.tokens.signing_key_types import SigningPublicKey


class JwksDocumentParser:
    """Parse un document ``{"keys": [...]}`` en JWKS et résolveur de clés."""

    def __init__(self, loader: JwkPublicKeyLoader | None = None) -> None:
        """Initialise le parseur."""
        self._loader = loader or JwkPublicKeyLoader()

    def parse(
        self, document: dict[str, Any]
    ) -> tuple[JWKS, dict[str, SigningPublicKey]]:
        """Parse un document JWKS.

        :param document: Corps JSON du endpoint JWKS.
        :returns: JWKS typé et map ``kid -> clé publique``.
        :raises JwksFetchError: Si le document est malformé.
        """
        keys_raw = document.get("keys")
        if not isinstance(keys_raw, list):
            raise JwksFetchError("Document JWKS invalide : clé 'keys' absente.")

        public_jwks: list[PublicJwk] = []
        resolver: dict[str, SigningPublicKey] = {}
        for entry in keys_raw:
            if not isinstance(entry, dict):
                raise JwksFetchError("Entrée JWK invalide dans le document.")
            jwk, public_key = self._loader.load(entry)
            if jwk.kid in resolver:
                raise JwksFetchError(f"kid dupliqué dans le JWKS : {jwk.kid!r}.")
            public_jwks.append(jwk)
            resolver[jwk.kid] = public_key

        return JWKS(keys=tuple(public_jwks)), resolver
