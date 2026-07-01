"""Représentation d'une JSON Web Key elliptique (EC).

:spec: FEAT-020.1, ADR-0006
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EcJwk:
    """JSON Web Key publique EC (champs ``crv``, ``x``, ``y`` uniquement).

    :param kid: Identifiant de clé.
    :param alg: Algorithme de signature (ex. ``"ES256"``).
    :param crv: Courbe elliptique (ex. ``"P-256"``).
    :param x: Coordonnée x en base64url.
    :param y: Coordonnée y en base64url.
    :param kty: Type de clé (``"EC"``).
    :param use: Usage (``"sig"``).
    """

    kid: str
    alg: str
    crv: str
    x: str
    y: str
    kty: str = "EC"
    use: str = "sig"

    def to_dict(self) -> dict[str, str]:
        """Sérialise la JWK en dictionnaire (champs publics uniquement).

        :returns: Représentation JSON-compatible.
        """
        return {
            "kty": self.kty,
            "use": self.use,
            "alg": self.alg,
            "kid": self.kid,
            "crv": self.crv,
            "x": self.x,
            "y": self.y,
        }
