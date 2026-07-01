"""``baobab-auth-security`` — brique de sécurité de l'écosystème ``baobab-auth``.

Fournit les implémentations cryptographiques que ``baobab-auth-core`` ne porte
pas : hachage Argon2id, JWT signés localement (RS256), refresh tokens opaques,
clés RSA et JWKS public, ainsi que des adaptateurs stricts vers les ports du core.

Le contenu de ``__all__`` constitue le **contrat public** versionné en SemVer.

:spec: FEAT-012.1
"""

from __future__ import annotations

from baobab_auth_security.clock import Clock, FixedClock, SystemClock
from baobab_auth_security.config import SecuritySettings
from baobab_auth_security.exceptions import (
    ConfigurationError,
    InvalidAlgorithmError,
    JwksFetchError,
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
from baobab_auth_security.integration import (
    CoreClaimsMapper,
    CorePasswordHasherAdapter,
    CoreRevocationAdapter,
    CoreTokenPairMapper,
    CoreTokenProviderAdapter,
)
from baobab_auth_security.jwks import (
    JWK,
    JWKS,
    EcJwk,
    EcPublicJwkConverter,
    JwkPublicKeyLoader,
    JwksDocumentParser,
    LocalJwksProvider,
    OkpJwk,
    OkpPublicJwkConverter,
    PublicJwk,
    PublicJwkConverter,
    RemoteJwksFetcher,
    RsaPublicJwkConverter,
)
from baobab_auth_security.keys import (
    EcKeyGenerator,
    Ed25519KeyGenerator,
    InMemoryKeyProvider,
    KeyAlgorithm,
    KeyGenerator,
    KeyIdDeriver,
    KeyPair,
    KeyStatus,
    PemKeyLoader,
)
from baobab_auth_security.password import (
    Argon2PasswordHasher,
    PasswordHashPolicy,
    PasswordHashResult,
    PasswordVerificationResult,
)
from baobab_auth_security.refresh_tokens import (
    RefreshTokenGenerator,
    RefreshTokenHasher,
    RefreshTokenResult,
)
from baobab_auth_security.revocation import (
    InMemoryRevocationChecker,
    RevocationChecker,
)
from baobab_auth_security.testing import SecurityTestHarness
from baobab_auth_security.tokens import (
    JwtAlgorithm,
    JwtDecoder,
    JwtEncoder,
    JwtTokenProvider,
    JwtValidator,
    SecurityTokenClaims,
    SecurityTokenPair,
)
from baobab_auth_security.version import __version__

__all__ = [
    "JWK",
    "JWKS",
    "Argon2PasswordHasher",
    "Clock",
    "ConfigurationError",
    "CoreClaimsMapper",
    "CorePasswordHasherAdapter",
    "CoreRevocationAdapter",
    "CoreTokenPairMapper",
    "CoreTokenProviderAdapter",
    "EcJwk",
    "EcKeyGenerator",
    "EcPublicJwkConverter",
    "Ed25519KeyGenerator",
    "FixedClock",
    "InMemoryKeyProvider",
    "InMemoryRevocationChecker",
    "InvalidAlgorithmError",
    "JwkPublicKeyLoader",
    "JwksDocumentParser",
    "JwksFetchError",
    "JwtAlgorithm",
    "JwtDecoder",
    "JwtEncoder",
    "JwtTokenProvider",
    "JwtValidator",
    "KeyAlgorithm",
    "KeyGenerator",
    "KeyIdDeriver",
    "KeyManagementError",
    "KeyNotFoundError",
    "KeyPair",
    "KeyStatus",
    "LocalJwksProvider",
    "OkpJwk",
    "OkpPublicJwkConverter",
    "PasswordHashPolicy",
    "PasswordHashResult",
    "PasswordHashingError",
    "PasswordVerificationResult",
    "PemKeyLoader",
    "PublicJwk",
    "PublicJwkConverter",
    "RefreshTokenError",
    "RefreshTokenGenerator",
    "RefreshTokenHasher",
    "RefreshTokenResult",
    "RemoteJwksFetcher",
    "RevocationChecker",
    "RsaPublicJwkConverter",
    "SecurityError",
    "SecuritySettings",
    "SecurityTestHarness",
    "SecurityTokenClaims",
    "SecurityTokenPair",
    "SystemClock",
    "TokenEncodingError",
    "TokenError",
    "TokenExpiredError",
    "TokenRevokedError",
    "TokenSignatureError",
    "TokenValidationError",
    "__version__",
]
