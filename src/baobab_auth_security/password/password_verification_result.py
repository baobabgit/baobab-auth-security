"""Résultat typé d'une vérification de mot de passe.

:spec: FEAT-010.1
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PasswordVerificationResult:
    """Résultat d'une vérification de mot de passe.

    :param is_valid: ``True`` si le mot de passe correspond au hash.
    :param needs_rehash: ``True`` si le hash devrait être recalculé (paramètres
        obsolètes). Toujours ``False`` lorsque ``is_valid`` est ``False``.
    """

    is_valid: bool
    needs_rehash: bool = False

    def __bool__(self) -> bool:
        """Permet d'utiliser le résultat comme un booléen de validité.

        :returns: La valeur de :attr:`is_valid`.
        """
        return self.is_valid
