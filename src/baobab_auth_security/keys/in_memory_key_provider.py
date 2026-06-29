"""Fournisseur de clés en mémoire (signature + résolution par ``kid``).

:spec: FEAT-010.4
"""

from __future__ import annotations

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from baobab_auth_security.exceptions import KeyManagementError, KeyNotFoundError
from baobab_auth_security.keys.key_pair import KeyPair
from baobab_auth_security.keys.key_status import KeyStatus


class InMemoryKeyProvider:
    """Conserve des paires de clés et désigne la clé active de signature.

    Fournit ``public_key_for_kid`` compatible avec le type
    :data:`baobab_auth_security.tokens.jwt_decoder.PublicKeyResolver`.

    :param keys: Paires initiales ; la première ``ACTIVE`` devient la clé de
        signature courante.
    """

    def __init__(self, keys: tuple[KeyPair, ...] = ()) -> None:
        """Initialise le fournisseur à partir d'un jeu de clés."""
        self._keys: dict[str, KeyPair] = {}
        self._active_kid: str | None = None
        for key in keys:
            self.add(key)

    def add(self, key_pair: KeyPair) -> None:
        """Ajoute une paire de clés ; la première ``ACTIVE`` devient signataire.

        :param key_pair: Paire à ajouter.
        :raises KeyManagementError: Si le ``kid`` est déjà présent.
        """
        if key_pair.kid in self._keys:
            raise KeyManagementError(f"kid déjà présent : {key_pair.kid}")
        self._keys[key_pair.kid] = key_pair
        if self._active_kid is None and key_pair.status is KeyStatus.ACTIVE:
            self._active_kid = key_pair.kid

    def set_active(self, kid: str) -> None:
        """Désigne la clé active de signature.

        :param kid: ``kid`` de la clé à activer.
        :raises KeyNotFoundError: Si le ``kid`` est inconnu.
        """
        if kid not in self._keys:
            raise KeyNotFoundError(f"kid inconnu : {kid}")
        self._active_kid = kid

    def active(self) -> KeyPair:
        """Retourne la paire de clés active de signature.

        :returns: La paire active.
        :raises KeyManagementError: Si aucune clé active n'est définie.
        """
        if self._active_kid is None:
            raise KeyManagementError("Aucune clé active de signature.")
        return self._keys[self._active_kid]

    def public_key_for_kid(self, kid: str) -> RSAPublicKey:
        """Résout une clé publique par ``kid`` (résolveur de vérification).

        :param kid: Identifiant de clé recherché.
        :returns: Clé publique RSA correspondante.
        :raises KeyNotFoundError: Si le ``kid`` est inconnu.
        """
        try:
            return self._keys[kid].public_key
        except KeyError as exc:
            raise KeyNotFoundError(f"kid inconnu : {kid}") from exc

    def all_keys(self) -> tuple[KeyPair, ...]:
        """Retourne toutes les paires connues.

        :returns: Tuple des paires de clés.
        """
        return tuple(self._keys.values())
