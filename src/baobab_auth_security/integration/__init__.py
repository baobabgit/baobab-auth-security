"""Module ``integration`` — adaptateurs et mappers vers ``baobab-auth-core``.

:spec: FEAT-011.1
"""

from __future__ import annotations

from baobab_auth_security.integration.core_claims_mapper import CoreClaimsMapper
from baobab_auth_security.integration.core_password_hasher_adapter import (
    CorePasswordHasherAdapter,
)
from baobab_auth_security.integration.core_revocation_adapter import (
    CoreRevocationAdapter,
)
from baobab_auth_security.integration.core_token_pair_mapper import CoreTokenPairMapper
from baobab_auth_security.integration.core_token_provider_adapter import (
    CoreTokenProviderAdapter,
)

__all__ = [
    "CoreClaimsMapper",
    "CorePasswordHasherAdapter",
    "CoreRevocationAdapter",
    "CoreTokenPairMapper",
    "CoreTokenProviderAdapter",
]
