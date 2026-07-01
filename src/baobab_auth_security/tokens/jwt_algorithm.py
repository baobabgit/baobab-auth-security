"""Algorithmes de signature JWT autorisés.

:spec: FEAT-010.2, ADR-0003
"""

from __future__ import annotations

from enum import StrEnum

from baobab_auth_security.exceptions import InvalidAlgorithmError


class JwtAlgorithm(StrEnum):
    """Liste blanche des algorithmes de signature JWT supportés.

    ``alg=none`` et tout algorithme symétrique (HS*) sont exclus par construction.
    """

    RS256 = "RS256"
    RS384 = "RS384"
    RS512 = "RS512"
    ES256 = "ES256"
    ES384 = "ES384"
    ES512 = "ES512"
    EdDSA = "EdDSA"

    @classmethod
    def from_name(cls, name: str) -> JwtAlgorithm:
        """Résout un algorithme depuis son nom, en refusant l'inconnu.

        :param name: Nom d'algorithme (ex. ``"RS256"``).
        :returns: Membre :class:`JwtAlgorithm` correspondant.
        :raises InvalidAlgorithmError: Si ``name`` vaut ``none`` ou n'est pas
            dans la liste blanche.
        """
        try:
            return cls(name)
        except ValueError as exc:
            raise InvalidAlgorithmError(
                f"Algorithme JWT non autorisé : {name!r}."
            ) from exc

    @classmethod
    def names(cls) -> tuple[str, ...]:
        """Retourne les noms d'algorithmes autorisés.

        :returns: Tuple des noms (ex. ``("RS256", "RS384", "RS512")``).
        """
        return tuple(algorithm.value for algorithm in cls)
