"""Algorithmes de signature RSA supportés pour les clés.

:spec: FEAT-010.4
"""

from __future__ import annotations

from enum import StrEnum

from baobab_auth_security.exceptions import ConfigurationError


class KeyAlgorithm(StrEnum):
    """Algorithmes de signature RSA (alignés sur ``JwtAlgorithm``)."""

    RS256 = "RS256"
    RS384 = "RS384"
    RS512 = "RS512"

    @classmethod
    def from_name(cls, name: str) -> KeyAlgorithm:
        """Résout un algorithme de clé depuis son nom.

        :param name: Nom (ex. ``"RS256"``).
        :returns: Membre correspondant.
        :raises ConfigurationError: Si l'algorithme est inconnu.
        """
        try:
            return cls(name)
        except ValueError as exc:
            raise ConfigurationError(
                f"Algorithme de clé non supporté : {name!r}."
            ) from exc
