"""Représentation d'une JSON Web Key (clé publique RSA uniquement).

:spec: FEAT-010.4, ADR-0006
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JWK:
    """JSON Web Key publique RSA.

    Ne contient **que** des champs publics (``kty``, ``use``, ``alg``, ``kid``,
    ``n``, ``e``) — jamais ``d``, ``p`` ou ``q``.

    :param kid: Identifiant de clé.
    :param alg: Algorithme de signature (ex. ``"RS256"``).
    :param n: Module RSA encodé en base64url.
    :param e: Exposant public RSA encodé en base64url.
    :param kty: Type de clé (``"RSA"``).
    :param use: Usage (``"sig"``).
    """

    kid: str
    alg: str
    n: str
    e: str
    kty: str = "RSA"
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
            "n": self.n,
            "e": self.e,
        }
