"""``baobab-auth-security`` — brique de sécurité de l'écosystème ``baobab-auth``.

Fournit les implémentations cryptographiques que ``baobab-auth-core`` ne porte
pas : hachage Argon2id, JWT signés localement (RS256), refresh tokens opaques,
clés RSA et JWKS public, ainsi que des adaptateurs stricts vers les ports du core.

Le contenu de ``__all__`` constitue le **contrat public** versionné en SemVer.

:spec: FEAT-012.1
"""

from __future__ import annotations

from baobab_auth_security.clock import Clock, FixedClock, SystemClock
from baobab_auth_security.exceptions import (
    ConfigurationError,
    InvalidAlgorithmError,
    KeyManagementError,
    KeyNotFoundError,
    PasswordHashingError,
    RefreshTokenError,
    SecurityError,
    TokenEncodingError,
    TokenError,
    TokenExpiredError,
    TokenRevokedError,
    TokenSignatureError,
    TokenValidationError,
)
from baobab_auth_security.password import (
    Argon2PasswordHasher,
    PasswordHashPolicy,
    PasswordHashResult,
    PasswordVerificationResult,
)
from baobab_auth_security.version import __version__

__all__ = [
    "Argon2PasswordHasher",
    "Clock",
    "ConfigurationError",
    "FixedClock",
    "InvalidAlgorithmError",
    "KeyManagementError",
    "KeyNotFoundError",
    "PasswordHashPolicy",
    "PasswordHashResult",
    "PasswordHashingError",
    "PasswordVerificationResult",
    "RefreshTokenError",
    "SecurityError",
    "SystemClock",
    "TokenEncodingError",
    "TokenError",
    "TokenExpiredError",
    "TokenRevokedError",
    "TokenSignatureError",
    "TokenValidationError",
    "__version__",
]
