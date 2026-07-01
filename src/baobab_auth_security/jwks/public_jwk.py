"""Union des types de JWK publiques supportées.

:spec: FEAT-020.1
"""

from __future__ import annotations

from baobab_auth_security.jwks.ec_jwk import EcJwk
from baobab_auth_security.jwks.jwk import JWK
from baobab_auth_security.jwks.okp_jwk import OkpJwk

type PublicJwk = JWK | EcJwk | OkpJwk
"""JWK publique RSA, EC ou OKP."""
