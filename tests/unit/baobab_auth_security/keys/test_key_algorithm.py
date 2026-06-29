"""Tests de :class:`KeyAlgorithm`.

:spec: FEAT-010.4
"""

from __future__ import annotations

import pytest

from baobab_auth_security.exceptions import ConfigurationError
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm


class TestKeyAlgorithm:
    """Vérifie la résolution des algorithmes de clé."""

    def test_FEAT_010_4_from_name_resolves_known(self) -> None:
        assert KeyAlgorithm.from_name("RS512") is KeyAlgorithm.RS512

    def test_FEAT_010_4_from_name_rejects_unknown(self) -> None:
        with pytest.raises(ConfigurationError):
            KeyAlgorithm.from_name("ES256")
