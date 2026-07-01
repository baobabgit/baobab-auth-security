"""Hiérarchie d'exceptions de ``baobab-auth-security``.

Toutes les exceptions du package dérivent de :class:`SecurityError`. Aucun message
d'exception ne doit contenir la valeur d'un secret (mot de passe, token brut, clé
privée).

:spec: FEAT-012.1, ADR-0006
"""

from __future__ import annotations


class SecurityError(Exception):
    """Racine de toutes les erreurs de ``baobab-auth-security``."""


class ConfigurationError(SecurityError):
    """Configuration invalide ou incohérente (paramètres, algorithmes, clés)."""


class PasswordHashingError(SecurityError):
    """Échec technique du hachage ou de la vérification d'un mot de passe."""


class TokenError(SecurityError):
    """Erreur générique liée à un token (JWT ou refresh)."""


class TokenEncodingError(TokenError):
    """Échec de l'encodage/signature d'un token."""


class TokenValidationError(TokenError):
    """Token invalide à la vérification (signature, claims, format)."""


class TokenSignatureError(TokenValidationError):
    """Signature de token invalide ou clé inconnue."""


class TokenExpiredError(TokenValidationError):
    """Token expiré (``exp`` dépassé)."""


class InvalidAlgorithmError(TokenValidationError):
    """Algorithme non autorisé (``alg=none`` ou hors liste blanche)."""


class TokenRevokedError(TokenValidationError):
    """Token révoqué (``jti`` présent dans la liste de révocation)."""


class KeyManagementError(SecurityError):
    """Erreur de gestion des clés (génération, chargement, résolution)."""


class KeyNotFoundError(KeyManagementError):
    """Aucune clé ne correspond au ``kid`` demandé."""


class JwksFetchError(KeyManagementError):
    """Échec de récupération ou de parsing d'un JWKS distant."""


class RefreshTokenError(SecurityError):
    """Erreur liée à un refresh token opaque."""


__all__ = [
    "ConfigurationError",
    "InvalidAlgorithmError",
    "JwksFetchError",
    "KeyManagementError",
    "KeyNotFoundError",
    "PasswordHashingError",
    "RefreshTokenError",
    "SecurityError",
    "TokenEncodingError",
    "TokenError",
    "TokenExpiredError",
    "TokenRevokedError",
    "TokenSignatureError",
    "TokenValidationError",
]
