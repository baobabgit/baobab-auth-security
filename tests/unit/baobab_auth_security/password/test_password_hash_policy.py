"""Tests de :class:`PasswordHashPolicy`.

:spec: FEAT-010.1
"""

from __future__ import annotations

import pytest

from baobab_auth_security.exceptions import ConfigurationError
from baobab_auth_security.password.password_hash_policy import PasswordHashPolicy


class TestPasswordHashPolicy:
    """Valide les bornes de la politique de coût Argon2."""

    def test_FEAT_010_1_defaults_are_sane(self) -> None:
        policy = PasswordHashPolicy()
        assert policy.time_cost >= 1
        assert policy.memory_cost >= 8
        assert policy.hash_len >= 16

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"time_cost": 0},
            {"memory_cost": 4},
            {"memory_cost": 8, "parallelism": 4},
            {"parallelism": 0},
            {"hash_len": 8},
            {"salt_len": 4},
        ],
    )
    def test_FEAT_010_1_rejects_out_of_range(self, kwargs: dict[str, int]) -> None:
        with pytest.raises(ConfigurationError):
            PasswordHashPolicy(**kwargs)

    def test_FEAT_010_1_is_frozen(self) -> None:
        policy = PasswordHashPolicy()
        with pytest.raises(AttributeError):
            policy.time_cost = 9  # type: ignore[misc]
