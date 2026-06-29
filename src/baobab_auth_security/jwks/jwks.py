"""Ensemble de JSON Web Keys (JWKS).

:spec: FEAT-010.4
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from baobab_auth_security.jwks.jwk import JWK


@dataclass(frozen=True)
class JWKS:
    """Ensemble de clés publiques (JWK Set).

    :param keys: Clés publiques exposées.
    """

    keys: tuple[JWK, ...]

    def to_dict(self) -> dict[str, Any]:
        """Sérialise le JWKS au format ``{"keys": [...]}``.

        :returns: Représentation JSON-compatible (clés publiques uniquement).
        """
        return {"keys": [key.to_dict() for key in self.keys]}

    def key_ids(self) -> tuple[str, ...]:
        """Retourne les ``kid`` publiés.

        :returns: Tuple des identifiants de clés.
        """
        return tuple(key.kid for key in self.keys)
