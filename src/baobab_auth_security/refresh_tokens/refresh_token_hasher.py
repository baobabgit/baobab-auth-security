"""Hachage de refresh tokens opaques (SHA-256, comparaison temps constant).

:spec: FEAT-010.3, ADR-0004
"""

from __future__ import annotations

import hashlib
import hmac

from baobab_auth_security.exceptions import RefreshTokenError


class RefreshTokenHasher:
    """Hache un refresh token opaque et compare en temps constant.

    Le refresh token possède une entropie cryptographique complète : un hash
    SHA-256 (déterministe, sans sel) suffit pour le stockage côté consommateur et
    permet la recherche par hash.
    """

    def hash(self, token: str) -> str:
        """Retourne le hash hexadécimal SHA-256 du token.

        :param token: Refresh token opaque en clair, non vide.
        :returns: Hash hexadécimal (64 caractères).
        :raises RefreshTokenError: Si le token est vide.
        """
        if not token:
            raise RefreshTokenError("Refresh token vide.")
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def verify(self, token: str, token_hash: str) -> bool:
        """Vérifie qu'un token correspond à un hash, en temps constant.

        :param token: Refresh token en clair à vérifier.
        :param token_hash: Hash de référence.
        :returns: ``True`` si le token correspond au hash.
        :raises RefreshTokenError: Si le token est vide.
        """
        return hmac.compare_digest(self.hash(token), token_hash)
