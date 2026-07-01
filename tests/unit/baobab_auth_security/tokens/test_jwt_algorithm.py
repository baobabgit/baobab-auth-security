"""Tests de :class:`JwtAlgorithm`.

:spec: FEAT-010.2, ADR-0003
"""

from __future__ import annotations

import pytest

from baobab_auth_security.exceptions import InvalidAlgorithmError
from baobab_auth_security.tokens.jwt_algorithm import JwtAlgorithm


class TestJwtAlgorithm:
    """Vérifie la liste blanche d'algorithmes et le refus de ``none``."""

    def test_FEAT_010_2_from_name_accepts_rs256(self) -> None:
        assert JwtAlgorithm.from_name("RS256") is JwtAlgorithm.RS256

    @pytest.mark.parametrize("name", ["none", "None", "HS256", "unknown"])
    def test_FEAT_010_2_from_name_rejects_disallowed(self, name: str) -> None:
        with pytest.raises(InvalidAlgorithmError):
            JwtAlgorithm.from_name(name)

    def test_FEAT_020_1_from_name_accepts_ec_and_eddsa(self) -> None:
        assert JwtAlgorithm.from_name("ES256") is JwtAlgorithm.ES256
        assert JwtAlgorithm.from_name("EdDSA") is JwtAlgorithm.EdDSA

    def test_FEAT_020_1_names_includes_ec_and_eddsa(self) -> None:
        names = JwtAlgorithm.names()
        assert "ES256" in names
        assert "EdDSA" in names
        assert names[:3] == ("RS256", "RS384", "RS512")
