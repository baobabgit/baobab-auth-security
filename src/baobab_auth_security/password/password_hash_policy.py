"""Politique de paramètres Argon2id.

:spec: FEAT-010.1, ADR-0002
"""

from __future__ import annotations

from dataclasses import dataclass

from baobab_auth_security.exceptions import ConfigurationError


@dataclass(frozen=True)
class PasswordHashPolicy:
    """Paramètres de coût Argon2id (valeurs par défaut alignées OWASP).

    :param time_cost: Nombre d'itérations.
    :param memory_cost: Mémoire utilisée, en kibioctets (KiB).
    :param parallelism: Degré de parallélisme.
    :param hash_len: Longueur du hash dérivé, en octets.
    :param salt_len: Longueur du sel aléatoire, en octets.
    :raises ConfigurationError: Si un paramètre est hors borne admissible.
    """

    time_cost: int = 3
    memory_cost: int = 65536
    parallelism: int = 4
    hash_len: int = 32
    salt_len: int = 16

    def __post_init__(self) -> None:
        """Valide la cohérence des paramètres de coût.

        :raises ConfigurationError: Si un paramètre est trop faible.
        """
        if self.time_cost < 1:
            raise ConfigurationError("time_cost doit être >= 1.")
        if self.memory_cost < 8:
            raise ConfigurationError("memory_cost doit être >= 8 KiB.")
        if self.parallelism < 1:
            raise ConfigurationError("parallelism doit être >= 1.")
        if self.memory_cost < 8 * self.parallelism:
            raise ConfigurationError("memory_cost doit être >= 8 * parallelism.")
        if self.hash_len < 16:
            raise ConfigurationError("hash_len doit être >= 16 octets.")
        if self.salt_len < 8:
            raise ConfigurationError("salt_len doit être >= 8 octets.")
