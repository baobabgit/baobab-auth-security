"""Génération de paires de clés RSA.

:spec: FEAT-010.4
"""

from __future__ import annotations

import hashlib

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from baobab_auth_security.clock.clock import Clock
from baobab_auth_security.exceptions import ConfigurationError
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm
from baobab_auth_security.keys.key_pair import KeyPair
from baobab_auth_security.keys.key_status import KeyStatus

_MIN_KEY_SIZE = 2048
_PUBLIC_EXPONENT = 65537


class KeyGenerator:
    """Génère des paires de clés RSA avec un ``kid`` stable.

    :param clock: Horloge UTC injectée (date de création).
    :param key_size: Taille de la clé RSA, en bits (>= 2048).
    :raises ConfigurationError: Si ``key_size`` < 2048.
    """

    def __init__(self, clock: Clock, key_size: int = _MIN_KEY_SIZE) -> None:
        """Initialise le générateur."""
        if key_size < _MIN_KEY_SIZE:
            raise ConfigurationError("key_size doit être >= 2048 bits.")
        self._clock = clock
        self._key_size = key_size

    def generate(
        self,
        algorithm: KeyAlgorithm = KeyAlgorithm.RS256,
        kid: str | None = None,
        status: KeyStatus = KeyStatus.ACTIVE,
    ) -> KeyPair:
        """Génère une paire de clés RSA.

        :param algorithm: Algorithme de signature associé.
        :param kid: Identifiant de clé ; dérivé de la clé publique si ``None``.
        :param status: Statut initial.
        :returns: La paire de clés générée.
        """
        private_key = rsa.generate_private_key(
            public_exponent=_PUBLIC_EXPONENT, key_size=self._key_size
        )
        public_key = private_key.public_key()
        return KeyPair(
            kid=kid or self._derive_kid(public_key),
            algorithm=algorithm,
            private_key=private_key,
            public_key=public_key,
            status=status,
            created_at=self._clock.now(),
        )

    @staticmethod
    def _derive_kid(public_key: RSAPublicKey) -> str:
        """Dérive un ``kid`` stable à partir de la clé publique.

        :param public_key: Clé publique RSA.
        :returns: ``kid`` hexadécimal (16 caractères).
        """
        der = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return hashlib.sha256(der).hexdigest()[:16]
