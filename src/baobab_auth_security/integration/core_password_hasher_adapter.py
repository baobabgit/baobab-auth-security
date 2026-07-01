"""Adaptateur du hasher Argon2 vers le port ``PasswordHasher`` du core.

:spec: FEAT-011.1, ADR-0005
"""

from __future__ import annotations

from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.plain_password import PlainPassword

from baobab_auth_security.password.argon2_password_hasher import Argon2PasswordHasher


class CorePasswordHasherAdapter:
    """Expose :class:`Argon2PasswordHasher` derrière le port réel du core.

    Satisfait ``baobab_auth_core.ports.password_hasher.PasswordHasher``
    (synchrone : ``hash`` / ``verify``).

    :param hasher: Service Argon2 sous-jacent ; défaut :class:`Argon2PasswordHasher`.
    """

    def __init__(self, hasher: Argon2PasswordHasher | None = None) -> None:
        """Initialise l'adaptateur."""
        self._hasher = hasher or Argon2PasswordHasher()

    def hash(self, password: PlainPassword) -> PasswordHash:
        """Hache un mot de passe et retourne le VO ``PasswordHash`` du core.

        :param password: Mot de passe en clair du core.
        :returns: Hash sous forme de value object du core.
        """
        return PasswordHash(self._hasher.hash(password.value).value)

    def verify(self, password: PlainPassword, password_hash: PasswordHash) -> bool:
        """Vérifie un mot de passe face à son hash.

        :param password: Mot de passe en clair du core.
        :param password_hash: Hash de référence du core.
        :returns: ``True`` si le mot de passe correspond.
        """
        return self._hasher.verify(password.value, password_hash.value).is_valid
