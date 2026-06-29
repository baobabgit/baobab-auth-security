"""Tests de :class:`JWKS`.

:spec: FEAT-010.4
"""

from __future__ import annotations

from baobab_auth_security.jwks.jwk import JWK
from baobab_auth_security.jwks.jwks import JWKS


class TestJwks:
    """Vérifie la sérialisation de l'ensemble de clés."""

    def test_FEAT_010_4_to_dict_wraps_keys(self) -> None:
        jwks = JWKS(
            keys=(
                JWK(kid="k1", alg="RS256", n="n1", e="AQAB"),
                JWK(kid="k2", alg="RS384", n="n2", e="AQAB"),
            )
        )
        data = jwks.to_dict()
        assert set(data) == {"keys"}
        assert len(data["keys"]) == 2
        assert jwks.key_ids() == ("k1", "k2")

    def test_FEAT_010_4_empty_jwks(self) -> None:
        assert JWKS(keys=()).to_dict() == {"keys": []}
