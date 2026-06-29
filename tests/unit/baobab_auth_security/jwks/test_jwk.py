"""Tests de :class:`JWK`.

:spec: FEAT-010.4, ADR-0006
"""

from __future__ import annotations

from baobab_auth_security.jwks.jwk import JWK


class TestJwk:
    """Vérifie que la JWK n'expose que des champs publics."""

    def test_FEAT_010_4_to_dict_contains_only_public_fields(self) -> None:
        jwk = JWK(kid="k1", alg="RS256", n="abc", e="AQAB")
        data = jwk.to_dict()
        assert data == {
            "kty": "RSA",
            "use": "sig",
            "alg": "RS256",
            "kid": "k1",
            "n": "abc",
            "e": "AQAB",
        }
        # Aucun composant privé ne doit apparaître.
        assert {"d", "p", "q", "dp", "dq", "qi"}.isdisjoint(data)
