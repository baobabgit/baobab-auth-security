"""Service de hachage de mot de passe Argon2id.

:spec: FEAT-010.1, ADR-0002
"""

from __future__ import annotations

from argon2 import PasswordHasher as _Argon2Hasher
from argon2 import Type
from argon2.exceptions import InvalidHashError, VerifyMismatchError

from baobab_auth_security.exceptions import PasswordHashingError
from baobab_auth_security.password.password_hash_policy import PasswordHashPolicy
from baobab_auth_security.password.password_hash_result import PasswordHashResult
from baobab_auth_security.password.password_verification_result import (
    PasswordVerificationResult,
)


class Argon2PasswordHasher:
    """Hache et vérifie des mots de passe avec Argon2id.

    Service technique riche : il renvoie des résultats typés et masque tout
    secret. L'adaptateur ``CorePasswordHasherAdapter`` (BL-S-010-006) restreint
    sa surface au port ``PasswordHasher`` du core.

    :param policy: Politique de coût Argon2 ; défaut :class:`PasswordHashPolicy`.
    """

    def __init__(self, policy: PasswordHashPolicy | None = None) -> None:
        """Initialise le hasher à partir d'une politique de coût."""
        self._policy = policy or PasswordHashPolicy()
        self._hasher = _Argon2Hasher(
            time_cost=self._policy.time_cost,
            memory_cost=self._policy.memory_cost,
            parallelism=self._policy.parallelism,
            hash_len=self._policy.hash_len,
            salt_len=self._policy.salt_len,
            type=Type.ID,
        )

    @property
    def policy(self) -> PasswordHashPolicy:
        """Politique de coût Argon2 active.

        :returns: La politique courante.
        """
        return self._policy

    def hash(self, plain_password: str) -> PasswordHashResult:
        """Hache un mot de passe en clair (Argon2id).

        :param plain_password: Mot de passe en clair, non vide.
        :returns: Résultat contenant le hash encodé (non réversible).
        :raises PasswordHashingError: Si le mot de passe est vide.
        """
        if not plain_password:
            raise PasswordHashingError("Le mot de passe à hacher est vide.")
        return PasswordHashResult(self._hasher.hash(plain_password))

    def verify(
        self, plain_password: str, password_hash: str
    ) -> PasswordVerificationResult:
        """Vérifie un mot de passe face à son hash, en temps constant.

        :param plain_password: Mot de passe en clair à vérifier.
        :param password_hash: Hash de référence (``$argon2id$...``).
        :returns: Résultat (``is_valid`` et ``needs_rehash``).
        :raises PasswordHashingError: Si le hash de référence est malformé.
        """
        try:
            self._hasher.verify(password_hash, plain_password)
        except VerifyMismatchError:
            return PasswordVerificationResult(is_valid=False, needs_rehash=False)
        except InvalidHashError as exc:
            raise PasswordHashingError("Hash de mot de passe invalide.") from exc
        return PasswordVerificationResult(
            is_valid=True,
            needs_rehash=self._hasher.check_needs_rehash(password_hash),
        )

    def needs_rehash(self, password_hash: str) -> bool:
        """Indique si un hash devrait être recalculé (paramètres obsolètes).

        :param password_hash: Hash à analyser.
        :returns: ``True`` si un re-hachage est recommandé.
        """
        return self._hasher.check_needs_rehash(password_hash)
