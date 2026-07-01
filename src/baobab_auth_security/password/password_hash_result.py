"""Résultat typé d'un hachage de mot de passe.

:spec: FEAT-010.1, ADR-0006
"""

from __future__ import annotations

from dataclasses import dataclass

from baobab_auth_security.exceptions import PasswordHashingError


@dataclass(frozen=True)
class PasswordHashResult:
    """Encapsule un hash de mot de passe Argon2id.

    Le hash est exposé via :attr:`value` (destiné au stockage par l'appelant),
    mais masqué dans :meth:`__repr__` / :meth:`__str__` pour éviter toute fuite
    accidentelle dans les logs.

    :param value: Représentation encodée du hash (``$argon2id$...``).
    :raises PasswordHashingError: Si la valeur est vide.
    """

    value: str

    def __post_init__(self) -> None:
        """Valide que le hash n'est pas vide.

        :raises PasswordHashingError: Si vide.
        """
        if not self.value:
            raise PasswordHashingError("Le hash de mot de passe est vide.")

    def __str__(self) -> str:
        """Retourne une représentation masquée.

        :returns: ``'***'``.
        """
        return "***"

    def __repr__(self) -> str:
        """Retourne une représentation masquée.

        :returns: Représentation sans valeur de hash.
        """
        return "PasswordHashResult(value='***')"
