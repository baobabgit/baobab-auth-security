"""Représentation d'une JSON Web Key OKP (Ed25519).

:spec: FEAT-020.1, ADR-0006
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OkpJwk:
    """JSON Web Key publique OKP (champ ``x`` uniquement).

    :param kid: Identifiant de clé.
    :param alg: Algorithme de signature (``"EdDSA"``).
    :param crv: Courbe (``"Ed25519"``).
    :param x: Clé publique en base64url.
    :param kty: Type de clé (``"OKP"``).
    :param use: Usage (``"sig"``).
    """

    kid: str
    alg: str
    crv: str
    x: str
    kty: str = "OKP"
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
        }
