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

    @pytest.mark.parametrize("name", ["none", "None", "HS256", "ES256", "unknown"])
    def test_FEAT_010_2_from_name_rejects_disallowed(self, name: str) -> None:
        with pytest.raises(InvalidAlgorithmError):
            JwtAlgorithm.from_name(name)

    def test_FEAT_010_2_names_lists_only_rs_family(self) -> None:
        assert JwtAlgorithm.names() == ("RS256", "RS384", "RS512")
