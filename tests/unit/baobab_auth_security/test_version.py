"""Tests du module ``version``.

:spec: FEAT-012.1
"""

from __future__ import annotations

import baobab_auth_security
from baobab_auth_security.version import __version__


class TestVersion:
    """Vérifie l'exposition de la version du package."""

    def test_FEAT_012_1_version_is_semver_string(self) -> None:
        # Arrange / Act
        version = __version__

        # Assert
        assert version == "0.1.0"
        assert version.count(".") == 2

    def test_FEAT_012_1_version_reexported_at_package_root(self) -> None:
        # Assert
        assert baobab_auth_security.__version__ == __version__
